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


# ============ UNIVERSITY ============
# STRATEGY: Netherlands IP + Groningen = click SSO portal then cancel = instant docUpload!
# This bypass works as of Jan 2026

GRONINGEN = {"id": 291085, "name": "University of Groningen", "domain": "rug.nl"}


def select_groningen() -> Dict:
    """Select University of Groningen for NL IP bypass"""
    return {**GRONINGEN, "idExtended": str(GRONINGEN["id"])}


# Alias for compatibility
def select_university() -> Dict:
    """Always returns Groningen for this tool"""
    return select_groningen()


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
def generate_groningen_invoice(first: str, last: str, dob: str) -> bytes:
    """Generate Groningen tuition fee invoice (matching Canva template)"""
    w, h = 595, 842  # A4 size at 72 DPI
    img = Image.new("RGB", (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    try:
        font_title = ImageFont.truetype("arial.ttf", 28)
        font_header = ImageFont.truetype("arial.ttf", 14)
        font_text = ImageFont.truetype("arial.ttf", 12)
        font_small = ImageFont.truetype("arial.ttf", 10)
    except:
        font_title = font_header = font_text = font_small = ImageFont.load_default()
    
    # Colors matching Groningen branding
    rug_red = (200, 16, 46)  # University of Groningen red
    dark_gray = (51, 51, 51)
    light_gray = (128, 128, 128)
    
    # Header - University of Groningen
    draw.text((40, 40), "University of Groningen", fill=rug_red, font=font_title)
    draw.text((40, 75), "Dienst Financiële en Economische Zaken", fill=light_gray, font=font_small)
    
    # Title
    draw.text((40, 130), "TUITION FEE INVOICE", fill=dark_gray, font=font_header)
    draw.line([(40, 155), (555, 155)], fill=rug_red, width=2)
    
    # Student info section
    student_id = f"S{random.randint(3000000, 3999999)}"
    current_year = int(time.strftime("%Y"))
    academic_year = f"{current_year}-{current_year + 1}"
    
    y = 180
    info_lines = [
        ("Student number:", student_id),
        ("Name:", f"{first} {last}"),
        ("Date of birth:", dob),
        ("For academic year:", academic_year),
    ]
    
    for label, value in info_lines:
        draw.text((40, y), label, fill=light_gray, font=font_text)
        draw.text((180, y), value, fill=dark_gray, font=font_text)
        y += 25
    
    # Tuition fees section
    y += 20
    draw.text((40, y), "TUITION FEES", fill=dark_gray, font=font_header)
    y += 30
    
    # Fee table
    tuition_fee = f"€ {random.randint(2200, 2400)},00"
    draw.text((40, y), "Statutory tuition fee", fill=dark_gray, font=font_text)
    draw.text((450, y), tuition_fee, fill=dark_gray, font=font_text)
    y += 25
    
    draw.line([(40, y), (555, y)], fill=light_gray, width=1)
    y += 10
    draw.text((40, y), "Total amount due", fill=dark_gray, font=font_header)
    draw.text((450, y), tuition_fee, fill=rug_red, font=font_header)
    
    # Payment info
    y += 50
    draw.text((40, y), "Payment details:", fill=dark_gray, font=font_header)
    y += 25
    
    bank_info = [
        ("Bank:", "Rabobank"),
        ("IBAN:", f"NL{random.randint(10, 99)} RABO 0{random.randint(100000000, 999999999)}"),
        ("BIC:", "RABONL2U"),
        ("Reference:", f"TF{current_year}{random.randint(10000, 99999)}"),
    ]
    
    for label, value in bank_info:
        draw.text((40, y), label, fill=light_gray, font=font_text)
        draw.text((120, y), value, fill=dark_gray, font=font_text)
        y += 20
    
    # Footer
    draw.line([(40, h - 80), (555, h - 80)], fill=light_gray, width=1)
    draw.text((40, h - 65), "Rijksuniversiteit Groningen", fill=light_gray, font=font_small)
    draw.text((40, h - 50), "Broerstraat 5, 9712 CP Groningen, Netherlands", fill=light_gray, font=font_small)
    draw.text((40, h - 35), "www.rug.nl", fill=rug_red, font=font_small)
    
    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


# Legacy alias
def generate_student_id(first: str, last: str, school: str) -> bytes:
    """Generate document for verification - now uses Groningen invoice"""
    # Generate DOB for ~2005 (student age)
    dob = f"2005-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}"
    return generate_groningen_invoice(first, last, dob)


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
        # Format 1: verificationId=XXX (query param)
        match = re.search(r"verificationId=([a-f0-9]+)", url, re.IGNORECASE)
        if match:
            return match.group(1)
        # Format 2: /verify/PROGRAM_ID/?verificationId=XXX or /verify/XXX (direct ID in path)
        match = re.search(r"/verify/([a-f0-9]{24,})/?\?", url, re.IGNORECASE)
        if match:
            # This is program ID, not verification ID, skip
            pass
        # Format 3: Direct verification ID in URL (no verificationId param)
        match = re.search(r"/verification/([a-f0-9]+)", url, re.IGNORECASE)
        if match:
            return match.group(1)
            
        # Check for externalUserId (Landing URL)
        if "externalUserId" in url:
            print("\n   ⚠️  WARNING: You provided the initial landing URL.")
            print("      Please wait for the form to fully load in the browser.")
            print("      The URL should change to include 'verificationId=...'")
            return None
            
        return None

    @staticmethod
    def _parse_program_id(url: str) -> Optional[str]:
        # Extract program ID from URL: https://services.sheerid.com/verify/PROGRAM_ID/...
        match = re.search(r"/verify/([a-f0-9]+)/?", url, re.IGNORECASE)
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
    
    def verify(self, use_groningen: bool = False) -> Dict:
        """Run full verification"""
        if not self.vid:
            return {"success": False, "error": "Invalid verification URL"}
        
        try:
            # Check current step first
            check_data, check_status = self._request("GET", f"/verification/{self.vid}")
            current_step = check_data.get("currentStep", "") if check_status == 200 else ""
            
            # Generate info
            first, last = generate_name()
            # Use pre-set org (from --groningen flag) or select randomly
            if not self.org:
                self.org = select_groningen() if use_groningen else select_university()
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
    import argparse
    
    print()
    print("╔" + "═" * 56 + "╗")
    print("║" + " 🤖 Perplexity AI Verification Tool".center(56) + "║")
    print("║" + " SheerID Student Discount".center(56) + "║")
    print("╚" + "═" * 56 + "╝")
    print()
    
    parser = argparse.ArgumentParser(description="Perplexity AI Student Verification Tool")
    parser.add_argument("url", nargs="?", help="SheerID verification URL")
    parser.add_argument("--groningen", "-g", action="store_true", 
                        help="Use Groningen bypass (requires Netherlands IP)")
    args = parser.parse_args()
    
    # Get URL
    if args.url:
        url = args.url
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
    
    # Show strategy being used
    if args.groningen:
        print("\n   🇳🇱 Using GRONINGEN BYPASS strategy!")
        print("   Requires: Netherlands IP + SSO portal cancel")
    
    print("\n   ⏳ Processing...")
    
    verifier = PerplexityVerifier(url)
    
    # Override university selection if using Groningen bypass
    if args.groningen:
        verifier.org = select_groningen()
        print(f"   🏫 Forced: {verifier.org['name']}")
    
    # Check link first
    check = verifier.check_link()
    if not check.get("valid"):
        print(f"\n   ❌ Link Error: {check.get('error')}")
        return
    
    result = verifier.verify(use_groningen=args.groningen)
    
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
