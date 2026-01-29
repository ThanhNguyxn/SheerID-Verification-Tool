"""
Spotify Student Verification Tool
SheerID Student Verification for Spotify Premium

Enhanced with:
- Success rate tracking per organization
- Weighted university selection (35+ countries supported)
- Retry with exponential backoff
- Rate limiting avoidance
- Anti-detection with Chrome TLS impersonation

Requirements:
- curl_cffi: pip install curl_cffi (CRITICAL for TLS spoofing)
- Residential proxy (STRONGLY recommended for better success rate)

Author: ThanhNguyxn
"""

import os
import re
import sys
import json
import time
import random
import hashlib
from pathlib import Path
from io import BytesIO
from typing import Dict, Optional, Tuple
from functools import wraps

try:
    import httpx
except ImportError:
    print("❌ Error: httpx required. Install: pip install httpx")
    sys.exit(1)

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("❌ Error: Pillow required. Install: pip install Pillow")
    sys.exit(1)

# Import anti-detection module
try:
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from anti_detect import (
        get_headers,
        get_fingerprint,
        get_random_user_agent,
        random_delay as anti_delay,
        create_session,
        get_matched_ua_for_impersonate,
        make_request,
        check_proxy_type,
        handle_fraud_rejection,
        should_retry_fraud,
    )

    HAS_ANTI_DETECT = True
    print("[INFO] Anti-detection module loaded")
except ImportError:
    HAS_ANTI_DETECT = False
    print("[WARN] anti_detect.py not found - detection risk is HIGH!")
    print("[WARN] Install: pip install curl_cffi for better success rate")


# ============ CONFIG ============
PROGRAM_ID = "67c8c14f5f17a83b745e3f82"
SHEERID_API_URL = "https://services.sheerid.com/rest/v2"
MIN_DELAY = 300
MAX_DELAY = 800


# ============ STATS TRACKING ============
class Stats:
    """Track success rates by organization"""

    def __init__(self):
        self.file = Path(__file__).parent / "stats.json"
        self.data = self._load()

    def _load(self) -> Dict:
        if self.file.exists():
            try:
                return json.loads(self.file.read_text())
            except:
                pass
        return {"total": 0, "success": 0, "failed": 0, "orgs": {}}

    def _save(self):
        self.file.write_text(json.dumps(self.data, indent=2))

    def record(self, org: str, success: bool):
        self.data["total"] += 1
        self.data["success" if success else "failed"] += 1

        if org not in self.data["orgs"]:
            self.data["orgs"][org] = {"success": 0, "failed": 0}
        self.data["orgs"][org]["success" if success else "failed"] += 1
        self._save()

    def get_rate(self, org: str = None) -> float:
        if org:
            o = self.data["orgs"].get(org, {})
            total = o.get("success", 0) + o.get("failed", 0)
            return o.get("success", 0) / total * 100 if total else 50
        return (
            self.data["success"] / self.data["total"] * 100 if self.data["total"] else 0
        )

    def print_stats(self):
        print(f"\n📊 Statistics:")
        print(
            f"   Total: {self.data['total']} | ✅ {self.data['success']} | ❌ {self.data['failed']}"
        )
        if self.data["total"]:
            print(f"   Success Rate: {self.get_rate():.1f}%")


stats = Stats()


# ============ UNIVERSITIES WITH WEIGHTS ============
# Spotify Premium Student Discount supports 35+ countries including:
# USA, UK, Canada, Australia, Germany, France, Japan, Brazil, Mexico,
# Netherlands, Spain, Italy, Singapore, Hong Kong, Indonesia, Turkey,
# Chile, Colombia, Czech Republic, Denmark, Finland, Greece, Hungary,
# Ireland, New Zealand, Philippines, Portugal, Switzerland, and more.

