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

# Import anti-detection module
try:
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from anti_detect import get_headers, get_fingerprint, get_random_user_agent, random_delay as anti_delay
    HAS_ANTI_DETECT = True
    print("[INFO] Anti-detection module loaded")
except ImportError:
    HAS_ANTI_DETECT = False


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
# Get assets directory
ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")


def generate_from_pdf(first: str, last: str, dob: str) -> bytes:
    """Generate invoice by replacing text in PDF template using PyMuPDF"""
    import fitz  # PyMuPDF
    
    pdf_path = os.path.join(ASSETS_DIR, "docs.pdf")
    doc = fitz.open(pdf_path)
    page = doc[0]
    
    # Generate random values
    student_num = str(random.randint(5000000, 5999999))
    current_year = int(time.strftime("%Y"))
    academic_year = f"{current_year}-{current_year + 1}"
    tuition = f"€{random.randint(10, 12)},{random.randint(100, 999)}.00"
    
    # Text replacements: (old_text, new_text)
    replacements = [
        ("7777777", student_num),
        ("Safouane Rodermond", f"{first} {last}"),
        ("7 July 2005", dob),
        ("2025-2026", academic_year),
        ("THANH NGUYXN", f"{first.upper()} {last.upper()}"),
        ("€11,200.00", tuition),
    ]
    
    # Collect positions before redacting
    positions = {}
    for old_text, new_text in replacements:
        areas = page.search_for(old_text)
        if areas:
            positions[old_text] = (areas[0], new_text)
    
    # Apply redactions (white boxes over old text)
    for old_text, new_text in replacements:
        areas = page.search_for(old_text)
        for rect in areas:
            page.add_redact_annot(rect, fill=(1, 1, 1))
    page.apply_redactions()
    
    # Insert new text at saved positions
    for old_text, (rect, new_text) in positions.items():
        text_point = fitz.Point(rect.x0, rect.y1 - 2)
        page.insert_text(text_point, new_text, fontsize=10, color=(0, 0, 0))
    
    # Convert to PNG
    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # 2x for high quality
    
    # Convert pixmap to bytes
    return pix.tobytes("png")


# Legacy function - now uses PDF method
def generate_from_template(first: str, last: str, dob: str) -> bytes:
    """Generate invoice from PDF template (wrapper for generate_from_pdf)"""
    return generate_from_pdf(first, last, dob)


