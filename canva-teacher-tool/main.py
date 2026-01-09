"""
Canva Education Teacher Document Generator
Generates UK Teacher documents for manual upload to canva.com/education

Supports:
- Employment Letter (UK school letterhead)
- Teacher ID Card (UK school staff ID)
- Teaching License (DfE QTS certificate)

NOTE: Canva Education does NOT use SheerID for verification.
      You must upload documents manually at canva.com/education

Author: ThanhNguyxn
Based on: GitHub Issue #49 templates by cruzzzdev
"""

import os
import sys
import json
import random
from pathlib import Path
from typing import Dict, Optional, Tuple, List
from datetime import datetime, timedelta

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


# ============ CONFIG ============
ASSETS_DIR = Path(__file__).parent / "assets"
TEMPLATES_DIR = ASSETS_DIR / "templates"
DATA_DIR = Path(__file__).parent / "data"
OUTPUT_DIR = Path(__file__).parent / "output"


# ============ UK SCHOOLS DATABASE ============
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
        json_path = DATA_DIR / "uk_schools.json"
        if json_path.exists():
            try:
                return json.loads(json_path.read_text())
            except:
                pass
        return DEFAULT_UK_SCHOOLS
    
    def random_school(self) -> Dict:
        return random.choice(self.schools)
    
    def search(self, query: str) -> Optional[Dict]:
        query_lower = query.lower()
        for school in self.schools:
            if query_lower in school["name"].lower():
                return school
        return None
    
    def list_schools(self) -> List[str]:
        return [s["name"] for s in self.schools]


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
    "Lee", "Martin", "Clarke", "James", "Morgan", "Hughes", "Edwards", "Hill"
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
]


def generate_name() -> Tuple[str, str]:
    return random.choice(UK_FIRST_NAMES), random.choice(UK_LAST_NAMES)


def generate_dob(min_age: int = 28, max_age: int = 55) -> str:
    """Generate DOB for teacher (DD/MM/YYYY format)"""
    today = datetime.now()
    age = random.randint(min_age, max_age)
    birth_year = today.year - age
    birth_month = random.randint(1, 12)
    birth_day = random.randint(1, 28)
    return f"{birth_day:02d}/{birth_month:02d}/{birth_year}"


def generate_staff_id() -> str:
    return f"STF-{random.randint(2020, 2025)}-{random.randint(100000, 999999)}"


def generate_data_controller_no() -> str:
    return f"Z{random.randint(1000000, 9999999)}"


# ============ DOCUMENT GENERATORS ============

def generate_employment_letter(first: str, last: str, school: Dict, position: str) -> bytes:
    """Generate Employment Letter from PDF template"""
    pdf_path = TEMPLATES_DIR / "Employment_Letter.pdf"
    if not pdf_path.exists():
        raise FileNotFoundError(f"Template not found: {pdf_path}")
    
    doc = fitz.open(str(pdf_path))
    page = doc[0]
    
    current_date = datetime.now().strftime("%d %B %Y")
    data_controller = generate_data_controller_no()
    
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
    
    for old_text, new_text in replacements:
        if not new_text:
            continue
        areas = page.search_for(old_text)
        for rect in areas:
            page.add_redact_annot(rect, fill=(1, 1, 1))
    
    page.apply_redactions()
    
    pdf_bytes = doc.tobytes()
    doc.close()
    
    doc = fitz.open("pdf", pdf_bytes)
    page = doc[0]
    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
    doc.close()
    
    return pix.tobytes("png")


def generate_teacher_id_card(first: str, last: str, school: Dict, position: str, dob: str) -> bytes:
    """Generate Teacher ID Card from PDF template"""
    pdf_path = TEMPLATES_DIR / "Teacher_ID_Card.pdf"
    if not pdf_path.exists():
        raise FileNotFoundError(f"Template not found: {pdf_path}")
    
    doc = fitz.open(str(pdf_path))
    page = doc[0]
    
    staff_id = generate_staff_id()
    issue_date = datetime.now().strftime("%d/%m/%Y")
    expiry_date = (datetime.now() + timedelta(days=3*365)).strftime("%d/%m/%Y")
    
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
    
    for old_text, new_text in replacements:
        areas = page.search_for(old_text)
        for rect in areas:
            page.add_redact_annot(rect, fill=(1, 1, 1))
    
    page.apply_redactions()
    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
    doc.close()
    
    return pix.tobytes("png")


