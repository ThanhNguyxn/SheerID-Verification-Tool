"""
Bolt.new Teacher Verification Tool
SheerID Teacher Verification for Bolt.new

Written from scratch based on SheerID API flow
Author: ThanhNguyxn
"""

import os
import re
import sys
import json
import time
import random
import hashlib
import base64
from pathlib import Path
from io import BytesIO
from typing import Dict, Optional, Tuple

try:
    import httpx
except ImportError:
    print("Error: httpx required. Install: pip install httpx")
    sys.exit(1)

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("Error: Pillow required. Install: pip install Pillow")
    sys.exit(1)

# Import anti-detection module
try:
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from anti_detect import get_headers, get_fingerprint, get_random_user_agent
    HAS_ANTI_DETECT = True
    print("[INFO] Anti-detection module loaded")
except ImportError:
    HAS_ANTI_DETECT = False

# ============ CONFIG ============
PROGRAM_ID = "68cc6a2e64f55220de204448"
SHEERID_BASE_URL = "https://services.sheerid.com"

# Universities with weights (teacher verification uses these)
# Bolt.new teacher discount is available globally
UNIVERSITIES = [
    # USA - High Priority
    {"id": 2565, "name": "Pennsylvania State University-Main Campus", "domain": "psu.edu", "weight": 100},
    {"id": 3499, "name": "University of California, Los Angeles", "domain": "ucla.edu", "weight": 98},
    {"id": 3491, "name": "University of California, Berkeley", "domain": "berkeley.edu", "weight": 97},
    {"id": 1953, "name": "Massachusetts Institute of Technology", "domain": "mit.edu", "weight": 95},
    {"id": 3113, "name": "Stanford University", "domain": "stanford.edu", "weight": 95},
    {"id": 2285, "name": "New York University", "domain": "nyu.edu", "weight": 94},
    {"id": 1426, "name": "Harvard University", "domain": "harvard.edu", "weight": 92},
    {"id": 698, "name": "Columbia University", "domain": "columbia.edu", "weight": 92},
    {"id": 3568, "name": "University of Michigan", "domain": "umich.edu", "weight": 93},
    {"id": 3686, "name": "University of Texas at Austin", "domain": "utexas.edu", "weight": 92},
    {"id": 1217, "name": "Georgia Institute of Technology", "domain": "gatech.edu", "weight": 91},
    {"id": 602, "name": "Carnegie Mellon University", "domain": "cmu.edu", "weight": 90},
    {"id": 751, "name": "Cornell University", "domain": "cornell.edu", "weight": 90},
    {"id": 2420, "name": "Northwestern University", "domain": "northwestern.edu", "weight": 88},
    {"id": 378, "name": "Arizona State University", "domain": "asu.edu", "weight": 91},
    # Canada
    {"id": 328355, "name": "University of Toronto", "domain": "utoronto.ca", "weight": 85},
    {"id": 4782066, "name": "McGill University", "domain": "mcgill.ca", "weight": 82},
    {"id": 328315, "name": "University of British Columbia", "domain": "ubc.ca", "weight": 84},
    # UK
    {"id": 273409, "name": "University of Oxford", "domain": "ox.ac.uk", "weight": 85},
    {"id": 273378, "name": "University of Cambridge", "domain": "cam.ac.uk", "weight": 85},
    {"id": 273294, "name": "Imperial College London", "domain": "imperial.ac.uk", "weight": 82},
    {"id": 273319, "name": "University College London", "domain": "ucl.ac.uk", "weight": 80},
    # Germany
    {"id": 10011178, "name": "Technical University of Munich", "domain": "tum.de", "weight": 82},
    {"id": 344450, "name": "Ludwig Maximilian University of Munich", "domain": "lmu.de", "weight": 80},
    # Australia
    {"id": 345301, "name": "The University of Melbourne", "domain": "unimelb.edu.au", "weight": 82},
    {"id": 345303, "name": "The University of Sydney", "domain": "sydney.edu.au", "weight": 80},
    # Japan
    {"id": 354085, "name": "The University of Tokyo", "domain": "u-tokyo.ac.jp", "weight": 80},
    {"id": 353961, "name": "Kyoto University", "domain": "kyoto-u.ac.jp", "weight": 78},
    # Singapore
    {"id": 356355, "name": "National University of Singapore", "domain": "nus.edu.sg", "weight": 82},
    {"id": 356356, "name": "Nanyang Technological University", "domain": "ntu.edu.sg", "weight": 80},
]


def select_university():
    """Weighted random selection of university"""
    weights = [u["weight"] for u in UNIVERSITIES]
    total = sum(weights)
    r = random.uniform(0, total)
    cumulative = 0
    for uni in UNIVERSITIES:
        cumulative += uni["weight"]
        if r <= cumulative:
            return {"id": uni["id"], "idExtended": str(uni["id"]), "name": uni["name"], "domain": uni["domain"]}
    return {"id": UNIVERSITIES[0]["id"], "idExtended": str(UNIVERSITIES[0]["id"]), "name": UNIVERSITIES[0]["name"], "domain": UNIVERSITIES[0]["domain"]}

