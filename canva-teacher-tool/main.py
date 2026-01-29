"""
Canva Education Teacher Document Generator
Generates UK Teacher documents for manual upload to canva.com/education

Supports:
- Employment Letter (UK school letterhead)
- Teacher ID Card (UK school staff ID)
- Teaching License (DfE QTS certificate)

Enhanced with:
- HTML templates rendered via Playwright (replaces PDF manipulation)
- Random noise injection to avoid template detection
- Slight blur and rotation for scan-like appearance
- Realistic handwritten signatures (Great Vibes font)

NOTE: Canva Education does NOT use SheerID for verification.
      You must upload documents manually at canva.com/education

Author: ThanhNguyxn
Based on: GitHub Issue #49 templates by cruzzzdev
HTML rewrite: HugeFrog24
"""

import sys
import json
import random
import asyncio
import base64
from pathlib import Path
from typing import Dict, Optional, Tuple, List
from datetime import datetime, timedelta
from io import BytesIO

try:
    from PIL import Image, ImageFilter
except ImportError:
    print("[ERROR] Pillow required. Install: pip install Pillow")
    sys.exit(1)

# Import noise generator from parent module if available
try:
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from doc_generator import add_simple_noise
except ImportError:

    def add_simple_noise(img, intensity=3):
        """Fallback: no-op noise function"""
        return img


# =============================================================================
# CONFIGURATION
# =============================================================================

BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "output"
DATA_DIR = BASE_DIR / "data"
TEMPLATES_DIR = BASE_DIR / "assets" / "templates"


# =============================================================================
# DATA: UK SCHOOLS
# =============================================================================