UNIVERSITIES = [
    # =========== USA - HIGH PRIORITY (15 schools) ===========
    {
        "id": 2565,
        "name": "Pennsylvania State University-Main Campus",
        "domain": "psu.edu",
        "weight": 100,
    },
    {
        "id": 3499,
        "name": "University of California, Los Angeles",
        "domain": "ucla.edu",
        "weight": 98,
    },
    {
        "id": 3491,
        "name": "University of California, Berkeley",
        "domain": "berkeley.edu",
        "weight": 97,
    },
    {
        "id": 1953,
        "name": "Massachusetts Institute of Technology",
        "domain": "mit.edu",
        "weight": 95,
    },
    {"id": 3113, "name": "Stanford University", "domain": "stanford.edu", "weight": 95},
    {"id": 2285, "name": "New York University", "domain": "nyu.edu", "weight": 96},
    {"id": 1426, "name": "Harvard University", "domain": "harvard.edu", "weight": 92},
    {"id": 698, "name": "Columbia University", "domain": "columbia.edu", "weight": 92},
    {"id": 3568, "name": "University of Michigan", "domain": "umich.edu", "weight": 95},
    {
        "id": 3686,
        "name": "University of Texas at Austin",
        "domain": "utexas.edu",
        "weight": 94,
    },
    {"id": 378, "name": "Arizona State University", "domain": "asu.edu", "weight": 93},
    {"id": 3521, "name": "University of Florida", "domain": "ufl.edu", "weight": 91},
    {
        "id": 1217,
        "name": "Georgia Institute of Technology",
        "domain": "gatech.edu",
        "weight": 90,
    },
    {
        "id": 602,
        "name": "Carnegie Mellon University",
        "domain": "cmu.edu",
        "weight": 89,
    },
    {"id": 2506, "name": "Ohio State University", "domain": "osu.edu", "weight": 88},
    # =========== CANADA - SUPPORTED (5 schools) ===========
    {
        "id": 328355,
        "name": "University of Toronto",
        "domain": "utoronto.ca",
        "weight": 88,
    },
    {"id": 4782066, "name": "McGill University", "domain": "mcgill.ca", "weight": 85},
    {
        "id": 328315,
        "name": "University of British Columbia",
        "domain": "ubc.ca",
        "weight": 86,
    },
    {
        "id": 328317,
        "name": "University of Waterloo",
        "domain": "uwaterloo.ca",
        "weight": 84,
    },
    {
        "id": 328319,
        "name": "University of Alberta",
        "domain": "ualberta.ca",
        "weight": 82,
    },
    # =========== UK - SUPPORTED (8 schools) ===========
    {"id": 273409, "name": "University of Oxford", "domain": "ox.ac.uk", "weight": 88},
    {
        "id": 273378,
        "name": "University of Cambridge",
        "domain": "cam.ac.uk",
        "weight": 88,
    },
    {
        "id": 273294,
        "name": "Imperial College London",
        "domain": "imperial.ac.uk",
        "weight": 85,
    },
    {
        "id": 273319,
        "name": "University College London",
        "domain": "ucl.ac.uk",
        "weight": 84,
    },
    {
        "id": 273381,
        "name": "University of Edinburgh",
        "domain": "ed.ac.uk",
        "weight": 82,
    },
    {
        "id": 273383,
        "name": "University of Manchester",
        "domain": "manchester.ac.uk",
        "weight": 80,
    },
    {
        "id": 273385,
        "name": "King's College London",
        "domain": "kcl.ac.uk",
        "weight": 79,
    },
    {
        "id": 273387,
        "name": "London School of Economics",
        "domain": "lse.ac.uk",
        "weight": 81,
    },
    # =========== GERMANY - SUPPORTED (6 schools) ===========
    {
        "id": 10011178,
        "name": "Technical University of Munich",
        "domain": "tum.de",
        "weight": 85,
    },
    {
        "id": 344450,
        "name": "Ludwig Maximilian University of Munich",
        "domain": "lmu.de",
        "weight": 83,
    },
    {
        "id": 344452,
        "name": "Heidelberg University",
        "domain": "uni-heidelberg.de",
        "weight": 81,
    },
    {
        "id": 344454,
        "name": "Humboldt University of Berlin",
        "domain": "hu-berlin.de",
        "weight": 80,
    },
    {
        "id": 344456,
        "name": "RWTH Aachen University",
        "domain": "rwth-aachen.de",
        "weight": 82,
    },
    {
        "id": 344458,
        "name": "Free University of Berlin",
        "domain": "fu-berlin.de",
        "weight": 79,
    },
    # =========== FRANCE - SUPPORTED (5 schools) ===========
    {
        "id": 329766,
        "name": "Ecole Polytechnique",
        "domain": "polytechnique.edu",
        "weight": 82,
    },
    {
        "id": 10148649,
        "name": "PSL Research University",
        "domain": "psl.eu",
        "weight": 80,
    },
    {
        "id": 329768,
        "name": "Sorbonne University",
        "domain": "sorbonne-universite.fr",
        "weight": 81,
    },
    {"id": 329770, "name": "Sciences Po", "domain": "sciencespo.fr", "weight": 79},
    {"id": 329772, "name": "HEC Paris", "domain": "hec.edu", "weight": 78},
    # =========== AUSTRALIA - SUPPORTED (6 schools) ===========
    {
        "id": 345301,
        "name": "The University of Melbourne",
        "domain": "unimelb.edu.au",
        "weight": 85,
    },
    {
        "id": 345303,
        "name": "The University of Sydney",
        "domain": "sydney.edu.au",
        "weight": 83,
    },
    {
        "id": 345276,
        "name": "Australian National University",
        "domain": "anu.edu.au",
        "weight": 81,
    },
    {
        "id": 345305,
        "name": "University of Queensland",
        "domain": "uq.edu.au",
        "weight": 80,
    },
    {"id": 345307, "name": "Monash University", "domain": "monash.edu", "weight": 79},
    {"id": 345309, "name": "UNSW Sydney", "domain": "unsw.edu.au", "weight": 82},
    # =========== JAPAN - SUPPORTED (5 schools) ===========
    {
        "id": 354085,
        "name": "The University of Tokyo",
        "domain": "u-tokyo.ac.jp",
        "weight": 83,
    },
    {"id": 353961, "name": "Kyoto University", "domain": "kyoto-u.ac.jp", "weight": 81},
    {"id": 353963, "name": "Osaka University", "domain": "osaka-u.ac.jp", "weight": 79},
    {"id": 353965, "name": "Tohoku University", "domain": "tohoku.ac.jp", "weight": 78},
    {
        "id": 353967,
        "name": "Tokyo Institute of Technology",
        "domain": "titech.ac.jp",
        "weight": 80,
    },
    # =========== BRAZIL - SUPPORTED (5 schools) ===========
    {
        "id": 10042652,
        "name": "University of Sao Paulo",
        "domain": "usp.br",
        "weight": 82,
    },
    {
        "id": 10059316,
        "name": "University of Campinas",
        "domain": "unicamp.br",
        "weight": 79,
    },
    {
        "id": 412760,
        "name": "Federal University of Rio de Janeiro",
        "domain": "ufrj.br",
        "weight": 78,
    },
    {
        "id": 412762,
        "name": "Federal University of Minas Gerais",
        "domain": "ufmg.br",
        "weight": 77,
    },
    {
        "id": 412764,
        "name": "Federal University of Rio Grande do Sul",
        "domain": "ufrgs.br",
        "weight": 76,
    },
    # =========== INDONESIA - SUPPORTED (5 schools) ===========
    {
        "id": 10008577,
        "name": "University of Indonesia",
        "domain": "ui.ac.id",
        "weight": 82,
    },
    {
        "id": 10008584,
        "name": "Institut Teknologi Bandung",
        "domain": "itb.ac.id",
        "weight": 80,
    },
    {
        "id": 10008579,
        "name": "Gadjah Mada University",
        "domain": "ugm.ac.id",
        "weight": 79,
    },
    {
        "id": 10008581,
        "name": "Airlangga University",
        "domain": "unair.ac.id",
        "weight": 77,
    },
    {
        "id": 10008589,
        "name": "Institut Teknologi Sepuluh Nopember",
        "domain": "its.ac.id",
        "weight": 78,
    },
    # =========== OTHER SUPPORTED COUNTRIES ===========
    # Singapore
    {
        "id": 356355,
        "name": "National University of Singapore",
        "domain": "nus.edu.sg",
        "weight": 85,
    },
    {
        "id": 356356,
        "name": "Nanyang Technological University",
        "domain": "ntu.edu.sg",
        "weight": 83,
    },
    # Netherlands
    {
        "id": 345979,
        "name": "Delft University of Technology",
        "domain": "tudelft.nl",
        "weight": 80,
    },
    {"id": 345981, "name": "University of Amsterdam", "domain": "uva.nl", "weight": 78},
    # Mexico
    {
        "id": 10019857,
        "name": "Universidad Nacional Autónoma de México",
        "domain": "unam.mx",
        "weight": 80,
    },
    {
        "id": 10019859,
        "name": "Tecnológico de Monterrey",
        "domain": "tec.mx",
        "weight": 79,
    },
    # Hong Kong
    {"id": 356575, "name": "University of Hong Kong", "domain": "hku.hk", "weight": 82},
    {
        "id": 356577,
        "name": "Chinese University of Hong Kong",
        "domain": "cuhk.edu.hk",
        "weight": 80,
    },
    # Turkey
    {
        "id": 10012345,
        "name": "Bogazici University",
        "domain": "boun.edu.tr",
        "weight": 78,
    },
    {
        "id": 10012347,
        "name": "Middle East Technical University",
        "domain": "metu.edu.tr",
        "weight": 77,
    },
]


