"""
Google One (Gemini) Student Verification Tool
SheerID Student Verification for Google One AI Premium

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


# ============ UNIVERSITIES WITH WEIGHTS (full 45 from JS data) ============
UNIVERSITIES = [
    # USA - Top Priority (Penn State - high success)
    {"id": 2565, "name": "Pennsylvania State University-Main Campus", "domain": "psu.edu", "weight": 100},
    # USA - Ivy League & Top Schools
    {"id": 1953, "name": "Massachusetts Institute of Technology", "domain": "mit.edu", "weight": 90},
    {"id": 1426, "name": "Harvard University", "domain": "harvard.edu", "weight": 85},
    {"id": 3113, "name": "Stanford University", "domain": "stanford.edu", "weight": 88},
    {"id": 3491, "name": "University of California, Berkeley", "domain": "berkeley.edu", "weight": 90},
    {"id": 590759, "name": "Yale University", "domain": "yale.edu", "weight": 82},
    {"id": 2626, "name": "Princeton University", "domain": "princeton.edu", "weight": 80},
    {"id": 698, "name": "Columbia University", "domain": "columbia.edu", "weight": 85},
    {"id": 2285, "name": "New York University", "domain": "nyu.edu", "weight": 88},
    {"id": 3499, "name": "University of California, Los Angeles", "domain": "ucla.edu", "weight": 92},
    {"id": 3508, "name": "University of Chicago", "domain": "uchicago.edu", "weight": 80},
    {"id": 943, "name": "Duke University", "domain": "duke.edu", "weight": 82},
    {"id": 751, "name": "Cornell University", "domain": "cornell.edu", "weight": 85},
    {"id": 2420, "name": "Northwestern University", "domain": "northwestern.edu", "weight": 82},
    # Canada
    {"id": 328355, "name": "University of Toronto", "domain": "utoronto.ca", "weight": 75},
    {"id": 4782066, "name": "McGill University", "domain": "mcgill.ca", "weight": 72},
    {"id": 328315, "name": "University of British Columbia", "domain": "ubc.ca", "weight": 74},
    # UK
    {"id": 273409, "name": "University of Oxford", "domain": "ox.ac.uk", "weight": 70},
    {"id": 273378, "name": "University of Cambridge", "domain": "cam.ac.uk", "weight": 70},
    {"id": 273294, "name": "Imperial College London", "domain": "imperial.ac.uk", "weight": 68},
    # India
    {"id": 10007277, "name": "Indian Institute of Technology Delhi", "domain": "iitd.ac.in", "weight": 72},
    {"id": 3819983, "name": "University of Mumbai", "domain": "mu.ac.in", "weight": 68},
    # Vietnam
    {"id": 588731, "name": "Hanoi University of Science and Technology", "domain": "hust.edu.vn", "weight": 95},
    {"id": 10066238, "name": "VNU University of Engineering and Technology", "domain": "uet.vnu.edu.vn", "weight": 90},
    {"id": 588738, "name": "VNU University of Information Technology", "domain": "uit.edu.vn", "weight": 88},
    {"id": 588772, "name": "FPT University", "domain": "fpt.edu.vn", "weight": 92},
    {"id": 588608, "name": "Posts and Telecommunications Institute of Technology", "domain": "ptit.edu.vn", "weight": 85},
    {"id": 10492794, "name": "VNU University of Science", "domain": "hus.vnu.edu.vn", "weight": 85},
    # Japan
    {"id": 354085, "name": "The University of Tokyo", "domain": "u-tokyo.ac.jp", "weight": 70},
    {"id": 353961, "name": "Kyoto University", "domain": "kyoto-u.ac.jp", "weight": 68},
    # South Korea
    {"id": 356569, "name": "Seoul National University", "domain": "snu.ac.kr", "weight": 72},
    {"id": 356632, "name": "Yonsei University", "domain": "yonsei.ac.kr", "weight": 70},
    {"id": 356431, "name": "Korea University", "domain": "korea.ac.kr", "weight": 68},
    # Germany
    {"id": 10011178, "name": "Technical University of Munich", "domain": "tum.de", "weight": 72},
    {"id": 344450, "name": "Ludwig Maximilian University of Munich", "domain": "lmu.de", "weight": 70},
    # France
    {"id": 329766, "name": "Ecole Polytechnique", "domain": "polytechnique.edu", "weight": 68},
    {"id": 10148649, "name": "PSL Research University", "domain": "psl.eu", "weight": 66},
    # Singapore
    {"id": 356355, "name": "National University of Singapore", "domain": "nus.edu.sg", "weight": 72},
    {"id": 356356, "name": "Nanyang Technological University", "domain": "ntu.edu.sg", "weight": 70},
    # China
    {"id": 3852634, "name": "Tsinghua University", "domain": "tsinghua.edu.cn", "weight": 72},
    {"id": 3852964, "name": "Peking University", "domain": "pku.edu.cn", "weight": 70},
    {"id": 3853298, "name": "Fudan University", "domain": "fudan.edu.cn", "weight": 68},
    # Brazil
    {"id": 10042652, "name": "University of Sao Paulo", "domain": "usp.br", "weight": 65},
    {"id": 10059316, "name": "University of Campinas", "domain": "unicamp.br", "weight": 63},
    {"id": 412760, "name": "Federal University of Rio de Janeiro", "domain": "ufrj.br", "weight": 62},
    # Australia
    {"id": 345301, "name": "The University of Melbourne", "domain": "unimelb.edu.au", "weight": 68},
    {"id": 345276, "name": "Australian National University", "domain": "anu.edu.au", "weight": 66},
    {"id": 345303, "name": "The University of Sydney", "domain": "sydney.edu.au", "weight": 66},
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
class GeminiVerifier:
    """Gemini Student Verification with enhanced features"""
    
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
            print(f"     📄 Size: {len(doc)/1024:.1f} KB")
            
            # Step 2: Submit info
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
    print("║" + " 🤖 Google One (Gemini) Verification Tool".center(56) + "║")
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
    
    verifier = GeminiVerifier(url)
    
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