def generate_teaching_license(first: str, last: str) -> bytes:
    """Generate Teaching License (QTS Certificate) from PDF template"""
    pdf_path = TEMPLATES_DIR / "Teaching_License.pdf"
    if not pdf_path.exists():
        raise FileNotFoundError(f"Template not found: {pdf_path}")
    
    doc = fitz.open(str(pdf_path))
    page = doc[0]
    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
    doc.close()
    
    return pix.tobytes("png")


# ============ MAIN ============

def main():
    import argparse
    
    print()
    print("╔" + "═" * 60 + "╗")
    print("║" + " 🎓 Canva Education - UK Teacher Document Generator".center(60) + "║")
    print("╚" + "═" * 60 + "╝")
    print()
    print("   ⚠️  NOTE: Canva does NOT use SheerID for teacher verification.")
    print("   You must upload documents manually at: canva.com/education")
    print()
    
    parser = argparse.ArgumentParser(description="Generate UK Teacher documents for Canva Education")
    parser.add_argument("--doc-type", "-d", choices=["employment_letter", "teacher_id", "teaching_license", "all"],
                        default="all", help="Document type to generate (default: all)")
    parser.add_argument("--name", "-n", help="Teacher name (format: 'First Last')")
    parser.add_argument("--school", "-s", help="School name (from database)")
    parser.add_argument("--position", "-p", help="Teaching position")
    parser.add_argument("--list-schools", action="store_true", help="List available schools")
    args = parser.parse_args()
    
    # List schools mode
    if args.list_schools:
        print("   📚 Available UK Schools:")
        for i, name in enumerate(uk_schools.list_schools(), 1):
            print(f"      {i}. {name}")
        return
    
    # Generate info
    if args.name:
        parts = args.name.split()
        first, last = parts[0], parts[-1] if len(parts) > 1 else parts[0]
    else:
        first, last = generate_name()
    
    if args.school:
        school = uk_schools.search(args.school)
        if not school:
            print(f"   ❌ School '{args.school}' not found. Use --list-schools to see options.")
            return
    else:
        school = uk_schools.random_school()
    
    position = args.position or random.choice(TEACHING_POSITIONS)
    dob = generate_dob()
    
    print(f"   👩‍🏫 Teacher: {first} {last}")
    print(f"   🏫 School: {school['name']}")
    print(f"   💼 Position: {position}")
    print(f"   🎂 DOB: {dob}")
    print()
    
    # Create output directory
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    # Generate documents
    doc_types = ["employment_letter", "teacher_id", "teaching_license"] if args.doc_type == "all" else [args.doc_type]
    
    generated = []
    for doc_type in doc_types:
        try:
            print(f"   ▶ Generating {doc_type.replace('_', ' ').title()}...")
            
            if doc_type == "employment_letter":
                doc = generate_employment_letter(first, last, school, position)
            elif doc_type == "teacher_id":
                doc = generate_teacher_id_card(first, last, school, position, dob)
            else:
                doc = generate_teaching_license(first, last)
            
            output_path = OUTPUT_DIR / f"{doc_type}_{first}_{last}.png"
            output_path.write_bytes(doc)
            generated.append(output_path)
            print(f"     ✅ Saved: {output_path.name} ({len(doc)/1024:.1f} KB)")
            
        except Exception as e:
            print(f"     ❌ Error: {e}")
    
    print()
    print("─" * 62)
    print("   📁 Output files saved to: ./output/")
    print()
    print("   📤 Next steps:")
    print("   1. Go to https://canva.com/education")
    print("   2. Click 'Get Verified' or 'I'm a Teacher'")
    print("   3. Upload one of the generated documents")
    print("   4. Wait 24-48 hours for review")
    print("─" * 62)


if __name__ == "__main__":
    main()
