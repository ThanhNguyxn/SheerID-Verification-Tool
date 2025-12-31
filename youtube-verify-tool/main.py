"""
YouTube Student Verification Tool
SheerID Student Verification for YouTube Premium

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
# YouTube uses same program as Spotify for student verification
PROGRAM_ID = "67c8c14f5f17a83b745e3f82"
SHEERID_BASE_URL = "https://services.sheerid.com"

# Pennsylvania State University campuses
SCHOOLS = {
    "2565": {
        "id": 2565,
        "idExtended": "2565",
        "name": "Pennsylvania State University-Main Campus",
        "domain": "PSU.EDU"
    },
    "651379": {
        "id": 651379,
        "idExtended": "651379",
        "name": "Pennsylvania State University-World Campus",
        "domain": "PSU.EDU"
    },
    "8387": {
        "id": 8387,
        "idExtended": "8387",
        "name": "Pennsylvania State University-Penn State Harrisburg",
        "domain": "PSU.EDU"
    }
}

DEFAULT_SCHOOL_ID = "2565"

# ============ NAME GENERATOR ============
FIRST_NAMES = [
    "James", "John", "Robert", "Michael", "William", "David", "Richard", "Joseph",
    "Thomas", "Christopher", "Mary", "Patricia", "Jennifer", "Linda", "Elizabeth",
    "Barbara", "Susan", "Jessica", "Sarah", "Karen", "Daniel", "Matthew", "Anthony",
    "Mark", "Donald", "Steven", "Andrew", "Paul", "Joshua", "Kenneth"
]

LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
    "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
    "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson",
    "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson"
]


def generate_name() -> Tuple[str, str]:
    return random.choice(FIRST_NAMES), random.choice(LAST_NAMES)


def generate_email(first_name: str, last_name: str) -> str:
    suffix = random.randint(100, 999)
    return f"{first_name[0].lower()}{last_name.lower()}{suffix}@psu.edu"


def generate_birth_date() -> str:
    """Generate birth date (18-25 years old for student)"""
    year = random.randint(2000, 2006)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    return f"{year}-{month:02d}-{day:02d}"


def generate_fingerprint() -> str:
    chars = "0123456789abcdef"
    return "".join(random.choice(chars) for _ in range(32))


# ============ IMAGE GENERATOR ============
def generate_student_id(first_name: str, last_name: str, school_name: str) -> bytes:
    """Generate fake student ID PNG"""
    width, height = 600, 380
    img = Image.new("RGB", (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    try:
        title_font = ImageFont.truetype("arial.ttf", 24)
        text_font = ImageFont.truetype("arial.ttf", 18)
        small_font = ImageFont.truetype("arial.ttf", 14)
    except:
        title_font = ImageFont.load_default()
        text_font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    
    # Header bar
    draw.rectangle([(0, 0), (width, 60)], fill=(0, 51, 102))
    draw.text((width//2, 30), "STUDENT IDENTIFICATION CARD", fill=(255, 255, 255), 
              font=title_font, anchor="mm")
    
    # School name
    draw.text((width//2, 90), school_name, fill=(0, 51, 102), font=text_font, anchor="mm")
    
    # Photo placeholder
    draw.rectangle([(30, 120), (150, 280)], outline=(200, 200, 200), width=2)
    draw.text((90, 200), "PHOTO", fill=(200, 200, 200), font=text_font, anchor="mm")
    
    # Student info
    student_id = f"PSU{random.randint(100000, 999999)}"
    info_y = 130
    info_lines = [
        f"Name: {first_name} {last_name}",
        f"Student ID: {student_id}",
        f"Major: Computer Science",
        f"Status: Full-time Student",
        f"Valid: {time.strftime('%Y')} - {int(time.strftime('%Y'))+1}"
    ]
    
    for line in info_lines:
        draw.text((180, info_y), line, fill=(51, 51, 51), font=text_font)
        info_y += 30
    
    # Footer
    draw.rectangle([(0, height-40), (width, height)], fill=(0, 51, 102))
    draw.text((width//2, height-20), "This card is property of the university", 
              fill=(255, 255, 255), font=small_font, anchor="mm")
    
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return buffer.getvalue()


# ============ VERIFIER ============
class YouTubeVerifier:
    """YouTube Student Verification"""
    
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
            
            print(f"   Student: {first_name} {last_name}")
            print(f"   Email: {email}")
            print(f"   School: {school['name']}")
            print(f"   Birth Date: {birth_date}")
            print(f"   Verification ID: {self.verification_id}")
            
            # Step 1: Generate student ID
            print("\n   -> Step 1/3: Generating student ID...")
            doc_data = generate_student_id(first_name, last_name, school["name"])
            print(f"      Document size: {len(doc_data)/1024:.2f} KB")
            
            # Step 2: Submit student info
            print("   -> Step 2/3: Submitting student info...")
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
                f"{SHEERID_BASE_URL}/rest/v2/verification/{self.verification_id}/step/collectStudentPersonalInfo",
                step2_body
            )
            
            if status != 200:
                return {"success": False, "error": f"Step 2 failed: {status}"}
            
            if isinstance(data, dict) and data.get("currentStep") == "error":
                error_msg = ", ".join(data.get("errorIds", ["Unknown"]))
                return {"success": False, "error": f"Step 2 error: {error_msg}"}
            
            current_step = data.get("currentStep", "") if isinstance(data, dict) else ""
            print(f"      Current step: {current_step}")
            
            # Step 3: Upload document
            print("   -> Step 3/3: Uploading student ID...")
            step3_body = {
                "files": [{
                    "fileName": "student_id.png",
                    "mimeType": "image/png",
                    "fileSize": len(doc_data)
                }]
            }
            
            data, status = self._request(
                "POST",
                f"{SHEERID_BASE_URL}/rest/v2/verification/{self.verification_id}/step/docUpload",
                step3_body
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
                "student": f"{first_name} {last_name}",
                "email": email
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}


def main():
    print()
    print("=" * 55)
    print("  YouTube Student Verification Tool")
    print("  SheerID Student Verification")
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
    
    verifier = YouTubeVerifier(url)
    result = verifier.verify()
    
    print()
    if result.get("success"):
        print("-" * 55)
        print("  [SUCCESS] Verification submitted!")
        print(f"  Student: {result.get('student')}")
        print(f"  Email: {result.get('email')}")
        print("-" * 55)
    else:
        print(f"  [FAILED] {result.get('error')}")


if __name__ == "__main__":
    main()
