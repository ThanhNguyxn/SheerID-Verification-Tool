"""
K12 Teacher Verification Tool
SheerID K12 Teacher Verification (High School)

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
from pathlib import Path
from io import BytesIO
from typing import Dict, Optional, Tuple, Any

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
PROGRAM_ID = "68d47554aa292d20b9bec8f7"
SHEERID_BASE_URL = "https://services.sheerid.com"

# ============ K12 SCHOOLS (from JS data - 50+ schools) ============
# K12 Teacher verification is US-ONLY (High School teachers)
# SheerID verifies against US K-12 school database
K12_SCHOOLS = [
    # NYC Specialized High Schools
    {"id": 155694, "name": "Stuyvesant High School", "city": "New York, NY", "weight": 100},
    {"id": 156251, "name": "Bronx High School Of Science", "city": "Bronx, NY", "weight": 98},
    {"id": 157582, "name": "Brooklyn Technical High School", "city": "Brooklyn, NY", "weight": 95},
    {"id": 155770, "name": "Staten Island Technical High School", "city": "Staten Island, NY", "weight": 90},
    {"id": 158162, "name": "Townsend Harris High School", "city": "Flushing, NY", "weight": 88},
    # Chicago Selective Enrollment
    {"id": 3521141, "name": "Walter Payton College Preparatory High School", "city": "Chicago, IL", "weight": 95},
    {"id": 3521074, "name": "Whitney M Young Magnet High School", "city": "Chicago, IL", "weight": 92},
    {"id": 219471, "name": "Northside College Preparatory High School", "city": "Chicago, IL", "weight": 88},
    {"id": 219254, "name": "Lane Technical High School", "city": "Chicago, IL", "weight": 85},
    # Virginia / DC STEM
    {"id": 3704245, "name": "Thomas Jefferson High School For Science And Technology", "city": "Alexandria, VA", "weight": 100},
    {"id": 167407, "name": "McKinley Technology High School", "city": "Washington, DC", "weight": 85},
    # California Elite
    {"id": 3539252, "name": "Gretchen Whitney High School", "city": "Cerritos, CA", "weight": 95},
    {"id": 262338, "name": "Lowell High School (San Francisco)", "city": "San Francisco, CA", "weight": 90},
    {"id": 262370, "name": "Palo Alto High School", "city": "Palo Alto, CA", "weight": 88},
    {"id": 262410, "name": "Gunn (Henry M.) High School", "city": "Palo Alto, CA", "weight": 85},
    # BASIS Charter Network
    {"id": 3536914, "name": "BASIS Scottsdale", "city": "Scottsdale, AZ", "weight": 90},
    {"id": 250527, "name": "BASIS Tucson North", "city": "Tucson, AZ", "weight": 88},
    {"id": 3536799, "name": "BASIS Mesa", "city": "Mesa, AZ", "weight": 85},
    {"id": 3707277, "name": "BASIS Chandler", "city": "Chandler, AZ", "weight": 82},
    # KIPP Charter
    {"id": 155846, "name": "KIPP Academy Charter School (Bronx)", "city": "Bronx, NY", "weight": 85},
    {"id": 3501341, "name": "KIPP DC Public Charter Schools", "city": "Washington, DC", "weight": 82},
    {"id": 10488713, "name": "KIPP SoCal Public Schools", "city": "Los Angeles, CA", "weight": 80},
    # Lincoln High Schools
    {"id": 270998, "name": "Lincoln High School (Tacoma, WA)", "city": "Tacoma, WA", "weight": 78},
    {"id": 268293, "name": "Lincoln High School (Portland, OR)", "city": "Portland, OR", "weight": 76},
    {"id": 257321, "name": "Lincoln High School (San Diego, CA)", "city": "San Diego, CA", "weight": 75},
    # Science Academies
    {"id": 10148026, "name": "Fulton Science Academy", "city": "Alpharetta, GA", "weight": 85},
    {"id": 3704829, "name": "Bio-Med Science Academy STEM School", "city": "Rootstown, OH", "weight": 82},
    {"id": 3706876, "name": "Harmony Science Academy Dallas", "city": "Dallas, TX", "weight": 80},
    # Elite Prep Schools
    {"id": 185742, "name": "Berkeley Preparatory School", "city": "Tampa, FL", "weight": 78},
    {"id": 168570, "name": "Georgetown Preparatory School", "city": "Rockville, MD", "weight": 80},
    {"id": 145364, "name": "Phillips Academy Andover", "city": "Andover, MA", "weight": 75},
    {"id": 148201, "name": "Phillips Exeter Academy", "city": "Exeter, NH", "weight": 75},
    # Top 50 US - Verified
    {"id": 202063, "name": "Signature School Inc", "city": "Evansville, IN", "weight": 95},
    {"id": 183857, "name": "School For Advanced Studies Homestead", "city": "Homestead, FL", "weight": 92},
    {"id": 3506727, "name": "Loveless Academic Magnet Program High School (LAMP)", "city": "Montgomery, AL", "weight": 90},
    {"id": 178685, "name": "Gwinnett School Of Mathematics, Science And Technology", "city": "Lawrenceville, GA", "weight": 88},
    {"id": 174195, "name": "North Carolina School of Science and Mathematics", "city": "Durham, NC", "weight": 90},
    {"id": 3520767, "name": "Il Mathematics And Science Academy", "city": "Aurora, IL", "weight": 92},
    # Westlake & Bellevue
    {"id": 242400, "name": "Westlake High School Austin", "city": "Austin, TX", "weight": 82},
    {"id": 269511, "name": "Bellevue High School WA", "city": "Bellevue, WA", "weight": 80},
    {"id": 269566, "name": "Interlake Senior High School", "city": "Bellevue, WA", "weight": 78},
]


def select_school():
    """Weighted random selection of K12 school"""
    weights = [s["weight"] for s in K12_SCHOOLS]
    total = sum(weights)
    r = random.uniform(0, total)
    cumulative = 0
    for school in K12_SCHOOLS:
        cumulative += school["weight"]
        if r <= cumulative:
            return {"id": school["id"], "idExtended": str(school["id"]), "name": school["name"], "type": "K12"}
    return {"id": K12_SCHOOLS[0]["id"], "idExtended": str(K12_SCHOOLS[0]["id"]), "name": K12_SCHOOLS[0]["name"], "type": "K12"}

# ============ NAME GENERATOR ============
FIRST_NAMES = [
    # Male names
    "James", "John", "Robert", "Michael", "William", "David", "Richard", "Joseph",
    "Thomas", "Christopher", "Charles", "Daniel", "Matthew", "Anthony", "Mark",
    "Donald", "Steven", "Andrew", "Paul", "Joshua", "Kenneth", "Kevin", "Brian",
    "George", "Timothy", "Ronald", "Edward", "Jason", "Jeffrey", "Ryan",
    "Jacob", "Nicholas", "Eric", "Jonathan", "Stephen", "Larry", "Justin", "Scott",
    "Brandon", "Benjamin", "Samuel", "Raymond", "Gregory", "Frank", "Alexander",
    # Female names
    "Mary", "Patricia", "Jennifer", "Linda", "Elizabeth", "Barbara", "Susan",
    "Jessica", "Sarah", "Karen", "Lisa", "Nancy", "Betty", "Margaret", "Sandra",
    "Ashley", "Kimberly", "Emily", "Donna", "Michelle", "Dorothy", "Carol",
    "Amanda", "Melissa", "Deborah", "Stephanie", "Rebecca", "Sharon", "Laura",
    "Emma", "Olivia", "Ava", "Isabella", "Sophia", "Mia", "Charlotte", "Amelia",
    "Harper", "Evelyn", "Abigail", "Ella", "Scarlett", "Grace", "Victoria", "Riley"
]

LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
    "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
    "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson",
    "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker",
    "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill",
    "Flores", "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell",
    "Mitchell", "Carter", "Roberts", "Turner", "Phillips", "Evans", "Parker", "Edwards",
    "Collins", "Stewart", "Morris", "Murphy", "Cook", "Rogers", "Morgan", "Peterson",
    "Cooper", "Reed", "Bailey", "Bell", "Gomez", "Kelly", "Howard", "Ward"
]


def generate_name() -> Tuple[str, str]:
    return random.choice(FIRST_NAMES), random.choice(LAST_NAMES)


def generate_email(first_name: str, last_name: str) -> str:
    suffix = random.randint(100, 999)
    domains = ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com"]
    domain = random.choice(domains)
    return f"{first_name.lower()}.{last_name.lower()}{suffix}@{domain}"


def generate_birth_date() -> str:
    """Generate birth date (25-55 years old for teacher)"""
    year = random.randint(1970, 2000)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    return f"{year}-{month:02d}-{day:02d}"


def generate_fingerprint() -> str:
    chars = "0123456789abcdef"
    return "".join(random.choice(chars) for _ in range(32))


# ============ IMAGE GENERATOR ============
def generate_white_image() -> bytes:
    """Generate pure white image for bypass when stuck on emailLoop"""
    img = Image.new("RGB", (100, 100), color=(255, 255, 255))
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return buffer.getvalue()


def generate_teacher_badge(first_name: str, last_name: str, school_name: str) -> bytes:
    """Generate fake K12 teacher badge PNG"""
    width, height = 500, 350
    img = Image.new("RGB", (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    try:
        title_font = ImageFont.truetype("arial.ttf", 22)
        text_font = ImageFont.truetype("arial.ttf", 16)
        small_font = ImageFont.truetype("arial.ttf", 12)
    except:
        title_font = ImageFont.load_default()
        text_font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    
    # Header bar
    draw.rectangle([(0, 0), (width, 50)], fill=(34, 139, 34))  # Forest green
    draw.text((width//2, 25), "STAFF IDENTIFICATION", fill=(255, 255, 255), 
              font=title_font, anchor="mm")
    
    # School name
    draw.text((width//2, 75), school_name, fill=(34, 139, 34), font=text_font, anchor="mm")
    
    # Photo placeholder
    draw.rectangle([(25, 100), (125, 220)], outline=(200, 200, 200), width=2)
    draw.text((75, 160), "PHOTO", fill=(200, 200, 200), font=text_font, anchor="mm")
    
    # Teacher info
    teacher_id = f"T{random.randint(10000, 99999)}"
    info_y = 110
    info_lines = [
        f"Name: {first_name} {last_name}",
        f"ID: {teacher_id}",
        f"Position: Teacher",
        f"Department: Education",
        f"Status: Active"
    ]
    
    for line in info_lines:
        draw.text((145, info_y), line, fill=(51, 51, 51), font=text_font)
        info_y += 22
    
    # Valid date
    current_year = int(time.strftime("%Y"))
    draw.text((145, info_y + 10), f"Valid: {current_year}-{current_year+1} School Year", 
              fill=(100, 100, 100), font=small_font)
    
    # Footer
    draw.rectangle([(0, height-35), (width, height)], fill=(34, 139, 34))
    draw.text((width//2, height-18), "Property of School District", 
              fill=(255, 255, 255), font=small_font, anchor="mm")
    
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return buffer.getvalue()


# ============ VERIFIER ============
class K12Verifier:
    """K12 Teacher Verification"""
    
    def __init__(self, verification_url: str, proxy: str = None):
        self.verification_url = verification_url
        self.verification_id = self._parse_verification_id(verification_url)
        self.device_fingerprint = generate_fingerprint()
        
        proxy_url = None
        if proxy:
            if not proxy.startswith("http"):
                proxy = f"http://{proxy}"
            proxy_url = proxy
            
        self.client = httpx.Client(timeout=30.0, proxy=proxy_url)
    
    def __del__(self):
        if hasattr(self, "client"):
            self.client.close()
    
    @staticmethod
    def _parse_verification_id(url: str) -> Optional[str]:
        match = re.search(r"verificationId=([a-f0-9]+)", url, re.IGNORECASE)
        return match.group(1) if match else None
    
    def _request(self, method: str, url: str, body: Dict = None) -> Tuple[Dict, int]:
        headers = {"Content-Type": "application/json"}
        try:
            response = self.client.request(method=method, url=url, json=body, headers=headers)
            try:
                data = response.json()
            except:
                data = {"text": response.text}
            return data, response.status_code
        except Exception as e:
            raise Exception(f"Request failed: {e}")
    
    def _upload_to_s3(self, upload_url: str, data: bytes, mime_type: str) -> bool:
        try:
            response = self.client.put(upload_url, content=data, 
                                       headers={"Content-Type": mime_type}, timeout=60.0)
            return 200 <= response.status_code < 300
        except Exception as e:
            print(f"   [ERROR] S3 upload failed: {e}")
            return False
    
    def verify(self) -> Dict:
        if not self.verification_id:
            return {"success": False, "error": "Invalid verification URL"}
        
        try:
            first_name, last_name = generate_name()
            email = generate_email(first_name, last_name)
            birth_date = generate_birth_date()
            school = select_school()
            
            print(f"   Teacher: {first_name} {last_name}")
            print(f"   Email: {email}")
            print(f"   School: {school['name']}")
            print(f"   Birth Date: {birth_date}")
            print(f"   Verification ID: {self.verification_id}")
            
            # Step 1: Generate teacher badge
            print("\n   -> Step 1/4: Generating teacher badge...")
            doc_data = generate_teacher_badge(first_name, last_name, school["name"])
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
            
            # Check for auto-pass (K12 often doesn't need upload!)
            if current_step == "success":
                print("   ✅ AUTO-PASS! No upload needed!")
                return {
                    "success": True,
                    "message": "Verification auto-approved! No document needed.",
                    "teacher": f"{first_name} {last_name}",
                    "email": email,
                    "auto_pass": True
                }
            
            # Step 3: Skip SSO if needed
            if current_step in ["sso", "collectTeacherPersonalInfo"]:
                print("   -> Step 3/5: Skipping SSO...")
                data, _ = self._request(
                    "DELETE",
                    f"{SHEERID_BASE_URL}/rest/v2/verification/{self.verification_id}/step/sso"
                )
                current_step = data.get("currentStep", "") if isinstance(data, dict) else ""
                
                # Check again for auto-pass after SSO skip
                if current_step == "success":
                    print("   ✅ AUTO-PASS after SSO skip!")
                    return {
                        "success": True,
                        "message": "Verification auto-approved!",
                        "teacher": f"{first_name} {last_name}",
                        "email": email,
                        "auto_pass": True
                    }
            
            # Handle emailLoop step - API does NOT allow docUpload when stuck here!
            # SheerID requires clicking email verification link before allowing doc upload
            # Return special status so caller can request new link and retry
            if current_step == "emailLoop":
                print(f"\n   ⚠️  emailLoop triggered for: {school['name']}")
                print(f"      This school/data combo requires email verification")
                return {
                    "success": False,
                    "email_loop": True,
                    "school": school["name"],
                    "teacher": f"{first_name} {last_name}",
                    "error": "emailLoop - need new verification link"
                }
            
            # Step 4: Upload document
            print("   -> Step 4/4: Uploading teacher badge...")
            step4_body = {
                "files": [{
                    "fileName": "teacher_badge.png",
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
                print(f"   [ERROR] Upload init failed. Status: {status}")
                print(f"   [DEBUG] Response: {json.dumps(data)}")
                return {"success": False, "error": "Failed to get upload URL"}
            
            upload_url = data["documents"][0].get("uploadUrl")
            if not upload_url:
                return {"success": False, "error": "No upload URL returned"}
            
            if not self._upload_to_s3(upload_url, doc_data, "image/png"):
                return {"success": False, "error": "S3 upload failed"}
            
            print("   [OK] Document uploaded!")
            
            # Step 5: Complete document upload
            print("   -> Step 5/5: Completing upload...")
            data, _ = self._request(
                "POST",
                f"{SHEERID_BASE_URL}/rest/v2/verification/{self.verification_id}/step/completeDocUpload"
            )
            print(f"      Upload completed: {data.get('currentStep', 'pending') if isinstance(data, dict) else 'pending'}")
            
            return {
                "success": True,
                "message": "Verification submitted! Wait for review.",
                "teacher": f"{first_name} {last_name}",
                "email": email,
                "auto_pass": False
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}


def main():
    print()
    print("=" * 55)
    print("  K12 Teacher Verification Tool")
    print("  SheerID K12 Teacher Verification (High School)")
    print("=" * 55)
    print()
    
    import argparse
    parser = argparse.ArgumentParser(description="K12 Teacher Verification Tool")
    parser.add_argument("url", nargs="?", help="Verification URL")
    parser.add_argument("--proxy", help="Proxy URL (e.g., http://user:pass@host:port)")
    args = parser.parse_args()

    if args.url:
        url = args.url
    else:
        url = input("Enter verification URL: ").strip()
    
    if not url or "sheerid.com" not in url:
        print("[ERROR] Invalid URL. Must contain sheerid.com")
        return
    
    print(f"\n[INFO] Processing URL...")
    if args.proxy:
        print(f"[INFO] Using proxy: {args.proxy}")
    
    verifier = K12Verifier(url, proxy=args.proxy)
    result = verifier.verify()
    
    print()
    if result.get("success"):
        print("-" * 55)
        print("  [SUCCESS] Verification submitted!")
        print(f"  Teacher: {result.get('teacher')}")
        print(f"  Email: {result.get('email')}")
        print("-" * 55)
    elif result.get("email_loop"):
        print("-" * 55)
        print("  ⚠️  EMAIL VERIFICATION REQUIRED")
        print("-" * 55)
        print(f"  School: {result.get('school')}")
        print(f"  Teacher: {result.get('teacher')}")
        print()
        print("  This school/data combination triggered SheerID's")
        print("  email verification loop. The API does not allow")
        print("  bypassing this step.")
        print()
        print("  📋 SOLUTION:")
        print("  1. Get a NEW verification link from ChatGPT K12 page")
        print("  2. Run this tool again with the new link")
        print("  3. Tool will use DIFFERENT random data which may auto-pass")
        print("-" * 55)
    else:
        print(f"  [FAILED] {result.get('error')}")


if __name__ == "__main__":
    main()