def select_university() -> Dict:
    """Weighted random selection based on success rates"""
    weights = []
    for uni in UNIVERSITIES:
        weight = uni["weight"] * (stats.get_rate(uni["name"]) / 50)
        weights.append(max(1, weight))

    total = sum(weights)
    r = random.uniform(0, total)

    cumulative = 0
    for uni, weight in zip(UNIVERSITIES, weights):
        cumulative += weight
        if r <= cumulative:
            return {**uni, "idExtended": str(uni["id"])}
    return {**UNIVERSITIES[0], "idExtended": str(UNIVERSITIES[0]["id"])}


# ============ UTILITIES ============
FIRST_NAMES = [
    "James",
    "John",
    "Robert",
    "Michael",
    "William",
    "David",
    "Richard",
    "Joseph",
    "Thomas",
    "Christopher",
    "Charles",
    "Daniel",
    "Matthew",
    "Anthony",
    "Mark",
    "Donald",
    "Steven",
    "Andrew",
    "Paul",
    "Joshua",
    "Kenneth",
    "Kevin",
    "Brian",
    "George",
    "Timothy",
    "Ronald",
    "Edward",
    "Jason",
    "Jeffrey",
    "Ryan",
    "Mary",
    "Patricia",
    "Jennifer",
    "Linda",
    "Barbara",
    "Elizabeth",
    "Susan",
    "Jessica",
    "Sarah",
    "Karen",
    "Lisa",
    "Nancy",
    "Betty",
    "Margaret",
    "Sandra",
    "Ashley",
    "Kimberly",
    "Emily",
    "Donna",
    "Michelle",
    "Dorothy",
    "Carol",
    "Amanda",
    "Melissa",
    "Deborah",
    "Stephanie",
    "Rebecca",
    "Sharon",
    "Laura",
    "Emma",
    "Olivia",
    "Ava",
    "Isabella",
    "Sophia",
    "Mia",
    "Charlotte",
    "Amelia",
]
LAST_NAMES = [
    "Smith",
    "Johnson",
    "Williams",
    "Brown",
    "Jones",
    "Garcia",
    "Miller",
    "Davis",
    "Rodriguez",
    "Martinez",
    "Hernandez",
    "Lopez",
    "Gonzalez",
    "Wilson",
    "Anderson",
    "Thomas",
    "Taylor",
    "Moore",
    "Jackson",
    "Martin",
    "Lee",
    "Perez",
    "Thompson",
    "White",
    "Harris",
    "Sanchez",
    "Clark",
    "Ramirez",
    "Lewis",
    "Robinson",
    "Walker",
    "Young",
    "Allen",
    "King",
    "Wright",
    "Scott",
    "Torres",
    "Nguyen",
    "Hill",
    "Flores",
    "Green",
    "Adams",
    "Nelson",
    "Baker",
    "Hall",
    "Rivera",
    "Campbell",
    "Mitchell",
    "Carter",
    "Roberts",
    "Turner",
    "Phillips",
    "Evans",
    "Parker",
    "Edwards",
]