# ============ NAME GENERATOR ============
FIRST_NAMES = [
    # Male names
    "James", "John", "Robert", "Michael", "William", "David", "Richard", "Joseph",
    "Thomas", "Christopher", "Charles", "Daniel", "Matthew", "Anthony", "Mark",
    "Donald", "Steven", "Andrew", "Paul", "Joshua", "Kenneth", "Kevin", "Brian",
    "George", "Timothy", "Ronald", "Edward", "Jason", "Jeffrey", "Ryan",
    "Jacob", "Nicholas", "Eric", "Jonathan", "Stephen", "Larry", "Justin", "Scott",
    # Female names
    "Mary", "Patricia", "Jennifer", "Linda", "Elizabeth", "Barbara", "Susan",
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
    "Mitchell", "Carter", "Roberts", "Turner", "Phillips", "Evans", "Parker", "Edwards",
    "Collins", "Stewart", "Morris", "Murphy", "Cook", "Rogers", "Morgan", "Peterson"
]


def generate_name() -> Tuple[str, str]:
    """Generate random first and last name"""
    return random.choice(FIRST_NAMES), random.choice(LAST_NAMES)


def generate_email(first_name: str, last_name: str, domain: str = "psu.edu") -> str:
    """Generate school email"""
    suffix = random.randint(100, 999)
    return f"{first_name[0].lower()}{last_name.lower()}{suffix}@{domain}"


def generate_birth_date() -> str:
    """Generate random birth date (25-55 years old)"""
    year = random.randint(1970, 2000)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    return f"{year}-{month:02d}-{day:02d}"


def generate_fingerprint() -> str:
    """Generate device fingerprint"""
    chars = "0123456789abcdef"
    return "".join(random.choice(chars) for _ in range(32))


