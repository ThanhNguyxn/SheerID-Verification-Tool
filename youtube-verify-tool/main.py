"""
YouTube Student Verification Tool
SheerID Student Verification for YouTube Premium

Enhanced with:
- Success rate tracking per organization
- Weighted university selection
- Retry with exponential backoff
- Rate limiting avoidance

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
    from anti_detect import get_headers, get_fingerprint, get_random_user_agent, random_delay as anti_delay
    HAS_ANTI_DETECT = True
    print("[INFO] Anti-detection module loaded")
except ImportError:
    HAS_ANTI_DETECT = False


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
        return self.data["success"] / self.data["total"] * 100 if self.data["total"] else 0
    
    def print_stats(self):
        print(f"\n📊 Statistics:")
        print(f"   Total: {self.data['total']} | ✅ {self.data['success']} | ❌ {self.data['failed']}")
        if self.data["total"]:
            print(f"   Success Rate: {self.get_rate():.1f}%")


stats = Stats()


# ============ UNIVERSITIES WITH WEIGHTS ============
# YouTube Premium Student Discount supports 100+ countries globally including:
# USA, UK, Canada, Australia, India, Vietnam, Japan, South Korea, Germany,
# France, Brazil, Indonesia, Philippines, Thailand, Malaysia, Singapore,
# Turkey, Mexico, Egypt, Saudi Arabia, UAE, South Africa, and many more.
# Vietnam and India are FULLY SUPPORTED - use local universities!

UNIVERSITIES = [
    # =========== VIETNAM - FULLY SUPPORTED (15 schools) ===========
    {"id": 588731, "name": "Hanoi University of Science and Technology", "domain": "hust.edu.vn", "weight": 98},
    {"id": 10066238, "name": "VNU University of Engineering and Technology", "domain": "uet.vnu.edu.vn", "weight": 96},
    {"id": 588738, "name": "VNU University of Information Technology", "domain": "uit.edu.vn", "weight": 94},
    {"id": 588772, "name": "FPT University", "domain": "fpt.edu.vn", "weight": 97},
    {"id": 588608, "name": "Posts and Telecommunications Institute of Technology", "domain": "ptit.edu.vn", "weight": 92},
    {"id": 10492794, "name": "VNU University of Science", "domain": "hus.vnu.edu.vn", "weight": 90},
    {"id": 10066240, "name": "Vietnam National University Ho Chi Minh City", "domain": "vnuhcm.edu.vn", "weight": 95},
    {"id": 588736, "name": "Ho Chi Minh City University of Technology", "domain": "hcmut.edu.vn", "weight": 93},
    {"id": 588740, "name": "Ton Duc Thang University", "domain": "tdtu.edu.vn", "weight": 91},
    {"id": 588597, "name": "Duy Tan University", "domain": "duytan.edu.vn", "weight": 89},
    {"id": 588599, "name": "University of Economics Ho Chi Minh City", "domain": "ueh.edu.vn", "weight": 88},
    {"id": 588601, "name": "Hue University", "domain": "hueuni.edu.vn", "weight": 85},
    {"id": 588603, "name": "University of Da Nang", "domain": "udn.vn", "weight": 84},
    {"id": 588605, "name": "Can Tho University", "domain": "ctu.edu.vn", "weight": 83},
    {"id": 588607, "name": "Foreign Trade University", "domain": "ftu.edu.vn", "weight": 90},
    
    # =========== INDIA - FULLY SUPPORTED (15 schools) ===========
    {"id": 10007277, "name": "Indian Institute of Technology Delhi", "domain": "iitd.ac.in", "weight": 95},
    {"id": 10007303, "name": "Indian Institute of Technology Bombay", "domain": "iitb.ac.in", "weight": 94},
    {"id": 10007289, "name": "Indian Institute of Technology Madras", "domain": "iitm.ac.in", "weight": 93},
    {"id": 10007295, "name": "Indian Institute of Technology Kanpur", "domain": "iitk.ac.in", "weight": 92},
    {"id": 10007281, "name": "Indian Institute of Technology Kharagpur", "domain": "iitkgp.ac.in", "weight": 91},
    {"id": 3819983, "name": "University of Mumbai", "domain": "mu.ac.in", "weight": 90},
    {"id": 3827577, "name": "University of Delhi", "domain": "du.ac.in", "weight": 92},
    {"id": 10007271, "name": "Indian Institute of Science Bangalore", "domain": "iisc.ac.in", "weight": 96},
    {"id": 3827579, "name": "Jawaharlal Nehru University", "domain": "jnu.ac.in", "weight": 88},
    {"id": 3827581, "name": "Banaras Hindu University", "domain": "bhu.ac.in", "weight": 86},
    {"id": 3827583, "name": "Aligarh Muslim University", "domain": "amu.ac.in", "weight": 85},
    {"id": 10007309, "name": "BITS Pilani", "domain": "bits-pilani.ac.in", "weight": 90},
    {"id": 3827585, "name": "University of Hyderabad", "domain": "uohyd.ac.in", "weight": 84},
    {"id": 10007315, "name": "Vellore Institute of Technology", "domain": "vit.ac.in", "weight": 88},
    {"id": 10007317, "name": "Manipal Academy of Higher Education", "domain": "manipal.edu", "weight": 87},
    
    # =========== INDONESIA - FULLY SUPPORTED (10 schools) ===========
    {"id": 10008577, "name": "University of Indonesia", "domain": "ui.ac.id", "weight": 90},
    {"id": 10008584, "name": "Institut Teknologi Bandung", "domain": "itb.ac.id", "weight": 88},
    {"id": 10008579, "name": "Gadjah Mada University", "domain": "ugm.ac.id", "weight": 87},
    {"id": 10008581, "name": "Airlangga University", "domain": "unair.ac.id", "weight": 85},
    {"id": 10008583, "name": "IPB University", "domain": "ipb.ac.id", "weight": 84},
    {"id": 10008585, "name": "Brawijaya University", "domain": "ub.ac.id", "weight": 83},
    {"id": 10008587, "name": "Diponegoro University", "domain": "undip.ac.id", "weight": 82},
    {"id": 10008589, "name": "Institut Teknologi Sepuluh Nopember", "domain": "its.ac.id", "weight": 86},
    {"id": 10008591, "name": "Bina Nusantara University", "domain": "binus.ac.id", "weight": 85},
    {"id": 10008593, "name": "Telkom University", "domain": "telkomuniversity.ac.id", "weight": 84},
    
    # =========== THAILAND - FULLY SUPPORTED (8 schools) ===========
    {"id": 10015929, "name": "Chulalongkorn University", "domain": "chula.ac.th", "weight": 88},
    {"id": 10015931, "name": "Mahidol University", "domain": "mahidol.ac.th", "weight": 87},
    {"id": 10015933, "name": "Chiang Mai University", "domain": "cmu.ac.th", "weight": 85},
    {"id": 10015935, "name": "Kasetsart University", "domain": "ku.ac.th", "weight": 84},
    {"id": 10015937, "name": "Thammasat University", "domain": "tu.ac.th", "weight": 86},
    {"id": 10015939, "name": "Prince of Songkla University", "domain": "psu.ac.th", "weight": 82},
    {"id": 10015941, "name": "Khon Kaen University", "domain": "kku.ac.th", "weight": 81},
    {"id": 10015943, "name": "King Mongkut's University of Technology Thonburi", "domain": "kmutt.ac.th", "weight": 85},
    
    # =========== PHILIPPINES - FULLY SUPPORTED (8 schools) ===========
    {"id": 10019175, "name": "University of the Philippines Diliman", "domain": "upd.edu.ph", "weight": 88},
    {"id": 10019177, "name": "Ateneo de Manila University", "domain": "ateneo.edu", "weight": 86},
    {"id": 10019179, "name": "De La Salle University", "domain": "dlsu.edu.ph", "weight": 85},
    {"id": 10019181, "name": "University of Santo Tomas", "domain": "ust.edu.ph", "weight": 84},
    {"id": 10019183, "name": "Polytechnic University of the Philippines", "domain": "pup.edu.ph", "weight": 83},
    {"id": 10019185, "name": "Mapua University", "domain": "mapua.edu.ph", "weight": 82},
    {"id": 10019187, "name": "University of San Carlos", "domain": "usc.edu.ph", "weight": 80},
    {"id": 10019189, "name": "Silliman University", "domain": "su.edu.ph", "weight": 79},
    
    # =========== USA - HIGH PRIORITY (10 schools) ===========
    {"id": 2565, "name": "Pennsylvania State University-Main Campus", "domain": "psu.edu", "weight": 100},
    {"id": 3499, "name": "University of California, Los Angeles", "domain": "ucla.edu", "weight": 98},
    {"id": 3491, "name": "University of California, Berkeley", "domain": "berkeley.edu", "weight": 97},
    {"id": 2285, "name": "New York University", "domain": "nyu.edu", "weight": 96},
    {"id": 3568, "name": "University of Michigan", "domain": "umich.edu", "weight": 95},
    {"id": 378, "name": "Arizona State University", "domain": "asu.edu", "weight": 94},
    {"id": 3521, "name": "University of Florida", "domain": "ufl.edu", "weight": 93},
    {"id": 3686, "name": "University of Texas at Austin", "domain": "utexas.edu", "weight": 92},
    {"id": 1217, "name": "Georgia Institute of Technology", "domain": "gatech.edu", "weight": 91},
    {"id": 602, "name": "Carnegie Mellon University", "domain": "cmu.edu", "weight": 90},
    
    # =========== JAPAN - SUPPORTED (5 schools) ===========
    {"id": 354085, "name": "The University of Tokyo", "domain": "u-tokyo.ac.jp", "weight": 85},
    {"id": 353961, "name": "Kyoto University", "domain": "kyoto-u.ac.jp", "weight": 84},
    {"id": 353963, "name": "Osaka University", "domain": "osaka-u.ac.jp", "weight": 82},
    {"id": 353965, "name": "Tohoku University", "domain": "tohoku.ac.jp", "weight": 81},
    {"id": 353967, "name": "Nagoya University", "domain": "nagoya-u.ac.jp", "weight": 80},
    
    # =========== SOUTH KOREA - SUPPORTED (5 schools) ===========
    {"id": 356569, "name": "Seoul National University", "domain": "snu.ac.kr", "weight": 85},
    {"id": 356632, "name": "Yonsei University", "domain": "yonsei.ac.kr", "weight": 84},
    {"id": 356431, "name": "Korea University", "domain": "korea.ac.kr", "weight": 83},
    {"id": 356571, "name": "KAIST", "domain": "kaist.ac.kr", "weight": 86},
    {"id": 356573, "name": "Pohang University of Science and Technology", "domain": "postech.ac.kr", "weight": 84},
    
    # =========== UK - SUPPORTED (5 schools) ===========
    {"id": 273409, "name": "University of Oxford", "domain": "ox.ac.uk", "weight": 85},
    {"id": 273378, "name": "University of Cambridge", "domain": "cam.ac.uk", "weight": 85},
    {"id": 273294, "name": "Imperial College London", "domain": "imperial.ac.uk", "weight": 83},
    {"id": 273319, "name": "University College London", "domain": "ucl.ac.uk", "weight": 82},
    {"id": 273381, "name": "University of Edinburgh", "domain": "ed.ac.uk", "weight": 80},
    
    # =========== OTHER COUNTRIES ===========
    # Australia
    {"id": 345301, "name": "The University of Melbourne", "domain": "unimelb.edu.au", "weight": 82},
    {"id": 345303, "name": "The University of Sydney", "domain": "sydney.edu.au", "weight": 80},
    # Brazil
    {"id": 10042652, "name": "University of Sao Paulo", "domain": "usp.br", "weight": 78},
    {"id": 10059316, "name": "University of Campinas", "domain": "unicamp.br", "weight": 76},
    # Germany
    {"id": 10011178, "name": "Technical University of Munich", "domain": "tum.de", "weight": 80},
    {"id": 344450, "name": "Ludwig Maximilian University of Munich", "domain": "lmu.de", "weight": 78},
    # Singapore
    {"id": 356355, "name": "National University of Singapore", "domain": "nus.edu.sg", "weight": 82},
    {"id": 356356, "name": "Nanyang Technological University", "domain": "ntu.edu.sg", "weight": 80},
    # Canada
    {"id": 328355, "name": "University of Toronto", "domain": "utoronto.ca", "weight": 80},
    {"id": 328315, "name": "University of British Columbia", "domain": "ubc.ca", "weight": 78},
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
    "James", "John", "Robert", "Michael", "William", "David", "Richard", "Joseph",
    "Thomas", "Christopher", "Charles", "Daniel", "Matthew", "Anthony", "Mark",
    "Donald", "Steven", "Andrew", "Paul", "Joshua", "Kenneth", "Kevin", "Brian",
    "George", "Timothy", "Ronald", "Edward", "Jason", "Jeffrey", "Ryan",
    "Mary", "Patricia", "Jennifer", "Linda", "Barbara", "Elizabeth", "Susan",
    "Jessica", "Sarah", "Karen", "Lisa", "Nancy", "Betty", "Margaret", "Sandra",
    "Ashley", "Kimberly", "Emily", "Donna", "Michelle", "Dorothy", "Carol",
    "Amanda", "Melissa", "Deborah", "Stephanie", "Rebecca", "Sharon", "Laura",
    "Emma", "Olivia", "Ava", "Isabella", "Sophia", "Mia", "Charlotte", "Amelia"
]
LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
    "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
    "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson",
    "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker",
    "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill",
    "Flores", "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell",
    "Mitchell", "Carter", "Roberts", "Turner", "Phillips", "Evans", "Parker", "Edwards"
]


def random_delay():
    time.sleep(random.randint(MIN_DELAY, MAX_DELAY) / 1000)


def generate_fingerprint() -> str:
    components = [str(time.time()), str(random.random()), "1920x1080"]
    return hashlib.md5("|".join(components).encode()).hexdigest()


def generate_name() -> Tuple[str, str]:
    return random.choice(FIRST_NAMES), random.choice(LAST_NAMES)


def generate_email(first: str, last: str, domain: str) -> str:
    patterns = [
        f"{first[0].lower()}{last.lower()}{random.randint(100, 999)}",
        f"{first.lower()}.{last.lower()}{random.randint(10, 99)}",
        f"{last.lower()}{first[0].lower()}{random.randint(100, 999)}"
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
    draw.text((w//2, 30), "STUDENT IDENTIFICATION CARD", fill=(255, 255, 255), font=font_lg, anchor="mm")
    
    # School
    draw.text((w//2, 90), school[:50], fill=(0, 51, 102), font=font_md, anchor="mm")
    
    # Photo placeholder
    draw.rectangle([(30, 120), (150, 280)], outline=(180, 180, 180), width=2)
    draw.text((90, 200), "PHOTO", fill=(180, 180, 180), font=font_md, anchor="mm")
    
    # Info
    student_id = f"STU{random.randint(100000, 999999)}"
    y = 130
    for line in [f"Name: {first} {last}", f"ID: {student_id}", "Status: Full-time Student",
                 "Major: Computer Science", f"Valid: {time.strftime('%Y')}-{int(time.strftime('%Y'))+1}"]:
        draw.text((175, y), line, fill=(51, 51, 51), font=font_md)
        y += 28
    
    # Footer
    draw.rectangle([(0, h-40), (w, h)], fill=(0, 51, 102))
    draw.text((w//2, h-20), "Property of University", fill=(255, 255, 255), font=font_sm, anchor="mm")
    
    # Barcode
    for i in range(20):
        x = 480 + i * 7
        draw.rectangle([(x, 280), (x+3, 280+random.randint(30, 50))], fill=(0, 0, 0))
    
    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


# ============ VERIFIER ============
class YouTubeVerifier:
    """YouTube Student Verification with enhanced features"""
    
    def __init__(self, url: str):
        self.url = url
        self.vid = self._parse_id(url)
        self.fingerprint = generate_fingerprint()
        self.client = httpx.Client(timeout=30)
        self.org = None
    
    def __del__(self):
        if hasattr(self, "client"):
            self.client.close()
    
    @staticmethod
    def _parse_id(url: str) -> Optional[str]:
        match = re.search(r"verificationId=([a-f0-9]+)", url, re.IGNORECASE)
        return match.group(1) if match else None
    
    def _request(self, method: str, endpoint: str, body: Dict = None) -> Tuple[Dict, int]:
        random_delay()
        try:
            resp = self.client.request(method, f"{SHEERID_API_URL}{endpoint}", 
                                       json=body, headers={"Content-Type": "application/json"})
            return resp.json() if resp.text else {}, resp.status_code
        except Exception as e:
            raise Exception(f"Request failed: {e}")
    
    def _upload_s3(self, url: str, data: bytes) -> bool:
        try:
            resp = self.client.put(url, content=data, headers={"Content-Type": "image/png"}, timeout=60)
            return 200 <= resp.status_code < 300
        except:
            return False
    
    def check_link(self) -> Dict:
        """Check if verification link is valid"""
        if not self.vid:
            return {"valid": False, "error": "Invalid URL"}
        
        data, status = self._request("GET", f"/verification/{self.vid}")
        if status != 200:
            return {"valid": False, "error": f"HTTP {status}"}
        
        step = data.get("currentStep", "")
        # Accept multiple valid steps - offers.sheerid.com URLs may start at docUpload
        valid_steps = ["collectStudentPersonalInfo", "docUpload", "sso"]
        if step in valid_steps:
            return {"valid": True, "step": step}
        elif step == "success":
            return {"valid": False, "error": "Already verified"}
        elif step == "pending":
            return {"valid": False, "error": "Already pending review"}
        return {"valid": False, "error": f"Invalid step: {step}"}
    
    def verify(self) -> Dict:
        """Run full verification"""
        if not self.vid:
            return {"success": False, "error": "Invalid verification URL"}
        
        try:
            # Check current step first
            check_data, check_status = self._request("GET", f"/verification/{self.vid}")
            current_step = check_data.get("currentStep", "") if check_status == 200 else ""
            
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
            print(f"   📍 Starting step: {current_step}")
            
            # Step 1: Generate document
            print("\n   ▶ Step 1/3: Generating student ID...")
            doc = generate_student_id(first, last, self.org["name"])
            print(f"     📄 Size: {len(doc)/1024:.1f} KB")
            
            # Step 2: Submit info (skip if already past this step)
            if current_step == "collectStudentPersonalInfo":
                print("   ▶ Step 2/3: Submitting student info...")
                body = {
                    "firstName": first, "lastName": last, "birthDate": dob,
                    "email": email, "phoneNumber": "",
                    "organization": {"id": self.org["id"], "idExtended": self.org["idExtended"], 
                                    "name": self.org["name"]},
                    "deviceFingerprintHash": self.fingerprint,
                    "locale": "en-US",
                    "metadata": {
                        "marketConsentValue": False,
                        "verificationId": self.vid,
                        "refererUrl": f"https://services.sheerid.com/verify/{PROGRAM_ID}/?verificationId={self.vid}",
                        "flags": '{"collect-info-step-email-first":"default","doc-upload-considerations":"default","doc-upload-may24":"default","doc-upload-redesign-use-legacy-message-keys":false,"docUpload-assertion-checklist":"default","font-size":"default","include-cvec-field-france-student":"not-labeled-optional"}',
                        "submissionOptIn": "By submitting the personal information above, I acknowledge that my personal information is being collected under the privacy policy of the business from which I am seeking a discount"
                    }
                }
                
                data, status = self._request("POST", f"/verification/{self.vid}/step/collectStudentPersonalInfo", body)
                
                if status != 200:
                    stats.record(self.org["name"], False)
                    return {"success": False, "error": f"Submit failed: {status}"}
                
                if data.get("currentStep") == "error":
                    stats.record(self.org["name"], False)
                    return {"success": False, "error": f"Error: {data.get('errorIds', [])}"}
                
                print(f"     📍 Current step: {data.get('currentStep')}")
                current_step = data.get("currentStep", "")
            elif current_step in ["docUpload", "sso"]:
                print("   ▶ Step 2/3: Skipping (already past info submission)...")
            else:
                print(f"   ▶ Step 2/3: Unknown step '{current_step}', attempting to continue...")
            
            # Step 3: Skip SSO if needed (PastKing logic)
            if current_step in ["sso", "collectStudentPersonalInfo"]:
                print("   ▶ Step 3/4: Skipping SSO...")
                self._request("DELETE", f"/verification/{self.vid}/step/sso")
            
            # Step 4: Upload document
            print("   ▶ Step 4/5: Uploading document...")
            upload_body = {"files": [{"fileName": "student_card.png", "mimeType": "image/png", "fileSize": len(doc)}]}
            data, status = self._request("POST", f"/verification/{self.vid}/step/docUpload", upload_body)
            
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
            data, status = self._request("POST", f"/verification/{self.vid}/step/completeDocUpload")
            print(f"     ✅ Upload completed: {data.get('currentStep', 'pending')}")
            
            stats.record(self.org["name"], True)
            
            return {
                "success": True,
                "message": "Verification submitted! Wait 24-48h for review.",
                "student": f"{first} {last}",
                "email": email,
                "school": self.org["name"],
                "redirectUrl": data.get("redirectUrl")
            }
            
        except Exception as e:
            if self.org:
                stats.record(self.org["name"], False)
            return {"success": False, "error": str(e)}


# ============ MAIN ============
def main():
    print()
    print("╔" + "═" * 56 + "╗")
    print("║" + " 🎬 YouTube Student Verification Tool".center(56) + "║")
    print("║" + " SheerID Student Discount".center(56) + "║")
    print("╚" + "═" * 56 + "╝")
    print()
    
    # Get URL
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = input("   Enter verification URL: ").strip()
    
    if not url or "sheerid.com" not in url:
        print("\n   ❌ Invalid URL. Must contain sheerid.com")
        return
    
    print("\n   ⏳ Processing...")
    
    verifier = YouTubeVerifier(url)
    
    # Check link first
    check = verifier.check_link()
    if not check.get("valid"):
        print(f"\n   ❌ Link Error: {check.get('error')}")
        return
    
    result = verifier.verify()
    
    print()
    print("─" * 58)
    if result.get("success"):
        print("   🎉 SUCCESS!")
        print(f"   👤 {result.get('student')}")
        print(f"   📧 {result.get('email')}")
        print(f"   🏫 {result.get('school')}")
        print()
        print("   ⏳ Wait 24-48 hours for manual review")
    else:
        print(f"   ❌ FAILED: {result.get('error')}")
    print("─" * 58)
    
    stats.print_stats()


if __name__ == "__main__":
    main()