def random_delay():
    time.sleep(random.randint(MIN_DELAY, MAX_DELAY) / 1000)


def generate_fingerprint() -> str:
    """Generate realistic browser fingerprint to avoid fraud detection"""
    # Realistic screen resolutions
    resolutions = [
        "1920x1080",
        "1366x768",
        "1536x864",
        "1440x900",
        "1280x720",
        "2560x1440",
    ]
    # Common timezones
    timezones = [-8, -7, -6, -5, -4, 0, 1, 2, 3, 5.5, 8, 9, 10]
    # Common languages
    languages = ["en-US", "en-GB", "en-CA", "en-AU", "es-ES", "fr-FR", "de-DE", "pt-BR"]
    # Common platforms
    platforms = ["Win32", "MacIntel", "Linux x86_64"]
    # Browser vendors
    vendors = ["Google Inc.", "Apple Computer, Inc.", ""]

    components = [
        str(int(time.time() * 1000)),
        str(random.random()),
        random.choice(resolutions),
        str(random.choice(timezones)),
        random.choice(languages),
        random.choice(platforms),
        random.choice(vendors),
        str(random.randint(1, 16)),  # hardware concurrency (CPU cores)
        str(random.randint(2, 32)),  # device memory GB
        str(random.randint(0, 1)),  # touch support
    ]
    return hashlib.md5("|".join(components).encode()).hexdigest()