# ============ IMAGE GENERATOR ============
def generate_teacher_document(first_name: str, last_name: str, school_name: str) -> bytes:
    """Generate fake teacher certificate PNG"""
    # Create image
    width, height = 800, 500
    img = Image.new("RGB", (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    # Try to use default font
    try:
        title_font = ImageFont.truetype("arial.ttf", 32)
        text_font = ImageFont.truetype("arial.ttf", 24)
        small_font = ImageFont.truetype("arial.ttf", 18)
    except:
        title_font = ImageFont.load_default()
        text_font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    
    # Draw border
    draw.rectangle([(20, 20), (width-20, height-20)], outline=(0, 51, 102), width=3)
    
    # Title
    title = "FACULTY EMPLOYMENT VERIFICATION"
    draw.text((width//2, 60), title, fill=(0, 51, 102), font=title_font, anchor="mm")
    
    # Horizontal line
    draw.line([(50, 100), (width-50, 100)], fill=(0, 51, 102), width=2)
    
    # School name
    draw.text((width//2, 140), school_name, fill=(51, 51, 51), font=text_font, anchor="mm")
    
    # Employee info
    y = 200
    info_lines = [
        f"Employee Name: {first_name} {last_name}",
        f"Position: Faculty Member",
        f"Department: Education",
        f"Employment Status: Active",
        f"Issue Date: {time.strftime('%B %d, %Y')}"
    ]
    
    for line in info_lines:
        draw.text((100, y), line, fill=(51, 51, 51), font=text_font)
        y += 40
    
    # Footer
    draw.text((width//2, height-60), "This document verifies current employment status.", 
              fill=(128, 128, 128), font=small_font, anchor="mm")
    
    # Save to bytes
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return buffer.getvalue()


# ============ VERIFIER ============
class BoltnewVerifier:
    """Bolt.new Teacher Verification"""
    
    def __init__(self, verification_url: str):
        self.verification_url = verification_url
        self.verification_id = self._parse_verification_id(verification_url)
        self.device_fingerprint = generate_fingerprint()
        self.client = httpx.Client(timeout=30.0)
    
    def __del__(self):
        if hasattr(self, "client"):
            self.client.close()
    
    @staticmethod
    def _parse_verification_id(url: str) -> Optional[str]:
        """Extract verification ID from URL"""
        match = re.search(r"verificationId=([a-f0-9]+)", url, re.IGNORECASE)
        return match.group(1) if match else None
    
    def _request(self, method: str, url: str, body: Dict = None) -> Tuple[Dict, int]:
        """Make SheerID API request"""
        headers = {"Content-Type": "application/json"}
        
        try:
            response = self.client.request(
                method=method,
                url=url,
                json=body,
                headers=headers
            )
            try:
                data = response.json()
            except:
                data = {"text": response.text}
            return data, response.status_code
        except Exception as e:
            raise Exception(f"Request failed: {e}")
    
    def _upload_to_s3(self, upload_url: str, data: bytes, mime_type: str) -> bool:
        """Upload file to S3"""
        try:
            response = self.client.put(
                upload_url,
                content=data,
                headers={"Content-Type": mime_type},
                timeout=60.0
            )
            return 200 <= response.status_code < 300
        except Exception as e:
            print(f"   [ERROR] S3 upload failed: {e}")
            return False
    
    def verify(self) -> Dict:
        """Run full verification flow"""
        if not self.verification_id:
            return {"success": False, "error": "Invalid verification URL"}
        
        try:
            # Generate teacher info
            first_name, last_name = generate_name()
            school = select_university()
            email = generate_email(first_name, last_name, school["domain"])
            birth_date = generate_birth_date()
            
            print(f"   Teacher: {first_name} {last_name}")
            print(f"   Email: {email}")
            print(f"   School: {school['name']}")
            print(f"   Birth Date: {birth_date}")
            print(f"   Verification ID: {self.verification_id}")
            
            # Step 1: Generate document
            print("\n   -> Step 1/4: Generating teacher document...")
            doc_data = generate_teacher_document(first_name, last_name, school["name"])
            print(f"      Document size: {len(doc_data)/1024:.2f} KB")
            
            # Step 2: Submit teacher info
            print("   -> Step 2/4: Submitting teacher info...")
            step2_body = {
                "firstName": first_name,
                "lastName": last_name,
                "birthDate": birth_date,
                "email": email,
                "phoneNumber": "",
                "organization": {
                    "id": school["id"],
                    "idExtended": school["idExtended"],
                    "name": school["name"]
                },
                "deviceFingerprintHash": self.device_fingerprint,
                "locale": "en-US",
                "metadata": {
                    "marketConsentValue": False,
                    "verificationId": self.verification_id,
                    "refererUrl": f"{SHEERID_BASE_URL}/verify/{PROGRAM_ID}/?verificationId={self.verification_id}",
                    "submissionOptIn": "By submitting the personal information above, I acknowledge that my personal information is being collected under the privacy policy of the business from which I am seeking a discount"
                }
            }
            
            data, status = self._request(
                "POST",
                f"{SHEERID_BASE_URL}/rest/v2/verification/{self.verification_id}/step/collectTeacherPersonalInfo",
                step2_body
            )
            
            if status != 200:
                return {"success": False, "error": f"Step 2 failed: {status}"}
            
            if isinstance(data, dict) and data.get("currentStep") == "error":
                error_msg = ", ".join(data.get("errorIds", ["Unknown"]))
                return {"success": False, "error": f"Step 2 error: {error_msg}"}
            
            current_step = data.get("currentStep", "") if isinstance(data, dict) else ""
            print(f"      Current step: {current_step}")
            
            # Step 3: Skip SSO if needed
            if current_step in ["sso", "collectTeacherPersonalInfo"]:
                print("   -> Step 3/4: Skipping SSO...")
                self._request(
                    "DELETE",
                    f"{SHEERID_BASE_URL}/rest/v2/verification/{self.verification_id}/step/sso"
                )
            
            # Step 4: Upload document
            print("   -> Step 4/4: Requesting upload URL...")
            step4_body = {
                "files": [{
                    "fileName": "teacher_certificate.png",
                    "mimeType": "image/png",
                    "fileSize": len(doc_data)
                }]
            }
            
            data, status = self._request(
                "POST",
                f"{SHEERID_BASE_URL}/rest/v2/verification/{self.verification_id}/step/docUpload",
                step4_body
            )
            
            if status != 200 or not isinstance(data, dict) or not data.get("documents"):
                return {"success": False, "error": "Failed to get upload URL"}
            
            # Upload to S3
            print("   -> Uploading document to S3...")
            upload_url = data["documents"][0].get("uploadUrl")
            if not upload_url:
                return {"success": False, "error": "No upload URL returned"}
            
            if not self._upload_to_s3(upload_url, doc_data, "image/png"):
                return {"success": False, "error": "S3 upload failed"}
            
            print("   [OK] Document uploaded!")
            
            # Step 5: Complete document upload (PastKing logic)
            print("   -> Step 5/5: Completing upload...")
            data, status = self._request(
                "POST",
                f"{SHEERID_BASE_URL}/rest/v2/verification/{self.verification_id}/step/completeDocUpload"
            )
            print(f"      Upload completed: {data.get('currentStep', 'pending')}")
            
            return {
                "success": True,
                "message": "Verification submitted! Wait for review.",
                "teacher": f"{first_name} {last_name}",
                "email": email,
                "redirectUrl": data.get("redirectUrl")
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}


def main():
    print()
    print("=" * 55)
    print("  Bolt.new Teacher Verification Tool")
    print("  SheerID Teacher Verification")
    print("=" * 55)
    print()
    
    # Get verification URL
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = input("Enter verification URL: ").strip()
    
    if not url or "sheerid.com" not in url:
        print("[ERROR] Invalid URL. Must contain sheerid.com")
        return
    
    print(f"\n[INFO] Processing URL...")
    
    verifier = BoltnewVerifier(url)
    result = verifier.verify()
    
    print()
    if result.get("success"):
        print("-" * 55)
        print("  [SUCCESS] Verification submitted!")
        print(f"  Teacher: {result.get('teacher')}")
        print(f"  Email: {result.get('email')}")
        print("-" * 55)
    else:
        print(f"  [FAILED] {result.get('error')}")


if __name__ == "__main__":
    main()