def generate_groningen_invoice(first: str, last: str, dob: str) -> bytes:
    """Generate Groningen tuition fee invoice (EXACT match to Canva template)"""
    w, h = 595, 842  # A4 size at 72 DPI
    img = Image.new("RGB", (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    try:
        font_uni = ImageFont.truetype("arial.ttf", 16)
        font_header = ImageFont.truetype("arial.ttf", 10)
        font_title = ImageFont.truetype("arial.ttf", 12)
        font_text = ImageFont.truetype("arial.ttf", 10)
        font_small = ImageFont.truetype("arial.ttf", 8)
        font_bold = ImageFont.truetype("arialbd.ttf", 10)
    except:
        font_uni = font_header = font_title = font_text = font_small = font_bold = ImageFont.load_default()
    
    # Colors
    rug_red = (204, 0, 0)
    black = (0, 0, 0)
    gray = (100, 100, 100)
    
    # ===== HEADER - LOGO =====
    try:
        logo_path = os.path.join(ASSETS_DIR, "groningen_logo.png")
        logo = Image.open(logo_path)
        # Resize logo to fit header (width ~180px)
        logo_ratio = logo.width / logo.height
        logo_height = 50
        logo_width = int(logo_height * logo_ratio)
        logo = logo.resize((logo_width, logo_height), Image.Resampling.LANCZOS)
        img.paste(logo, (30, 25), logo if logo.mode == 'RGBA' else None)
    except:
        # Fallback to text if logo not found
        draw.rectangle([(40, 30), (65, 70)], fill=rug_red)
        draw.text((70, 35), "university of", fill=rug_red, font=font_header)
        draw.text((70, 48), "groningen", fill=rug_red, font=font_uni)
    
    # Middle header
    draw.text((200, 35), "university services", fill=gray, font=font_header)
    
    # Right header
    draw.text((380, 30), "student information and", fill=gray, font=font_header)
    draw.text((380, 42), "administration", fill=gray, font=font_header)
    draw.text((380, 56), "050 363 8233", fill=gray, font=font_small)
    draw.text((380, 68), "www.rug.nl/insandouts", fill=gray, font=font_small)
    
    # Address block (right)
    draw.text((420, 90), "Broerstraat 5", fill=gray, font=font_small)
    draw.text((420, 100), "Groningen", fill=gray, font=font_small)
    draw.text((420, 110), "PO Box 72", fill=gray, font=font_small)
    draw.text((420, 120), "9700 AB Groningen", fill=gray, font=font_small)
    draw.text((420, 130), "The Netherlands", fill=gray, font=font_small)
    draw.text((420, 145), "www.rug.nl/SIA", fill=gray, font=font_small)
    
    # Recipient name (left)
    name_full = f"{first.upper()} {last.upper()}"
    draw.text((40, 100), name_full, fill=black, font=font_title)
    
    # ===== DATE & REFERENCE LINE =====
    current_year = int(time.strftime("%Y"))
    invoice_date = f"{random.randint(1, 28)} {'January February March April May June July August September October November December'.split()[random.randint(0, 11)]} {current_year}"
    ref_code = f"5Re9fe6r4en6ce{random.randint(10, 99)}"
    
    draw.text((40, 180), "Date", fill=gray, font=font_small)
    draw.text((200, 180), "Concerning", fill=gray, font=font_small)
    draw.text((450, 180), ref_code, fill=gray, font=font_small)
    
    draw.text((40, 192), invoice_date, fill=black, font=font_text)
    draw.text((200, 192), "Tuition Fees", fill=black, font=font_text)
    
    # ===== INVOICE TITLE =====
    draw.text((40, 215), "Invoice tuition fees", fill=black, font=font_title)
    
    # ===== STUDENT INFO =====
    student_num = str(random.randint(5000000, 5999999))
    academic_year = f"{current_year}-{current_year + 1}"
    
    y = 240
    labels = ["Student number:", "Name:", "Date of birth:", "For academic year:", "For the study programme(s):", "Tuition fees:"]
    values = [
        student_num,
        f"{first} {last}",
        dob.replace("-", " ").replace("2005", "2005"),  # Format: 15 May 2005
        academic_year,
        "Bachelor International Business (English taught) Full-time\nGroningen",
        f"€{random.randint(10, 12)},{random.randint(100, 999)}.00"
    ]
    
    for label, value in zip(labels, values):
        draw.text((40, y), label, fill=black, font=font_text)
        if "\n" in value:
            lines = value.split("\n")
            draw.text((180, y), lines[0], fill=black, font=font_text)
            draw.text((180, y + 12), lines[1], fill=black, font=font_text)
            y += 12
        else:
            draw.text((180, y), value, fill=black, font=font_text)
        y += 18
    
    # ===== TRANSFER DETAILS =====
    y += 15
    draw.text((40, y), "Transfer details", fill=black, font=font_bold)
    y += 18
    
    iban = f"NL{random.randint(10, 99)}MLKP{random.randint(1000000000, 9999999999)}"
    transfer_labels = ["Bank account holder:", "IBAN:", "Bank name:", "BIC/SWIFT code:", "Bank address:", "Payment reference:"]
    transfer_values = [
        f"Rijksuniversiteit Groningen {iban} ABN",
        f"AMRO ABNANL2A Gustav Mahlerlaan 10, 1082 PP",
        "Amsterdam, the Netherlands Tuition fees S5643302, Y.",
        "Amman",
        "",
        ""
    ]
    
    for label, value in zip(transfer_labels, transfer_values):
        draw.text((40, y), label, fill=black, font=font_text)
        draw.text((130, y), value, fill=black, font=font_text)
        y += 14
    
    # ===== WARNING TEXT (red) =====
    y += 20
    draw.text((40, y), "Make sure to transfer the tuition fees before the starting date of the programme.", fill=rug_red, font=font_text)
    y += 20
    
    warning_text = "Please note that if you are a non-EU student who needs an MVV and/or Dutch residence permit,\nplease uphold the deadline that the Immigration Service Desk of the University of Groningen\nhas given to you."
    for line in warning_text.split("\n"):
        draw.text((40, y), line, fill=black, font=font_small)
        y += 12
    
    # ===== SIGNATURE =====
    y += 20
    try:
        sig_path = os.path.join(ASSETS_DIR, "signature.png")
        sig = Image.open(sig_path)
        # Resize signature to fit (width ~100px)
        sig_ratio = sig.width / sig.height
        sig_height = 40
        sig_width = int(sig_height * sig_ratio)
        sig = sig.resize((sig_width, sig_height), Image.Resampling.LANCZOS)
        img.paste(sig, (40, y), sig if sig.mode == 'RGBA' else None)
        y += sig_height + 10
    except:
        # Fallback to lines if signature not found
        draw.line([(40, y), (120, y + 20)], fill=black, width=1)
        draw.line([(60, y + 5), (100, y + 15)], fill=black, width=1)
        y += 30
    
    draw.text((40, y), "T.K. Idema", fill=black, font=font_text)
    y += 12
    draw.text((40, y), "Head of the Student Information and Administration", fill=black, font=font_text)
    
    # ===== PAGE NUMBER =====
    draw.text((40, h - 30), "1 - 1", fill=gray, font=font_small)
    
    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


# Format DOB for display
def format_dob_display(dob: str) -> str:
    """Convert 2005-05-15 to 15 May 2005"""
    months = ["January", "February", "March", "April", "May", "June", 
              "July", "August", "September", "October", "November", "December"]
    parts = dob.split("-")
    if len(parts) == 3:
        year, month, day = parts
        return f"{int(day)} {months[int(month)-1]} {year}"
    return dob


# Legacy alias
def generate_student_id(first: str, last: str, school: str) -> bytes:
    """Generate document for verification - now uses Groningen invoice"""
    # Generate DOB for ~2005 (student age)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    dob_display = format_dob_display(f"2005-{month:02d}-{day:02d}")
    return generate_from_pdf(first, last, dob_display)


# ============ VERIFIER ============
class PerplexityVerifier:
    """Perplexity Student Verification with enhanced features"""
    
    def __init__(self, url: str):
        self.url = url
        self.vid = self._parse_id(url)
        self.program_id = self._parse_program_id(url)
        self.fingerprint = generate_fingerprint()
        self.client = httpx.Client(
            timeout=30,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "application/json",
                "Accept-Language": "en-US,en;q=0.9",
                "Origin": "https://services.sheerid.com",
                "Referer": "https://services.sheerid.com/"
            }
        )
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

    def search_organization(self, query: str) -> Optional[Dict]:
        """Search for organization ID dynamically"""
        print(f"   🔍 Searching for '{query}'...")
        # Use global organization search endpoint
        endpoint = f"/organization?searchTerm={query}&programId={self.program_id}"
        data, status = self._request("GET", endpoint)
        
        if status != 200:
            print(f"     ⚠️ Search API Error: {status} - {data}")
            return None
            
        if isinstance(data, list):
            print(f"     ℹ️  Found {len(data)} results")
            if len(data) > 0:
                return data[0]
        else:
            print(f"     ⚠️ Unexpected search response format: {type(data)}")
            
        return None
    
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
            # Always use Groningen
            if not self.org:
                # Try to search dynamically first to get correct ID
                # Try Dutch name first as seen in user screenshot
                found_org = self.search_organization("Rijksuniversiteit Groningen")
                if not found_org:
                    found_org = self.search_organization("University of Groningen")
                if not found_org:
                    found_org = self.search_organization("Groningen")
                
                if found_org:
                    self.org = found_org
                    # Ensure domain is set (search result might not have it, but we know it's rug.nl)
                    if "domain" not in self.org:
                        self.org["domain"] = "rug.nl"
                    print(f"     ✅ Found Org ID: {self.org['id']}")
                else:
                    print("     ⚠️ Search failed, using hardcoded fallback...")
                    self.org = select_groningen()

            email = generate_email(first, last, self.org.get("domain", "rug.nl"))
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
                    }
                }
                
                data, status = self._request("POST", f"/verification/{self.vid}/step/collectStudentPersonalInfo", body)
                
                if status != 200:
                    stats.record(self.org["name"], False)
                    print(f"     ❌ Error details: {data}")
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
    args = parser.parse_args()
    
    # Get URL
    if args.url:
        url = args.url
    else:
        print("   💡 TIP: To get the verification URL:")
        print("   1. Open Developer Tools (F12) -> Network tab")
        print("   2. Filter by 'sheerid'")
        print("   3. Find request starting with 'verification' or ID")
        print("   4. Right-click -> Copy URL")
        print()
        url = input("   Enter verification URL: ").strip()
    
    if not url or "sheerid.com" not in url:
        print("\n   ❌ Invalid URL. Must contain sheerid.com")
        return
    
    # Always use Groningen logic
    print("\n   🇳🇱 Using GRONINGEN BYPASS strategy!")
    print("   Requires: Netherlands IP + SSO portal cancel")
    
    print("\n   ⏳ Processing...")
    
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
