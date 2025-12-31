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

# ============ CONFIG ============
PROGRAM_ID = "68d47554aa292d20b9bec8f7"
SHEERID_BASE_URL = "https://services.sheerid.com"

# High Schools (Springfield High School variants)
SCHOOLS = {
    "3995910": {
        "id": 3995910,
        "idExtended": "3995910",
        "name": "Springfield High School (Springfield, OR)",
        "type": "HIGH_SCHOOL"
    },
    "3995271": {
        "id": 3995271,
        "idExtended": "3995271",
        "name": "Springfield High School (Springfield, OH)",
        "type": "HIGH_SCHOOL"
    },
    "3992142": {
        "id": 3992142,
        "idExtended": "3992142",
        "name": "Springfield High School (Springfield, IL)",
        "type": "HIGH_SCHOOL"
    },
    "3996208": {
        "id": 3996208,
        "idExtended": "3996208",
        "name": "Springfield High School (Springfield, PA)",
        "type": "HIGH_SCHOOL"
    }
}

DEFAULT_SCHOOL_ID = "3995910"

# ============ NAME GENERATOR ============
FIRST_NAMES = [
    "James", "John", "Robert", "Michael", "William", "David", "Richard", "Joseph",
    "Thomas", "Christopher", "Mary", "Patricia", "Jennifer", "Linda", "Elizabeth",
    "Barbara", "Susan", "Jessica", "Sarah", "Karen", "Daniel", "Matthew", "Anthony"
]

LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
    "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson"
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
            school = SCHOOLS[DEFAULT_SCHOOL_ID]
            
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
                    "marketConsentValue": True,
                    "submissionOptIn": "By submitting, I acknowledge the privacy policy."
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
                return {"success": False, "error": "Failed to get upload URL"}
            
            upload_url = data["documents"][0].get("uploadUrl")
            if not upload_url:
                return {"success": False, "error": "No upload URL returned"}
            
            if not self._upload_to_s3(upload_url, doc_data, "image/png"):
                return {"success": False, "error": "S3 upload failed"}
            
            print("   [OK] Document uploaded successfully!")
            
            return {
                "success": True,
                "message": "Verification submitted! Wait for review.",
                "teacher": f"{first_name} {last_name}",
                "email": email
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
    
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = input("Enter verification URL: ").strip()
    
    if not url or "sheerid.com" not in url:
        print("[ERROR] Invalid URL. Must contain sheerid.com")
        return
    
    print(f"\n[INFO] Processing URL...")
    
    verifier = K12Verifier(url)
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