def generate_name() -> Tuple[str, str]:
    return random.choice(FIRST_NAMES), random.choice(LAST_NAMES)


def generate_email(first: str, last: str, domain: str) -> str:
    patterns = [
        f"{first[0].lower()}{last.lower()}{random.randint(100, 999)}",
        f"{first.lower()}.{last.lower()}{random.randint(10, 99)}",
        f"{last.lower()}{first[0].lower()}{random.randint(100, 999)}",
    ]
    return f"{random.choice(patterns)}@{domain}"


def generate_birth_date() -> str:
    year = random.randint(2000, 2006)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    return f"{year}-{month:02d}-{day:02d}"


# ============ DOCUMENT GENERATOR ============
def generate_student_id(first: str, last: str, school: str) -> bytes:
    """Generate fake student ID card"""
    w, h = 650, 400
    img = Image.new("RGB", (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    try:
        font_lg = ImageFont.truetype("arial.ttf", 24)
        font_md = ImageFont.truetype("arial.ttf", 18)
        font_sm = ImageFont.truetype("arial.ttf", 14)
    except:
        font_lg = font_md = font_sm = ImageFont.load_default()

    # Header
    draw.rectangle([(0, 0), (w, 60)], fill=(0, 51, 102))
    draw.text(
        (w // 2, 30),
        "STUDENT IDENTIFICATION CARD",
        fill=(255, 255, 255),
        font=font_lg,
        anchor="mm",
    )

    # School
    draw.text((w // 2, 90), school[:50], fill=(0, 51, 102), font=font_md, anchor="mm")

    # Photo placeholder
    draw.rectangle([(30, 120), (150, 280)], outline=(180, 180, 180), width=2)
    draw.text((90, 200), "PHOTO", fill=(180, 180, 180), font=font_md, anchor="mm")

    # Info
    student_id = f"STU{random.randint(100000, 999999)}"
    y = 130
    for line in [
        f"Name: {first} {last}",
        f"ID: {student_id}",
        "Status: Full-time Student",
        "Major: Computer Science",
        f"Valid: {time.strftime('%Y')}-{int(time.strftime('%Y')) + 1}",
    ]:
        draw.text((175, y), line, fill=(51, 51, 51), font=font_md)
        y += 28

    # Footer
    draw.rectangle([(0, h - 40), (w, h)], fill=(0, 51, 102))
    draw.text(
        (w // 2, h - 20),
        "Property of University",
        fill=(255, 255, 255),
        font=font_sm,
        anchor="mm",
    )

    # Barcode
    for i in range(20):
        x = 480 + i * 7
        draw.rectangle(
            [(x, 280), (x + 3, 280 + random.randint(30, 50))], fill=(0, 0, 0)
        )

    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


# ============ VERIFIER ============
class SpotifyVerifier:
    """Spotify Student Verification with enhanced anti-detection"""

    def __init__(self, url: str, proxy: str = None):
        self.url = url
        self.vid = self._parse_id(url)
        self.fingerprint = generate_fingerprint()
        self.impersonate = None

        # Use enhanced anti-detection session
        if HAS_ANTI_DETECT:
            self.client, self.lib_name, self.impersonate = create_session(proxy)
            if self.impersonate:
                print(f"[INFO] TLS Fingerprint: Impersonating {self.impersonate}")

            # Warn about proxy type
            if proxy:
                proxy_type = check_proxy_type(proxy)
                if proxy_type == "datacenter":
                    print("[WARN] ⚠️  Datacenter proxy detected - may be blocked!")
        else:
            # Fallback to httpx (HIGH detection risk)
            proxy_url = None
            if proxy:
                if not proxy.startswith("http"):
                    proxy = f"http://{proxy}"
                proxy_url = proxy
            self.client = httpx.Client(timeout=30, proxy=proxy_url)
            self.lib_name = "httpx"
            print("[WARN] ❌ Using httpx without TLS spoofing - HIGH detection risk!")

        self.org = None

    def __del__(self):
        if hasattr(self, "client"):
            try:
                self.client.close()
            except:
                pass

    @staticmethod
    def _parse_id(url: str) -> Optional[str]:
        match = re.search(r"verificationId=([a-f0-9]+)", url, re.IGNORECASE)
        return match.group(1) if match else None

    def _request(
        self, method: str, endpoint: str, body: Dict = None
    ) -> Tuple[Dict, int]:
        random_delay()
        try:
            # Use anti-detect headers if available
            headers = (
                get_headers(for_sheerid=True)
                if HAS_ANTI_DETECT
                else {"Content-Type": "application/json"}
            )
            resp = self.client.request(
                method, f"{SHEERID_API_URL}{endpoint}", json=body, headers=headers
            )
            try:
                parsed = resp.json() if resp.text else {}
            except Exception:
                parsed = {"_text": resp.text}
            return parsed, resp.status_code
        except Exception as e:
            raise Exception(f"Request failed: {e}")

    def _upload_s3(self, url: str, data: bytes) -> bool:
        """Upload to S3 with multiple signature attempts for library compatibility"""
        signatures = [
            lambda: self.client.put(
                url, content=data, headers={"Content-Type": "image/png"}, timeout=60
            ),
            lambda: self.client.put(
                url, data=data, headers={"Content-Type": "image/png"}, timeout=60
            ),
            lambda: self.client.request(
                "PUT",
                url,
                content=data,
                headers={"Content-Type": "image/png"},
                timeout=60,
            ),
        ]

        last_exc = None
        for sig in signatures:
            try:
                resp = sig()
                if hasattr(resp, "status_code"):
                    if 200 <= resp.status_code < 300:
                        return True
                elif resp:
                    return True
            except TypeError as e:
                last_exc = e
                continue
            except Exception as e:
                last_exc = e
                continue

        print(f"     ❗ S3 upload failed. Last error: {last_exc}")
        return False

    def check_link(self) -> Dict:
        """Check if verification link is valid"""
        if not self.vid:
            return {"valid": False, "error": "Invalid URL"}

        data, status = self._request("GET", f"/verification/{self.vid}")
        if status != 200:
            return {"valid": False, "error": f"HTTP {status}"}

        step = data.get("currentStep", "")
        if step == "collectStudentPersonalInfo":
            return {"valid": True, "step": step}
        elif step == "success":
            return {"valid": False, "error": "Already verified"}
        return {"valid": False, "error": f"Invalid step: {step}"}

    def verify(self) -> Dict:
        """Run full verification"""
        if not self.vid:
            return {"success": False, "error": "Invalid verification URL"}

        try:
            # Generate info
            first, last = generate_name()
            self.org = select_university()
            email = generate_email(first, last, self.org["domain"])
            dob = generate_birth_date()

            print(f"\n   🎓 Student: {first} {last}")
            print(f"   📧 Email: {email}")
            print(f"   🏫 School: {self.org['name']}")
            print(f"   🎂 DOB: {dob}")
            print(f"   🔑 ID: {self.vid[:20]}...")

            # Step 1: Generate document
            print("\n   ▶ Step 1/3: Generating student ID...")
            doc = generate_student_id(first, last, self.org["name"])
            print(f"     📄 Size: {len(doc) / 1024:.1f} KB")

            # Step 2: Submit info
            print("   ▶ Step 2/3: Submitting student info...")
            body = {
                "firstName": first,
                "lastName": last,
                "birthDate": dob,
                "email": email,
                "phoneNumber": "",
                "organization": {
                    "id": self.org["id"],
                    "idExtended": self.org["idExtended"],
                    "name": self.org["name"],
                },
                "deviceFingerprintHash": self.fingerprint,
                "locale": "en-US",
                "metadata": {
                    "marketConsentValue": False,
                    "verificationId": self.vid,
                    "refererUrl": f"https://services.sheerid.com/verify/{PROGRAM_ID}/?verificationId={self.vid}",
                    "flags": '{"collect-info-step-email-first":"default","doc-upload-considerations":"default","doc-upload-may24":"default","doc-upload-redesign-use-legacy-message-keys":false,"docUpload-assertion-checklist":"default","font-size":"default","include-cvec-field-france-student":"not-labeled-optional"}',
                    "submissionOptIn": "By submitting the personal information above, I acknowledge that my personal information is being collected under the privacy policy of the business from which I am seeking a discount",
                },
            }

            data, status = self._request(
                "POST",
                f"/verification/{self.vid}/step/collectStudentPersonalInfo",
                body,
            )

            if status != 200:
                stats.record(self.org["name"], False)
                return {"success": False, "error": f"Submit failed: {status}"}

            if data.get("currentStep") == "error":
                error_ids = data.get("errorIds", [])
                # Check for fraud rejection
                if "fraudRulesReject" in str(error_ids):
                    if HAS_ANTI_DETECT:
                        handle_fraud_rejection(
                            retry_count=0,
                            error_payload=data,
                            message=f"University: {self.org['name']}",
                        )
                stats.record(self.org["name"], False)
                return {
                    "success": False,
                    "error": f"Error: {error_ids}",
                    "is_fraud_reject": "fraudRulesReject" in str(error_ids),
                }

            print(f"     📍 Current step: {data.get('currentStep')}")
            current_step = data.get("currentStep", "")

            # Step 3: Handle SSO step
            if current_step == "sso":
                print(
                    "   ⚠️  SSO step detected - data likely not in authoritative database"
                )
                print("   ▶ Step 3/4: Skipping SSO (will require document review)...")
                self._request("DELETE", f"/verification/{self.vid}/step/sso")
            elif current_step == "success":
                # Instant verification success!
                print("   ✅ Instant verification via authoritative data!")
                stats.record(self.org["name"], True)
                return {
                    "success": True,
                    "message": "Instant verification!",
                    "student": f"{first} {last}",
                    "email": email,
                    "school": self.org["name"],
                }

            # Step 4: Upload document
            print("   ▶ Step 4/5: Uploading document...")
            upload_body = {
                "files": [
                    {
                        "fileName": "student_card.png",
                        "mimeType": "image/png",
                        "fileSize": len(doc),
                    }
                ]
            }
            data, status = self._request(
                "POST", f"/verification/{self.vid}/step/docUpload", upload_body
            )

            if not data.get("documents"):
                stats.record(self.org["name"], False)
                return {"success": False, "error": "No upload URL"}

            upload_url = data["documents"][0].get("uploadUrl")
            if not self._upload_s3(upload_url, doc):
                stats.record(self.org["name"], False)
                return {"success": False, "error": "Upload failed"}

            print("     ✅ Document uploaded!")

            # Step 5: Complete document upload (PastKing logic)
            print("   ▶ Step 5/5: Completing upload...")
            data, status = self._request(
                "POST", f"/verification/{self.vid}/step/completeDocUpload"
            )
            final_step = data.get("currentStep", "unknown")
            print(f"     📍 Final step: {final_step}")

            # Determine actual verification status
            if final_step == "success":
                # Instant verification success (rare - authoritative database match)
                stats.record(self.org["name"], True)
                return {
                    "success": True,
                    "message": "Verified instantly! No review needed.",
                    "student": f"{first} {last}",
                    "email": email,
                    "school": self.org["name"],
                    "redirectUrl": data.get("redirectUrl"),
                }
            elif final_step == "pending":
                # Document submitted for manual/AI review - NOT verified yet
                # Don't record as success - actual result unknown until review completes
                return {
                    "success": False,
                    "pending": True,
                    "message": "Document submitted for review. Wait 24-48h for result.",
                    "student": f"{first} {last}",
                    "email": email,
                    "school": self.org["name"],
                }
            elif final_step in ["rejected", "error"]:
                stats.record(self.org["name"], False)
                error_ids = data.get("errorIds", [])
                return {
                    "success": False,
                    "error": f"Rejected: {error_ids}"
                    if error_ids
                    else "Document rejected",
                }
            else:
                # Unknown step - treat as pending
                return {
                    "success": False,
                    "pending": True,
                    "message": f"Unknown status: {final_step}. Check manually.",
                    "student": f"{first} {last}",
                    "email": email,
                    "school": self.org["name"],
                }

        except Exception as e:
            if self.org:
                stats.record(self.org["name"], False)
            return {"success": False, "error": str(e)}


# ============ MAIN ============
def main():
    import argparse

    parser = argparse.ArgumentParser(description="Spotify Student Verification Tool")
    parser.add_argument("url", nargs="?", help="Verification URL")
    parser.add_argument(
        "--proxy", help="Proxy server (host:port or http://user:pass@host:port)"
    )
    args = parser.parse_args()

    print()
    print("╔" + "═" * 56 + "╗")
    print("║" + " 🎵 Spotify Student Verification Tool".center(56) + "║")
    print("║" + " SheerID Student Discount".center(56) + "║")
    print("╚" + "═" * 56 + "╝")
    print()

    # Get URL
    if args.url:
        url = args.url
    else:
        url = input("   Enter verification URL: ").strip()

    if not url or "sheerid.com" not in url:
        print("\n   ❌ Invalid URL. Must contain sheerid.com")
        return

    # Show proxy info
    if args.proxy:
        print(f"   🔒 Using proxy: {args.proxy}")

    print("\n   ⏳ Processing...")

    verifier = SpotifyVerifier(url, proxy=args.proxy)

    # Check link first
    check = verifier.check_link()
    if not check.get("valid"):
        print(f"\n   ❌ Link Error: {check.get('error')}")
        return

    result = verifier.verify()

    print()
    print("─" * 58)
    if result.get("success"):
        print("   🎉 VERIFIED INSTANTLY!")
        print(f"   👤 {result.get('student')}")
        print(f"   📧 {result.get('email')}")
        print(f"   🏫 {result.get('school')}")
        print()
        print("   ✅ No review needed - verified via authoritative database!")
    elif result.get("pending"):
        print("   ⏳ SUBMITTED FOR REVIEW")
        print(f"   👤 {result.get('student')}")
        print(f"   📧 {result.get('email')}")
        print(f"   🏫 {result.get('school')}")
        print()
        print("   ⚠️  Document uploaded, waiting for review (24-48h)")
        print("   ⚠️  This is NOT a guaranteed success!")
    else:
        print(f"   ❌ FAILED: {result.get('error')}")
    print("─" * 58)

    stats.print_stats()


if __name__ == "__main__":
    main()