DEFAULT_UK_SCHOOLS = [
    {
        "name": "Leeds Grammar School",
        "address": "Alwoodley Gates, Harrogate Road",
        "town": "Leeds",
        "postcode": "LS17 8GS",
        "phone": "0113 229 1552",
        "lea": "Leeds LEA",
    },
    {
        "name": "Manchester Grammar School",
        "address": "Old Hall Lane",
        "town": "Manchester",
        "postcode": "M13 0XT",
        "phone": "0161 224 7201",
        "lea": "Manchester LEA",
    },
    {
        "name": "King Edward's School",
        "address": "Edgbaston Park Road",
        "town": "Birmingham",
        "postcode": "B15 2UA",
        "phone": "0121 472 1672",
        "lea": "Birmingham LEA",
    },
    {
        "name": "St Paul's School",
        "address": "Lonsdale Road",
        "town": "London",
        "postcode": "SW13 9JT",
        "phone": "020 8748 9162",
        "lea": "Richmond LEA",
    },
    {
        "name": "Westminster School",
        "address": "Little Dean's Yard",
        "town": "London",
        "postcode": "SW1P 3PF",
        "phone": "020 7963 1000",
        "lea": "Westminster LEA",
    },
    {
        "name": "Eton College",
        "address": "High Street",
        "town": "Windsor",
        "postcode": "SL4 6DW",
        "phone": "01753 370 100",
        "lea": "Windsor LEA",
    },
    {
        "name": "Harrow School",
        "address": "5 High Street",
        "town": "Harrow",
        "postcode": "HA1 3HP",
        "phone": "020 8872 8000",
        "lea": "Harrow LEA",
    },
    {
        "name": "Rugby School",
        "address": "Lawrence Sheriff Street",
        "town": "Rugby",
        "postcode": "CV22 5EH",
        "phone": "01788 556 216",
        "lea": "Warwickshire LEA",
    },
    {
        "name": "Cheltenham Ladies' College",
        "address": "Bayshill Road",
        "town": "Cheltenham",
        "postcode": "GL50 3EP",
        "phone": "01242 520 691",
        "lea": "Gloucestershire LEA",
    },
    {
        "name": "Dulwich College",
        "address": "Dulwich Common",
        "town": "London",
        "postcode": "SE21 7LD",
        "phone": "020 8693 3601",
        "lea": "Southwark LEA",
    },
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

UK_FIRST_NAMES = [
    "James",
    "Oliver",
    "Harry",
    "George",
    "Noah",
    "Jack",
    "Charlie",
    "Oscar",
    "William",
    "Henry",
    "Thomas",
    "Alfie",
    "Joshua",
    "Leo",
    "Archie",
    "Ethan",
    "Emma",
    "Olivia",
    "Amelia",
    "Isla",
    "Ava",
    "Mia",
    "Emily",
    "Isabella",
    "Sophia",
    "Grace",
    "Lily",
    "Chloe",
    "Ella",
    "Charlotte",
    "Sophie",
    "Alice",
]

UK_LAST_NAMES = [
    "Smith",
    "Jones",
    "Williams",
    "Taylor",
    "Brown",
    "Davies",
    "Evans",
    "Wilson",
    "Thomas",
    "Roberts",
    "Johnson",
    "Lewis",
    "Walker",
    "Robinson",
    "Wood",
    "Thompson",
    "White",
    "Watson",
    "Jackson",
    "Wright",
    "Green",
    "Harris",
    "Cooper",
    "King",
]


class SchoolDatabase:
    """UK Schools database with search and random selection."""

    def __init__(self):
        self.schools = self._load()

    def _load(self) -> List[Dict]:
        json_path = DATA_DIR / "uk_schools.json"
        if json_path.exists():
            try:
                return json.loads(json_path.read_text())
            except Exception:
                pass
        return DEFAULT_UK_SCHOOLS

    def random(self) -> Dict:
        return random.choice(self.schools)

    def search(self, query: str) -> Optional[Dict]:
        query_lower = query.lower()
        for school in self.schools:
            if query_lower in school["name"].lower():
                return school
        return None

    def list_names(self) -> List[str]:
        return [s["name"] for s in self.schools]


# =============================================================================
# DATA GENERATORS
# =============================================================================


def generate_name() -> Tuple[str, str]:
    return random.choice(UK_FIRST_NAMES), random.choice(UK_LAST_NAMES)


def generate_dob(min_age: int = 28, max_age: int = 55) -> str:
    """Generate DOB in DD/MM/YYYY format."""
    age = random.randint(min_age, max_age)
    year = datetime.now().year - age
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    return f"{day:02d}/{month:02d}/{year}"


def generate_staff_id() -> str:
    return f"STF-{random.randint(2020, 2025)}-{random.randint(100000, 999999)}"


def generate_trn() -> str:
    """Generate Teacher Reference Number."""
    return f"{random.randint(1000000, 9999999)}"


def generate_data_controller_no() -> str:
    return f"Z{random.randint(1000000, 9999999)}"


# =============================================================================
# TEMPLATE ENGINE
# =============================================================================


def load_template(name: str) -> str:
    """Load HTML template from file."""
    path = TEMPLATES_DIR / f"{name}.html"
    if not path.exists():
        raise FileNotFoundError(f"Template not found: {path}")
    return path.read_text(encoding="utf-8")


def load_photo_base64() -> str:
    """Load employee photo as base64 data URL, or return placeholder."""
    photo_path = TEMPLATES_DIR / "employee.png"
    if photo_path.exists():
        b64 = base64.b64encode(photo_path.read_bytes()).decode("utf-8")
        return f'<img src="data:image/png;base64,{b64}" style="width:100%;height:100%;object-fit:cover;border-radius:3px;">'
    return "PHOTO"


def load_chip_base64() -> str:
    """Load ID card chip image as base64 data URL."""
    chip_path = TEMPLATES_DIR / "chip.png"
    if chip_path.exists():
        b64 = base64.b64encode(chip_path.read_bytes()).decode("utf-8")
        return f'<img src="data:image/png;base64,{b64}">'
    return ""


def render_employment_letter(first: str, last: str, school: Dict, position: str) -> str:
    """Render employment letter template with data."""
    template = load_template("employment_letter")

    staff_id = generate_staff_id()
    start_date = (datetime.now() - timedelta(days=random.randint(180, 1800))).strftime(
        "%d %B %Y"
    )

    # Parse address
    addr_parts = school["address"].split(",")
    addr_line1 = addr_parts[0].strip()
    addr_line2 = f"{addr_parts[1].strip()}<br>" if len(addr_parts) > 1 else ""

    # Determine department from position
    if "Language" in position:
        department = "Modern Foreign Languages"
    else:
        department = position.replace("Head of ", "").replace(" Department", "")

    return template.format(
        school_name=school["name"],
        address_line1=addr_line1,
        address_line2=addr_line2,
        address_full=school["address"],
        town=school["town"],
        postcode=school["postcode"],
        phone=school["phone"],
        current_date=datetime.now().strftime("%d %B %Y"),
        year=datetime.now().year,
        staff_id=staff_id,
        full_name=f"{first} {last}",
        full_name_upper=f"{first.upper()} {last.upper()}",
        start_date=start_date,
        position=position,
        department=department,
        data_controller=generate_data_controller_no(),
        # Random signature rotation for realistic hand-signed look
        signature_rotation=round(random.uniform(-3, 3), 1),
    )


def render_teacher_id(
    first: str, last: str, school: Dict, position: str, dob: str
) -> str:
    """Render teacher ID card template with data."""
    template = load_template("teacher_id")

    # Extract short position for badge
    if " - " in position:
        pos_short = position.upper().split(" - ")[-1]
    else:
        pos_short = position.upper().replace("HEAD OF ", "").replace(" DEPARTMENT", "")

    return template.format(
        school_name_upper=school["name"].upper(),
        full_name_upper=f"{first.upper()} {last.upper()}",
        position_short=pos_short,
        dob=dob,
        # Issue date set to ~2 weeks ago to look established, not freshly minted
        issue_date=(datetime.now() - timedelta(days=random.randint(10, 20))).strftime(
            "%d/%m/%Y"
        ),
        expiry_date=(datetime.now() + timedelta(days=3 * 365)).strftime("%d/%m/%Y"),
        staff_id=generate_staff_id(),
        lea=school.get("lea", f"{school['town']} LEA"),
        photo_html=load_photo_base64(),
        chip_html=load_chip_base64(),
    )


def render_teaching_license(first: str, last: str) -> str:
    """Render teaching license (QTS certificate) template with data."""
    template = load_template("teaching_license")

    trn = generate_trn()
    award_date = (datetime.now() - timedelta(days=random.randint(365, 3650))).strftime(
        "%d %B %Y"
    )

    return template.format(
        full_name=f"{first} {last}",
        trn=trn,
        trn_short=trn[:6],
        award_date=award_date,
        year=datetime.now().year,
    )


# =============================================================================
# RENDERING ENGINE
# =============================================================================


async def html_to_png(html: str, width: int = 595, height: int = None) -> bytes:
    """Render HTML to PNG using Playwright."""
    try:
        from playwright.async_api import async_playwright
    except ImportError:
        print("[ERROR] Playwright required. Install:")
        print("   pip install playwright")
        print("   playwright install chromium")
        sys.exit(1)

    async with async_playwright() as p:
        browser = None
        try:
            browser = await p.chromium.launch()
            page = await browser.new_page(
                viewport={"width": width, "height": height or 842}
            )

            await page.set_content(html)
            await page.wait_for_load_state("networkidle")

            # Auto-detect content height if not specified
            if height is None:
                content_height = await page.evaluate("document.body.scrollHeight")
                await page.set_viewport_size(
                    {"width": width, "height": content_height + 50}
                )

            screenshot = await page.screenshot(type="png", full_page=True)
            return screenshot
        finally:
            if browser:
                await browser.close()


def apply_anti_detection(png_bytes: bytes, max_rotation: float = 2.0) -> bytes:
    """Add noise, slight blur, and rotation to avoid template detection.

    Args:
        png_bytes: Raw PNG image bytes
        max_rotation: Maximum rotation angle in degrees (use lower values for letters)
    """
    img = Image.open(BytesIO(png_bytes))

    if img.mode != "RGB":
        img = img.convert("RGB")

    # Add subtle noise
    img = add_simple_noise(img, intensity=random.randint(2, 4))

    # Occasional slight blur
    if random.random() > 0.6:
        img = img.filter(ImageFilter.GaussianBlur(radius=0.3))

    # Random rotation to simulate scan alignment (varies by document type)
    rotation_angle = random.uniform(-max_rotation, max_rotation)
    img = img.rotate(
        rotation_angle,
        resample=Image.Resampling.BICUBIC,
        expand=True,
        fillcolor=(255, 255, 255),
    )

    buf = BytesIO()
    img.save(buf, format="PNG", optimize=True)
    return buf.getvalue()


# =============================================================================
# DOCUMENT GENERATORS
# =============================================================================


async def generate_employment_letter(
    first: str, last: str, school: Dict, position: str
) -> bytes:
    """Generate employment letter as PNG."""
    html = render_employment_letter(first, last, school, position)
    png = await html_to_png(html, width=595, height=842)
    # Letters are placed carefully in scanner - minimal rotation
    return apply_anti_detection(png, max_rotation=0.75)


async def generate_teacher_id(
    first: str, last: str, school: Dict, position: str, dob: str
) -> bytes:
    """Generate teacher ID card as PNG."""
    html = render_teacher_id(first, last, school, position, dob)
    png = await html_to_png(html, width=380, height=260)
    # Small cards are harder to align - more rotation
    return apply_anti_detection(png, max_rotation=2.0)


async def generate_teaching_license(first: str, last: str) -> bytes:
    """Generate teaching license (QTS certificate) as PNG."""
    html = render_teaching_license(first, last)
    png = await html_to_png(html, width=560, height=780)
    # Certificate - moderate rotation
    return apply_anti_detection(png, max_rotation=1.0)


# =============================================================================
# CLI
# =============================================================================


async def main():
    import argparse

    # Fix Unicode output on Windows (cp1252 can't encode Vietnamese, etc.)
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
        except AttributeError:
            # Python < 3.7 fallback
            import io

            sys.stdout = io.TextIOWrapper(
                sys.stdout.buffer, encoding="utf-8", errors="replace"
            )
            sys.stderr = io.TextIOWrapper(
                sys.stderr.buffer, encoding="utf-8", errors="replace"
            )

    print()
    print("=" * 62)
    print("   Canva Education - UK Teacher Document Generator")
    print("=" * 62)
    print()
    print("   NOTE: Canva does NOT use SheerID for teacher verification.")
    print("   You must upload documents manually at: canva.com/education")
    print()

    parser = argparse.ArgumentParser(
        description="Generate UK Teacher documents for Canva Education"
    )
    parser.add_argument(
        "--doc-type",
        "-d",
        choices=["employment_letter", "teacher_id", "teaching_license", "all"],
        default="all",
        help="Document type to generate",
    )
    parser.add_argument("--name", "-n", help="Teacher name (format: 'First Last')")
    parser.add_argument("--school", "-s", help="School name (partial match)")
    parser.add_argument("--position", "-p", help="Teaching position")
    parser.add_argument(
        "--list-schools", action="store_true", help="List available schools"
    )
    args = parser.parse_args()

    schools = SchoolDatabase()

    # List schools mode
    if args.list_schools:
        print("   Available UK Schools:")
        for i, name in enumerate(schools.list_names(), 1):
            print(f"      {i}. {name}")
        return

    # Parse or generate data
    if args.name:
        parts = args.name.split()
        first, last = parts[0], parts[-1] if len(parts) > 1 else parts[0]
    else:
        first, last = generate_name()

    if args.school:
        school = schools.search(args.school)
        if not school:
            print(f"   [ERROR] School '{args.school}' not found. Use --list-schools")
            return
    else:
        school = schools.random()

    position = args.position or random.choice(TEACHING_POSITIONS)
    dob = generate_dob()

    print(f"   Teacher: {first} {last}")
    print(f"   School: {school['name']}")
    print(f"   Position: {position}")
    print(f"   DOB: {dob}")
    print()

    # Create output directory
    OUTPUT_DIR.mkdir(exist_ok=True)

    # Determine which documents to generate
    if args.doc_type == "all":
        doc_types = ["employment_letter", "teacher_id", "teaching_license"]
    else:
        doc_types = [args.doc_type]

    # Generate documents
    for doc_type in doc_types:
        try:
            print(f"   > Generating {doc_type.replace('_', ' ').title()}...")

            if doc_type == "employment_letter":
                doc = await generate_employment_letter(first, last, school, position)
            elif doc_type == "teacher_id":
                doc = await generate_teacher_id(first, last, school, position, dob)
            else:
                doc = await generate_teaching_license(first, last)

            output_path = OUTPUT_DIR / f"{doc_type}_{first}_{last}.png"
            output_path.write_bytes(doc)
            print(f"     [OK] Saved: {output_path.name} ({len(doc) / 1024:.1f} KB)")

        except Exception as e:
            print(f"     [ERROR] {e}")

    print()
    print("-" * 62)
    print("   Output files saved to: ./output/")
    print()
    print("   Next steps:")
    print("   1. Go to https://canva.com/education")
    print("   2. Click 'Get Verified' or 'I'm a Teacher'")
    print("   3. Upload one of the generated documents")
    print("   4. Wait 24-48 hours for review")
    print("-" * 62)


if __name__ == "__main__":
    asyncio.run(main())
