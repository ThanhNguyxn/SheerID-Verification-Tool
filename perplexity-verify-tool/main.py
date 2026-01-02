"""
Perplexity AI Student Verification Tool
SheerID Student Verification for Perplexity Pro

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
# Perplexity Program ID (will be parsed from URL usually, but this is a common one if needed)
# But we rely on the full URL passed by user
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
# NOTE: As of Jan 2026, new Perplexity student sign-ups are US-ONLY
# Other countries may work for existing users but new sign-ups restricted

UNIVERSITIES = [
    # =========== USA - HIGH PRIORITY ===========
    # These have highest success rates for new sign-ups
    {"id": 2565, "name": "Pennsylvania State University-Main Campus", "domain": "psu.edu", "weight": 100},
    {"id": 3499, "name": "University of California, Los Angeles", "domain": "ucla.edu", "weight": 98},
    {"id": 3491, "name": "University of California, Berkeley", "domain": "berkeley.edu", "weight": 97},
    {"id": 1953, "name": "Massachusetts Institute of Technology", "domain": "mit.edu", "weight": 95},
    {"id": 3113, "name": "Stanford University", "domain": "stanford.edu", "weight": 95},
    {"id": 2285, "name": "New York University", "domain": "nyu.edu", "weight": 96},
    {"id": 1426, "name": "Harvard University", "domain": "harvard.edu", "weight": 92},
    {"id": 590759, "name": "Yale University", "domain": "yale.edu", "weight": 90},
    {"id": 2626, "name": "Princeton University", "domain": "princeton.edu", "weight": 90},
    {"id": 698, "name": "Columbia University", "domain": "columbia.edu", "weight": 92},
    {"id": 3508, "name": "University of Chicago", "domain": "uchicago.edu", "weight": 88},
    {"id": 943, "name": "Duke University", "domain": "duke.edu", "weight": 88},
    {"id": 751, "name": "Cornell University", "domain": "cornell.edu", "weight": 90},
    {"id": 2420, "name": "Northwestern University", "domain": "northwestern.edu", "weight": 88},
    # More US Universities
    {"id": 3568, "name": "University of Michigan", "domain": "umich.edu", "weight": 95},
    {"id": 3686, "name": "University of Texas at Austin", "domain": "utexas.edu", "weight": 94},
    {"id": 1217, "name": "Georgia Institute of Technology", "domain": "gatech.edu", "weight": 93},
    {"id": 602, "name": "Carnegie Mellon University", "domain": "cmu.edu", "weight": 92},
    {"id": 3477, "name": "University of California, San Diego", "domain": "ucsd.edu", "weight": 93},
    {"id": 3600, "name": "University of North Carolina at Chapel Hill", "domain": "unc.edu", "weight": 90},
    {"id": 3645, "name": "University of Southern California", "domain": "usc.edu", "weight": 91},
    {"id": 3629, "name": "University of Pennsylvania", "domain": "upenn.edu", "weight": 90},
    {"id": 1603, "name": "Indiana University Bloomington", "domain": "iu.edu", "weight": 88},
    {"id": 2506, "name": "Ohio State University", "domain": "osu.edu", "weight": 90},
    {"id": 2700, "name": "Purdue University", "domain": "purdue.edu", "weight": 89},
    {"id": 3761, "name": "University of Washington", "domain": "uw.edu", "weight": 90},
    {"id": 3770, "name": "University of Wisconsin-Madison", "domain": "wisc.edu", "weight": 88},
    {"id": 3562, "name": "University of Maryland", "domain": "umd.edu", "weight": 87},
    {"id": 519, "name": "Boston University", "domain": "bu.edu", "weight": 86},
    {"id": 378, "name": "Arizona State University", "domain": "asu.edu", "weight": 92},
    {"id": 3521, "name": "University of Florida", "domain": "ufl.edu", "weight": 90},
    {"id": 3535, "name": "University of Illinois at Urbana-Champaign", "domain": "illinois.edu", "weight": 91},
    {"id": 3557, "name": "University of Minnesota Twin Cities", "domain": "umn.edu", "weight": 88},
    {"id": 3483, "name": "University of California, Davis", "domain": "ucdavis.edu", "weight": 89},
    {"id": 3487, "name": "University of California, Irvine", "domain": "uci.edu", "weight": 88},
    {"id": 3502, "name": "University of California, Santa Barbara", "domain": "ucsb.edu", "weight": 87},
    # Community Colleges (may have higher success)
    {"id": 2874, "name": "Santa Monica College", "domain": "smc.edu", "weight": 85},
    {"id": 2350, "name": "Northern Virginia Community College", "domain": "nvcc.edu", "weight": 84},
    
    # =========== OTHER COUNTRIES (Lower priority - may not work for new sign-ups) ===========
    # Canada
    {"id": 328355, "name": "University of Toronto", "domain": "utoronto.ca", "weight": 40},
    {"id": 328315, "name": "University of British Columbia", "domain": "ubc.ca", "weight": 38},
    # UK
    {"id": 273409, "name": "University of Oxford", "domain": "ox.ac.uk", "weight": 35},
    {"id": 273378, "name": "University of Cambridge", "domain": "cam.ac.uk", "weight": 35},
    # India (likely blocked for new sign-ups)
    {"id": 10007277, "name": "Indian Institute of Technology Delhi", "domain": "iitd.ac.in", "weight": 20},
    {"id": 3819983, "name": "University of Mumbai", "domain": "mu.ac.in", "weight": 15},
    # Australia
    {"id": 345301, "name": "The University of Melbourne", "domain": "unimelb.edu.au", "weight": 30},
    {"id": 345303, "name": "The University of Sydney", "domain": "sydney.edu.au", "weight": 28},
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
    
    # Add Perplexity specific watermark/style if needed
    # For now, generic student ID is fine
    
    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


# ============ VERIFIER ============
class PerplexityVerifier:
    """Perplexity Student Verification with enhanced features"""
    
    def __init__(self, url: str):
        self.url = url
        self.vid = self._parse_id(url)
        self.program_id = self._parse_program_id(url)
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

    @staticmethod
    def _parse_program_id(url: str) -> Optional[str]:
        # Extract program ID from URL: https://services.sheerid.com/verify/PROGRAM_ID/...
        match = re.search(r"/verify/([a-f0-9]+)/", url, re.IGNORECASE)
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
        # Accept multiple valid steps - handle re-upload after rejection
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
                        "refererUrl": f"https://services.sheerid.com/verify/{self.program_id}/?verificationId={self.vid}",
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
    print("║" + " 🤖 Perplexity AI Verification Tool".center(56) + "║")
    print("║" + " SheerID Student Discount".center(56) + "║")
    print("╚" + "═" * 56 + "╝")
    print()
    
    # Get URL
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        print("   💡 TIP: To get the verification URL:")
        print("   1. Go to Perplexity student verification page")
        print("   2. Open Console (F12)")
        print("   3. Run this code:")
        print("      console.log(Array.from(document.querySelectorAll('iframe, embed, object')).map(el => el.src || el.data).filter(src => src && src.includes('sheerid'))[0]);")
        print()
        url = input("   Enter verification URL: ").strip()
    
    if not url or "sheerid.com" not in url:
        print("\n   ❌ Invalid URL. Must contain sheerid.com")
        return
    
    print("\n   ⏳ Processing...")
    
    verifier = PerplexityVerifier(url)
    
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
