"""
Canva Education Teacher Verification Tool
UK Teacher Document Generator for SheerID Bypass

Supports:
- Employment Letter (UK school letterhead)
- Teacher ID Card (UK school staff ID)
- Teaching License (DfE QTS certificate)

Author: ThanhNguyxn
Based on: GitHub Issue #49 templates by cruzzzdev
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
from typing import Dict, Optional, Tuple, List
from datetime import datetime, timedelta

try:
    import httpx
except ImportError:
    print("❌ Error: httpx required. Install: pip install httpx")
    sys.exit(1)

try:
    import fitz  # PyMuPDF
except ImportError:
    print("❌ Error: PyMuPDF required. Install: pip install pymupdf")
    sys.exit(1)

try:
    from PIL import Image
except ImportError:
    print("❌ Error: Pillow required. Install: pip install Pillow")
    sys.exit(1)

# Import anti-detection module
try:
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from anti_detect import get_headers, get_fingerprint, random_delay as anti_delay
    HAS_ANTI_DETECT = True
except ImportError:
    HAS_ANTI_DETECT = False


# ============ CONFIG ============
SHEERID_API_URL = "https://services.sheerid.com/rest/v2"
ASSETS_DIR = Path(__file__).parent / "assets"
TEMPLATES_DIR = ASSETS_DIR / "templates"
DATA_DIR = Path(__file__).parent / "data"
MIN_DELAY = 300
MAX_DELAY = 800


# ============ UK SCHOOLS DATABASE ============
# Default UK schools (fallback if database not loaded)
DEFAULT_UK_SCHOOLS = [
    {"name": "Leeds Grammar School", "address": "Alwoodley Gates, Harrogate Road", "town": "Leeds", "postcode": "LS17 8GS", "phone": "0139 1219 502", "lea": "Leeds LEA"},
    {"name": "Manchester Grammar School", "address": "Old Hall Lane", "town": "Manchester", "postcode": "M13 0XT", "phone": "0161 224 7201", "lea": "Manchester LEA"},
    {"name": "King Edward's School", "address": "Edgbaston Park Road", "town": "Birmingham", "postcode": "B15 2UA", "phone": "0121 472 1672", "lea": "Birmingham LEA"},
    {"name": "St Paul's School", "address": "Lonsdale Road", "town": "London", "postcode": "SW13 9JT", "phone": "020 8748 9162", "lea": "Richmond LEA"},
    {"name": "Westminster School", "address": "Little Dean's Yard", "town": "London", "postcode": "SW1P 3PF", "phone": "020 7963 1000", "lea": "Westminster LEA"},
    {"name": "Eton College", "address": "High Street", "town": "Windsor", "postcode": "SL4 6DW", "phone": "01753 370 100", "lea": "Windsor LEA"},
    {"name": "Harrow School", "address": "5 High Street", "town": "Harrow", "postcode": "HA1 3HP", "phone": "020 8872 8000", "lea": "Harrow LEA"},
    {"name": "Rugby School", "address": "Lawrence Sheriff Street", "town": "Rugby", "postcode": "CV22 5EH", "phone": "01788 556 216", "lea": "Warwickshire LEA"},
    {"name": "Cheltenham Ladies' College", "address": "Bayshill Road", "town": "Cheltenham", "postcode": "GL50 3EP", "phone": "01242 520 691", "lea": "Gloucestershire LEA"},
    {"name": "Dulwich College", "address": "Dulwich Common", "town": "London", "postcode": "SE21 7LD", "phone": "020 8693 3601", "lea": "Southwark LEA"},
]


class UKSchoolDatabase:
    """Manage UK schools database"""
    
    def __init__(self):
        self.schools = self._load()
    
    def _load(self) -> List[Dict]:
        """Load schools from JSON or use defaults"""
        json_path = DATA_DIR / "uk_schools.json"
        if json_path.exists():
            try:
                return json.loads(json_path.read_text())
            except:
                pass
        return DEFAULT_UK_SCHOOLS
    
    def random_school(self) -> Dict:
        """Get a random UK school"""
        return random.choice(self.schools)
    
    def search(self, query: str) -> Optional[Dict]:
        """Search for a school by name"""
        query_lower = query.lower()
        for school in self.schools:
            if query_lower in school["name"].lower():
                return school
        return None


# Initialize database
uk_schools = UKSchoolDatabase()


# ============ NAME GENERATORS ============
UK_FIRST_NAMES = [
    "James", "Oliver", "Harry", "George", "Noah", "Jack", "Charlie", "Oscar",
    "William", "Henry", "Thomas", "Alfie", "Joshua", "Leo", "Archie", "Ethan",
    "Emma", "Olivia", "Amelia", "Isla", "Ava", "Mia", "Emily", "Isabella",
    "Sophia", "Grace", "Lily", "Chloe", "Ella", "Charlotte", "Sophie", "Alice",
    "Angela", "David", "Michael", "Sarah", "Claire", "Andrew", "Peter", "Susan"
]

UK_LAST_NAMES = [
    "Smith", "Jones", "Williams", "Taylor", "Brown", "Davies", "Evans", "Wilson",
    "Thomas", "Roberts", "Johnson", "Lewis", "Walker", "Robinson", "Wood", "Thompson",
    "White", "Watson", "Jackson", "Wright", "Green", "Harris", "Cooper", "King",
    "Lee", "Martin", "Clarke", "James", "Morgan", "Hughes", "Edwards", "Hill",
    "Ramirez", "Anderson", "Moore", "Garcia", "Martinez", "Davis", "Miller", "Wilson"
]

TEACHING_POSITIONS = [
    "Head of Drama Department",
    "Head of English Department", 
    "Head of Mathematics Department",
    "Head of Science Department",
    "Head of History Department",
    "Head of Geography Department",
    "Head of Modern Languages",
    "Head of Art Department",
    "Head of Music Department",
    "Head of PE Department",
    "Deputy Head Teacher",
    "Senior Teacher",
    "Class Teacher",
    "Subject Leader - English",
    "Subject Leader - Mathematics",
    "Year Group Leader",
    "Teaching and Learning Coordinator",
]


def random_delay():
    time.sleep(random.randint(MIN_DELAY, MAX_DELAY) / 1000)


def generate_fingerprint() -> str:
    components = [str(time.time()), str(random.random()), "1920x1080"]
    return hashlib.md5("|".join(components).encode()).hexdigest()


def generate_name() -> Tuple[str, str]:
    return random.choice(UK_FIRST_NAMES), random.choice(UK_LAST_NAMES)


def generate_teacher_email(first: str, last: str, school_name: str) -> str:
    """Generate realistic school email"""
    # Create school domain from name
    domain_base = school_name.lower().replace(" ", "").replace("'", "")[:15]
    domain = f"{domain_base}.sch.uk"
    
    patterns = [
        f"{first.lower()}.{last.lower()}",
        f"{first[0].lower()}{last.lower()}",
        f"{first.lower()}{last[0].lower()}",
    ]
    return f"{random.choice(patterns)}@{domain}"


def generate_dob(min_age: int = 28, max_age: int = 60) -> str:
    """Generate DOB for teacher (between 28-60 years old)"""
    today = datetime.now()
    age = random.randint(min_age, max_age)
    birth_year = today.year - age
    birth_month = random.randint(1, 12)
    birth_day = random.randint(1, 28)
    return f"{birth_day:02d}/{birth_month:02d}/{birth_year}"


def generate_trn() -> str:
    """Generate Teacher Reference Number (7 digits)"""
    return str(random.randint(1000000, 9999999))


def generate_staff_id() -> str:
    """Generate staff ID number"""
    return f"STF-{random.randint(2020, 2025)}-{random.randint(100000, 999999)}"


def generate_data_controller_no() -> str:
    """Generate Data Controller Number"""
    return f"Z{random.randint(1000000, 9999999)}"


# ============ DOCUMENT GENERATORS ============

def generate_employment_letter(first: str, last: str, school: Dict, position: str) -> bytes:
    """
    Generate Employment Letter by modifying PDF template
    
    Template placeholders found:
    - "Leeds Grammar School" -> school name
    - "Alwoodley Gates" -> address
    - "Dr. S. Evans" -> teacher name (appears as signatory too)
    - "07 January 2026" -> current date
    - "Z6615748" -> Data Controller No
    """
    pdf_path = TEMPLATES_DIR / "Employment_Letter.pdf"
    if not pdf_path.exists():
        raise FileNotFoundError(f"Template not found: {pdf_path}")
    
    doc = fitz.open(str(pdf_path))
    page = doc[0]
    
    # Current date
    current_date = datetime.now().strftime("%d %B %Y")
    data_controller = generate_data_controller_no()
    
    # Replacements
    replacements = [
        ("Leeds Grammar School", school["name"]),
        ("Alwoodley Gates", school["address"].split(",")[0] if "," in school["address"] else school["address"]),
        ("Harrogate Road", school["address"].split(",")[1].strip() if "," in school["address"] else ""),
        ("Leeds LS17 8GS", f"{school['town']} {school['postcode']}"),
        ("0139 1219 502", school.get("phone", "0800 000 0000")),
        ("07 January 2026", current_date),
        ("Z6615748", data_controller),
        ("Dr. S. Evans", f"{first} {last}"),
        ("Angela Ramirez", f"{first} {last}"),
        ("ANGELA RAMIREZ", f"{first.upper()} {last.upper()}"),
        ("HEAD OF DRAMA", position.upper().replace("HEAD OF ", "").replace(" DEPARTMENT", "")),
        ("Head of Drama Department", position),
        ("Leeds LEA", school.get("lea", f"{school['town']} LEA")),
    ]
    
    # Collect positions and apply redactions
    for old_text, new_text in replacements:
        if not new_text:
            continue
        areas = page.search_for(old_text)
        for rect in areas:
            page.add_redact_annot(rect, fill=(1, 1, 1))
    
    page.apply_redactions()
    
    # Insert new text
    for old_text, new_text in replacements:
        if not new_text:
            continue
        areas = page.search_for(old_text)
        # Search may fail after redaction, so we reopen
    
    # Save modified PDF
    pdf_bytes = doc.tobytes()
    doc.close()
    
    # Reopen and do text insertion properly
    doc = fitz.open("pdf", pdf_bytes)
    page = doc[0]
    
    # Convert to PNG for upload (SheerID expects image)
    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
    doc.close()
    
    return pix.tobytes("png")


def generate_teacher_id_card(first: str, last: str, school: Dict, position: str, dob: str) -> bytes:
    """
    Generate Teacher ID Card by modifying PDF template
    
    Template placeholders found:
    - "LEEDS GRAMMAR SCHOOL" -> school name
    - "ANGELA RAMIREZ" -> teacher name
    - "HEAD OF DRAMA DEPARTMENT" -> position
    - "STF-2024-489194" -> staff ID
    - "19/08/1965" -> DOB
    - "10/08/2025" -> issue date
    - "05/10/2028" -> expiry date
    - "Leeds LEA" -> LEA
    """
    pdf_path = TEMPLATES_DIR / "Teacher_ID_Card.pdf"
    if not pdf_path.exists():
        raise FileNotFoundError(f"Template not found: {pdf_path}")
    
    doc = fitz.open(str(pdf_path))
    page = doc[0]
    
    # Generate dates
    staff_id = generate_staff_id()
    issue_date = datetime.now().strftime("%d/%m/%Y")
    expiry_date = (datetime.now() + timedelta(days=3*365)).strftime("%d/%m/%Y")
    
    # Replacements
    replacements = [
        ("LEEDS GRAMMAR SCHOOL", school["name"].upper()),
        ("ANGELA RAMIREZ", f"{first.upper()} {last.upper()}"),
        ("HEAD OF DRAMA", position.upper().split(" - ")[-1] if " - " in position else position.upper().replace("HEAD OF ", "").replace(" DEPARTMENT", "")),
        ("STF-2024-489194", staff_id),
        ("489194", staff_id.split("-")[-1]),
        ("19/08/1965", dob),
        ("10/08/2025", issue_date),
        ("05/10/2028", expiry_date),
        ("Leeds LEA", school.get("lea", f"{school['town']} LEA")),
    ]
    
    # Apply redactions
    for old_text, new_text in replacements:
        areas = page.search_for(old_text)
        for rect in areas:
            page.add_redact_annot(rect, fill=(1, 1, 1))
    
    page.apply_redactions()
    
    # Re-insert text would require font handling, skip for now
    # Just convert to PNG
    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
    doc.close()
    
    return pix.tobytes("png")


def generate_teaching_license(first: str, last: str) -> bytes:
    """
    Generate Teaching License (QTS Certificate) by modifying PDF template
    
    Template placeholders found:
    - Teacher Reference Number (TRN)
    - Teacher name
    - Award date
    """
    pdf_path = TEMPLATES_DIR / "Teaching_License.pdf"
    if not pdf_path.exists():
        raise FileNotFoundError(f"Template not found: {pdf_path}")
    
    doc = fitz.open(str(pdf_path))
    page = doc[0]
    
    # Generate TRN
    trn = generate_trn()
    award_date = (datetime.now() - timedelta(days=random.randint(365, 3650))).strftime("%d %B %Y")
    
    # For QTS, we mainly need to find and replace name and TRN
    # The template structure is complex, so we'll render as-is for now
    # Convert to PNG
    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
    doc.close()
    
    return pix.tobytes("png")


# ============ SHEERID VERIFIER ============

class CanvaTeacherVerifier:
    """Canva Education Teacher Verification via SheerID"""
    
    def __init__(self, url: str):
        self.url = url
        self.vid = self._parse_verification_id(url)
        self.program_id = self._parse_program_id(url)
        self.fingerprint = generate_fingerprint()
        self.client = httpx.Client(
            timeout=30,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Accept": "application/json",
                "Accept-Language": "en-GB,en;q=0.9",
                "Origin": "https://services.sheerid.com",
                "Referer": "https://services.sheerid.com/"
            }
        )
        self.school = None
        self.org_id = None
    
    def __del__(self):
        if hasattr(self, "client"):
            self.client.close()
    
    @staticmethod
    def _parse_verification_id(url: str) -> Optional[str]:
        """Extract verification ID from URL"""
        match = re.search(r"verificationId=([a-f0-9]+)", url, re.IGNORECASE)
        if match:
            return match.group(1)
        match = re.search(r"/verification/([a-f0-9]+)", url, re.IGNORECASE)
        if match:
            return match.group(1)
        return None
    
    @staticmethod
    def _parse_program_id(url: str) -> Optional[str]:
        """Extract program ID from URL"""
        match = re.search(r"/verify/([a-f0-9]+)/?", url, re.IGNORECASE)
        return match.group(1) if match else None
    
    def _request(self, method: str, endpoint: str, body: Dict = None) -> Tuple[Dict, int]:
        random_delay()
        try:
            resp = self.client.request(
                method, 
                f"{SHEERID_API_URL}{endpoint}",
                json=body,
                headers={"Content-Type": "application/json"} if body else {}
            )
            return resp.json() if resp.text else {}, resp.status_code
        except Exception as e:
            return {"error": str(e)}, 500
    
    def _upload_s3(self, url: str, data: bytes) -> bool:
        """Upload document to S3"""
        try:
            resp = self.client.put(url, content=data, headers={"Content-Type": "image/png"}, timeout=60)
            return 200 <= resp.status_code < 300
        except:
            return False
    
    def search_organization(self, query: str) -> Optional[Dict]:
        """Search for school/organization in SheerID"""
        print(f"   🔍 Searching for '{query}'...")
        endpoint = f"/organization?searchTerm={query}&programId={self.program_id}&country=GB"
        data, status = self._request("GET", endpoint)
        
        if status == 200 and isinstance(data, list) and len(data) > 0:
            print(f"     ✅ Found {len(data)} results")
            return data[0]
        return None
    
    def check_link(self) -> Dict:
        """Check if verification link is valid"""
        if not self.vid:
            return {"valid": False, "error": "Invalid URL - no verification ID found"}
        
        data, status = self._request("GET", f"/verification/{self.vid}")
        if status != 200:
            return {"valid": False, "error": f"HTTP {status}"}
        
        step = data.get("currentStep", "")
        valid_steps = ["collectTeacherPersonalInfo", "collectStudentPersonalInfo", "docUpload", "sso"]
        
        if step in valid_steps:
            return {"valid": True, "step": step, "segment": data.get("segment", "teacher")}
        elif step == "success":
            return {"valid": False, "error": "Already verified"}
        elif step == "pending":
            return {"valid": False, "error": "Already pending review"}
        
        return {"valid": False, "error": f"Invalid step: {step}"}
    
    def verify(self, doc_type: str = "employment_letter") -> Dict:
        """Run full verification"""
        if not self.vid:
            return {"success": False, "error": "Invalid verification URL"}
        
        try:
            # Check current step
            check_data, check_status = self._request("GET", f"/verification/{self.vid}")
            current_step = check_data.get("currentStep", "") if check_status == 200 else ""
            segment = check_data.get("segment", "teacher")
            
            # Generate teacher info
            first, last = generate_name()
            self.school = uk_schools.random_school()
            position = random.choice(TEACHING_POSITIONS)
            dob = generate_dob()
            email = generate_teacher_email(first, last, self.school["name"])
            
            print(f"\n   👩‍🏫 Teacher: {first} {last}")
            print(f"   📧 Email: {email}")
            print(f"   🏫 School: {self.school['name']}")
            print(f"   💼 Position: {position}")
            print(f"   🎂 DOB: {dob}")
            print(f"   📍 Current step: {current_step}")
            
            # Step 1: Generate document
            print(f"\n   ▶ Step 1/4: Generating {doc_type.replace('_', ' ')}...")
            
            if doc_type == "employment_letter":
                doc = generate_employment_letter(first, last, self.school, position)
            elif doc_type == "teacher_id":
                doc = generate_teacher_id_card(first, last, self.school, position, dob)
            elif doc_type == "teaching_license":
                doc = generate_teaching_license(first, last)
            else:
                doc = generate_employment_letter(first, last, self.school, position)
            
            print(f"     📄 Document size: {len(doc)/1024:.1f} KB")
            
            # Step 2: Search for organization
            print("   ▶ Step 2/4: Finding school in SheerID...")
            org = self.search_organization(self.school["name"])
            if not org:
                # Try with just town
                org = self.search_organization(f"school {self.school['town']}")
            if not org:
                # Use fallback
                org = {"id": random.randint(100000, 999999), "name": self.school["name"], "idExtended": str(random.randint(100000, 999999))}
                print(f"     ⚠️ Using generated org ID")
            else:
                print(f"     ✅ Found org: {org.get('name', 'Unknown')}")
            
            self.org_id = org.get("id")
            
            # Step 3: Submit personal info (if needed)
            collect_step = "collectTeacherPersonalInfo" if segment == "teacher" else "collectStudentPersonalInfo"
            
            if current_step == collect_step:
                print(f"   ▶ Step 3/4: Submitting teacher info...")
                body = {
                    "firstName": first,
                    "lastName": last,
                    "birthDate": dob.replace("/", "-"),  # Convert to ISO format
                    "email": email,
                    "organization": {
                        "id": org.get("id"),
                        "idExtended": org.get("idExtended", str(org.get("id"))),
                        "name": org.get("name", self.school["name"])
                    },
                    "deviceFingerprintHash": self.fingerprint,
                    "locale": "en-GB"
                }
                
                data, status = self._request("POST", f"/verification/{self.vid}/step/{collect_step}", body)
                
                if status != 200:
                    return {"success": False, "error": f"Submit failed: {status} - {data}"}
                
                current_step = data.get("currentStep", "")
                print(f"     📍 New step: {current_step}")
            
            # Skip SSO if needed
            if current_step == "sso":
                print("   ▶ Skipping SSO...")
                self._request("DELETE", f"/verification/{self.vid}/step/sso")
            
            # Step 4: Upload document
            print("   ▶ Step 4/4: Uploading document...")
            upload_body = {
                "files": [{
                    "fileName": f"teacher_doc_{int(time.time())}.png",
                    "mimeType": "image/png",
                    "fileSize": len(doc)
                }]
            }
            
            data, status = self._request("POST", f"/verification/{self.vid}/step/docUpload", upload_body)
            
            if not data.get("documents"):
                return {"success": False, "error": "No upload URL received"}
            
            upload_url = data["documents"][0].get("uploadUrl")
            if not self._upload_s3(upload_url, doc):
                return {"success": False, "error": "S3 upload failed"}
            
            print("     ✅ Document uploaded!")
            
            # Complete upload
            data, status = self._request("POST", f"/verification/{self.vid}/step/completeDocUpload")
            final_step = data.get("currentStep", "pending")
            print(f"     ✅ Completed: {final_step}")
            
            return {
                "success": True,
                "message": "Verification submitted! Wait 24-48h for review.",
                "teacher": f"{first} {last}",
                "email": email,
                "school": self.school["name"],
                "position": position,
                "status": final_step
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}


# ============ MAIN ============

def main():
    import argparse
    
    print()
    print("╔" + "═" * 58 + "╗")
    print("║" + " 🎓 Canva Education Teacher Verification Tool".center(58) + "║")
    print("║" + " UK Teacher Document Generator".center(58) + "║")
    print("╚" + "═" * 58 + "╝")
    print()
    
    parser = argparse.ArgumentParser(description="Canva Education Teacher Verification")
    parser.add_argument("url", nargs="?", help="SheerID verification URL")
    parser.add_argument("--doc-type", "-d", choices=["employment_letter", "teacher_id", "teaching_license"],
                        default="employment_letter", help="Document type to generate")
    parser.add_argument("--test-doc", "-t", action="store_true", help="Generate test document only")
    args = parser.parse_args()
    
    # Test mode
    if args.test_doc:
        print("   🧪 Test mode: Generating sample document...")
        first, last = generate_name()
        school = uk_schools.random_school()
        position = random.choice(TEACHING_POSITIONS)
        dob = generate_dob()
        
        print(f"   Teacher: {first} {last}")
        print(f"   School: {school['name']}")
        print(f"   Position: {position}")
        
        if args.doc_type == "employment_letter":
            doc = generate_employment_letter(first, last, school, position)
        elif args.doc_type == "teacher_id":
            doc = generate_teacher_id_card(first, last, school, position, dob)
        else:
            doc = generate_teaching_license(first, last)
        
        output_path = Path(__file__).parent / f"test_{args.doc_type}.png"
        output_path.write_bytes(doc)
        print(f"   ✅ Saved to: {output_path}")
        return
    
    # Get URL
    if args.url:
        url = args.url
    else:
        print("   💡 TIP: To get the verification URL:")
        print("   1. Start Canva Education verification")
        print("   2. Open Developer Tools (F12) -> Network tab")
        print("   3. Filter by 'sheerid'")
        print("   4. Find request with 'verificationId='")
        print("   5. Copy the full URL")
        print()
        url = input("   Enter verification URL: ").strip()
    
    if not url or "sheerid.com" not in url.lower():
        print("\n   ❌ Invalid URL. Must contain sheerid.com")
        return
    
    print(f"\n   📝 Using document type: {args.doc_type.replace('_', ' ').title()}")
    print("   ⏳ Processing...")
    
    verifier = CanvaTeacherVerifier(url)
    
    # Check link
    check = verifier.check_link()
    if not check.get("valid"):
        print(f"\n   ❌ Link Error: {check.get('error')}")
        return
    
    print(f"   ✅ Link valid - Step: {check.get('step')}")
    
    # Run verification
    result = verifier.verify(args.doc_type)
    
    print()
    print("─" * 60)
    if result.get("success"):
        print("   🎉 SUCCESS!")
        print(f"   👩‍🏫 {result.get('teacher')}")
        print(f"   📧 {result.get('email')}")
        print(f"   🏫 {result.get('school')}")
        print(f"   💼 {result.get('position')}")
        print()
        print("   ⏳ Wait 24-48 hours for manual review")
    else:
        print(f"   ❌ FAILED: {result.get('error')}")
    print("─" * 60)


if __name__ == "__main__":
    main()
