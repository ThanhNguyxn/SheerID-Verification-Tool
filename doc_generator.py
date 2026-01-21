"""
Enhanced Document Generator Module
Shared module for generating verification documents with anti-detection features

Features:
- Random noise injection to avoid template detection
- Color variation for uniqueness
- Dynamic layout positioning
- Multiple document types (Student ID, Transcript, Teacher Badge, Invoice)
- Font variation and randomization

Usage:
    from doc_generator import generate_student_id, generate_transcript, generate_teacher_badge
    
    # Generate student ID with noise
    doc_bytes = generate_student_id("John", "Doe", "MIT")
    
    # Generate transcript
    doc_bytes = generate_transcript("John", "Doe", "2005-03-15", "MIT")

Author: ThanhNguyxn
"""

import random
import time
import hashlib
from io import BytesIO
from typing import Tuple, Optional

try:
    from PIL import Image, ImageDraw, ImageFont, ImageFilter
except ImportError:
    print("❌ Error: Pillow required. Install: pip install Pillow")
    raise


# ============ COLOR PALETTES ============
# Multiple color schemes to avoid detection
COLOR_SCHEMES = [
    # Classic blue
    {"primary": (0, 51, 102), "secondary": (51, 102, 153), "accent": (255, 255, 255), "text": (51, 51, 51)},
    # Dark blue
    {"primary": (25, 45, 85), "secondary": (45, 85, 125), "accent": (255, 255, 255), "text": (40, 40, 40)},
    # Navy
    {"primary": (0, 0, 80), "secondary": (30, 30, 110), "accent": (255, 255, 255), "text": (45, 45, 45)},
    # Maroon
    {"primary": (128, 0, 32), "secondary": (160, 40, 72), "accent": (255, 255, 255), "text": (50, 50, 50)},
    # Forest Green
    {"primary": (34, 85, 51), "secondary": (51, 119, 68), "accent": (255, 255, 255), "text": (48, 48, 48)},
    # Purple
    {"primary": (75, 0, 130), "secondary": (100, 30, 160), "accent": (255, 255, 255), "text": (55, 55, 55)},
]


def get_random_color_scheme() -> dict:
    """Get a random color scheme"""
    return random.choice(COLOR_SCHEMES)


def add_noise(img: Image.Image, intensity: float = 0.02) -> Image.Image:
    """
    Add subtle noise to image to avoid template detection
    
    Args:
        img: PIL Image object
        intensity: Noise intensity (0.0 - 1.0)
    
    Returns:
        Image with noise applied
    """
    import numpy as np
    
    # Convert to numpy array
    arr = np.array(img, dtype=np.float32)
    
    # Generate noise
    noise = np.random.normal(0, intensity * 255, arr.shape)
    
    # Add noise
    arr = arr + noise
    
    # Clip values
    arr = np.clip(arr, 0, 255).astype(np.uint8)
    
    return Image.fromarray(arr)


def add_simple_noise(img: Image.Image, intensity: int = 3) -> Image.Image:
    """
    Add simple noise without numpy dependency
    
    Args:
        img: PIL Image object
        intensity: Max pixel variation (+/-)
    
    Returns:
        Image with noise applied
    """
    pixels = img.load()
    width, height = img.size
    
    # Only modify a subset of pixels for performance
    for _ in range(width * height // 10):
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        
        try:
            r, g, b = pixels[x, y][:3]
            r = max(0, min(255, r + random.randint(-intensity, intensity)))
            g = max(0, min(255, g + random.randint(-intensity, intensity)))
            b = max(0, min(255, b + random.randint(-intensity, intensity)))
            
            if len(pixels[x, y]) == 4:
                pixels[x, y] = (r, g, b, pixels[x, y][3])
            else:
                pixels[x, y] = (r, g, b)
        except:
            pass
    
    return img


def randomize_position(base_x: int, base_y: int, variance: int = 3) -> Tuple[int, int]:
    """Add small random offset to position"""
    return (
        base_x + random.randint(-variance, variance),
        base_y + random.randint(-variance, variance)
    )


def get_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    """
    Get font with fallback to default
    
    Args:
        size: Font size
        bold: Whether to use bold font
    
    Returns:
        ImageFont object
    """
    # Try different font paths
    font_paths = [
        "arial.ttf",
        "Arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "C:\\Windows\\Fonts\\arial.ttf",
    ]
    
    if bold:
        font_paths = [
            "arialbd.ttf",
            "Arial Bold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "C:\\Windows\\Fonts\\arialbd.ttf",
        ] + font_paths
    
    for path in font_paths:
        try:
            return ImageFont.truetype(path, size)
        except:
            continue
    
    return ImageFont.load_default()


def generate_barcode(draw: ImageDraw.Draw, x: int, y: int, width: int = 140, height_range: Tuple[int, int] = (30, 50)):
    """Generate fake barcode pattern"""
    bar_count = random.randint(20, 30)
    bar_width = width // bar_count
    
    for i in range(bar_count):
        if random.random() > 0.3:  # Not all bars
            bar_x = x + i * bar_width
            bar_height = random.randint(height_range[0], height_range[1])
            bar_w = random.randint(1, max(2, bar_width - 1))
            draw.rectangle([(bar_x, y), (bar_x + bar_w, y + bar_height)], fill=(0, 0, 0))


def generate_qr_placeholder(draw: ImageDraw.Draw, x: int, y: int, size: int = 60):
    """Generate fake QR code pattern"""
    cell_size = size // 10
    
    # Draw border
    draw.rectangle([(x, y), (x + size, y + size)], outline=(0, 0, 0), width=2)
    
    # Draw random pattern
    for i in range(10):
        for j in range(10):
            if random.random() > 0.5:
                cell_x = x + i * cell_size
                cell_y = y + j * cell_size
                draw.rectangle([(cell_x, cell_y), (cell_x + cell_size, cell_y + cell_size)], fill=(0, 0, 0))
    
    # Draw position markers (corners)
    for corner in [(x, y), (x + size - 20, y), (x, y + size - 20)]:
        draw.rectangle([corner, (corner[0] + 20, corner[1] + 20)], fill=(0, 0, 0))
        draw.rectangle([(corner[0] + 5, corner[1] + 5), (corner[0] + 15, corner[1] + 15)], fill=(255, 255, 255))
        draw.rectangle([(corner[0] + 8, corner[1] + 8), (corner[0] + 12, corner[1] + 12)], fill=(0, 0, 0))


def generate_student_id(first: str, last: str, school: str, add_noise: bool = True) -> bytes:
    """
    Generate fake student ID card with anti-detection features
    
    Args:
        first: First name
        last: Last name
        school: School name
        add_noise: Whether to add noise for anti-detection
    
    Returns:
        PNG image bytes
    """
    # Randomize dimensions slightly
    w = random.randint(640, 660)
    h = random.randint(390, 410)
    
    # Random background color (slight off-white)
    bg_color = (
        255 - random.randint(0, 8),
        255 - random.randint(0, 8),
        255 - random.randint(0, 8)
    )
    
    img = Image.new("RGB", (w, h), bg_color)
    draw = ImageDraw.Draw(img)
    
    # Get random color scheme
    colors = get_random_color_scheme()
    
    # Get fonts
    font_lg = get_font(random.randint(22, 26))
    font_md = get_font(random.randint(16, 20))
    font_sm = get_font(random.randint(12, 15))
    
    # Header with slight position variance
    header_height = random.randint(55, 65)
    draw.rectangle([(0, 0), (w, header_height)], fill=colors["primary"])
    
    title = random.choice([
        "STUDENT IDENTIFICATION CARD",
        "STUDENT ID CARD",
        "UNIVERSITY STUDENT CARD",
        "STUDENT IDENTIFICATION"
    ])
    title_pos = randomize_position(w // 2, header_height // 2, variance=2)
    draw.text(title_pos, title, fill=colors["accent"], font=font_lg, anchor="mm")
    
    # School name
    school_y = header_height + random.randint(25, 35)
    school_display = school[:50] if len(school) > 50 else school
    draw.text((w // 2, school_y), school_display, fill=colors["primary"], font=font_md, anchor="mm")
    
    # Photo placeholder
    photo_x = random.randint(25, 35)
    photo_y = random.randint(115, 125)
    photo_w = random.randint(115, 125)
    photo_h = random.randint(155, 165)
    draw.rectangle([(photo_x, photo_y), (photo_x + photo_w, photo_y + photo_h)], 
                   outline=(180, 180, 180), width=2)
    draw.text((photo_x + photo_w // 2, photo_y + photo_h // 2), 
              "PHOTO", fill=(180, 180, 180), font=font_md, anchor="mm")
    
    # Student info
    student_id = f"STU{random.randint(100000, 999999)}"
    current_year = int(time.strftime('%Y'))
    
    info_x = photo_x + photo_w + random.randint(20, 30)
    info_y = random.randint(125, 135)
    
    majors = ["Computer Science", "Business Administration", "Engineering", 
              "Mathematics", "Biology", "Economics", "Psychology", "Chemistry"]
    
    info_lines = [
        f"Name: {first} {last}",
        f"ID: {student_id}",
        f"Status: {random.choice(['Full-time Student', 'Undergraduate', 'Graduate Student'])}",
        f"Major: {random.choice(majors)}",
        f"Valid: {current_year}-{current_year + 1}"
    ]
    
    for line in info_lines:
        pos = randomize_position(info_x, info_y, variance=1)
        draw.text(pos, line, fill=colors["text"], font=font_md)
        info_y += random.randint(26, 32)
    
    # Footer
    footer_y = h - random.randint(38, 45)
    draw.rectangle([(0, footer_y), (w, h)], fill=colors["primary"])
    footer_text = random.choice([
        "Property of University",
        "Official Student Identification",
        "This card is property of the institution"
    ])
    draw.text((w // 2, (footer_y + h) // 2), footer_text, 
              fill=colors["accent"], font=font_sm, anchor="mm")
    
    # Barcode
    barcode_x = w - random.randint(160, 180)
    barcode_y = photo_y + photo_h - random.randint(55, 65)
    generate_barcode(draw, barcode_x, barcode_y)
    
    # Add noise if requested
    if add_noise:
        img = add_simple_noise(img, intensity=random.randint(2, 4))
    
    # Slight blur for more realistic look
    if random.random() > 0.5:
        img = img.filter(ImageFilter.GaussianBlur(radius=0.3))
    
    # Save
    buf = BytesIO()
    # Random quality for variation
    img.save(buf, format="PNG", optimize=True)
    return buf.getvalue()


def generate_transcript(first: str, last: str, dob: str, school: str, add_noise: bool = True) -> bytes:
    """
    Generate fake academic transcript
    
    Args:
        first: First name
        last: Last name
        dob: Date of birth (YYYY-MM-DD)
        school: School name
        add_noise: Whether to add noise
    
    Returns:
        PNG image bytes
    """
    # A4-ish proportions
    w = random.randint(800, 850)
    h = random.randint(1100, 1150)
    
    bg_color = (255 - random.randint(0, 5), 255 - random.randint(0, 5), 255 - random.randint(0, 5))
    img = Image.new("RGB", (w, h), bg_color)
    draw = ImageDraw.Draw(img)
    
    colors = get_random_color_scheme()
    
    font_title = get_font(random.randint(24, 28), bold=True)
    font_header = get_font(random.randint(18, 22), bold=True)
    font_text = get_font(random.randint(12, 14))
    font_small = get_font(random.randint(10, 12))
    
    y = 50
    
    # School name header
    draw.text((w // 2, y), school.upper(), fill=colors["primary"], font=font_title, anchor="mm")
    y += 40
    
    # Title
    draw.text((w // 2, y), "OFFICIAL ACADEMIC TRANSCRIPT", fill=colors["text"], font=font_header, anchor="mm")
    y += 50
    
    # Horizontal line
    draw.line([(50, y), (w - 50, y)], fill=colors["primary"], width=2)
    y += 30
    
    # Student info
    student_id = f"S{random.randint(1000000, 9999999)}"
    current_year = int(time.strftime('%Y'))
    
    info = [
        ("Name:", f"{first} {last}"),
        ("Student ID:", student_id),
        ("Date of Birth:", dob),
        ("Program:", random.choice(["Bachelor of Science", "Bachelor of Arts", "Master of Science"])),
        ("Major:", random.choice(["Computer Science", "Business", "Engineering", "Mathematics"])),
        ("Academic Year:", f"{current_year - 1}-{current_year}"),
    ]
    
    for label, value in info:
        draw.text((60, y), label, fill=colors["text"], font=font_text)
        draw.text((200, y), value, fill=colors["text"], font=font_text)
        y += 25
    
    y += 20
    
    # Course table header
    draw.rectangle([(50, y), (w - 50, y + 30)], fill=colors["primary"])
    draw.text((60, y + 8), "COURSE", fill=colors["accent"], font=font_text)
    draw.text((400, y + 8), "CREDITS", fill=colors["accent"], font=font_text)
    draw.text((500, y + 8), "GRADE", fill=colors["accent"], font=font_text)
    draw.text((600, y + 8), "POINTS", fill=colors["accent"], font=font_text)
    y += 35
    
    # Generate random courses
    courses = [
        "Introduction to Computer Science",
        "Calculus I",
        "English Composition",
        "General Chemistry",
        "Physics I",
        "Data Structures",
        "Linear Algebra",
        "Statistics",
        "Database Systems",
        "Software Engineering",
    ]
    
    random.shuffle(courses)
    grades = ["A", "A-", "B+", "B", "B-", "A", "A-"]
    total_credits = 0
    total_points = 0
    
    for course in courses[:random.randint(6, 8)]:
        credits = random.choice([3, 4])
        grade = random.choice(grades)
        grade_points = {"A": 4.0, "A-": 3.7, "B+": 3.3, "B": 3.0, "B-": 2.7}[grade]
        points = credits * grade_points
        
        total_credits += credits
        total_points += points
        
        draw.text((60, y), course, fill=colors["text"], font=font_text)
        draw.text((420, y), str(credits), fill=colors["text"], font=font_text)
        draw.text((520, y), grade, fill=colors["text"], font=font_text)
        draw.text((620, y), f"{points:.1f}", fill=colors["text"], font=font_text)
        y += 22
    
    # GPA
    gpa = total_points / total_credits if total_credits > 0 else 0
    y += 20
    draw.line([(50, y), (w - 50, y)], fill=colors["primary"], width=1)
    y += 15
    draw.text((60, y), f"TOTAL CREDITS: {total_credits}", fill=colors["text"], font=font_text)
    draw.text((400, y), f"GPA: {gpa:.2f}", fill=colors["primary"], font=font_header)
    
    # Footer
    y = h - 100
    draw.text((60, y), "This is an official transcript issued by the Registrar's Office.", 
              fill=colors["text"], font=font_small)
    y += 20
    draw.text((60, y), f"Issue Date: {time.strftime('%B %d, %Y')}", fill=colors["text"], font=font_small)
    
    # Add noise
    if add_noise:
        img = add_simple_noise(img, intensity=random.randint(2, 4))
    
    buf = BytesIO()
    img.save(buf, format="PNG", optimize=True)
    return buf.getvalue()


def generate_teacher_badge(first: str, last: str, school: str, add_noise: bool = True) -> bytes:
    """
    Generate fake teacher/faculty badge
    
    Args:
        first: First name
        last: Last name
        school: School name
        add_noise: Whether to add noise
    
    Returns:
        PNG image bytes
    """
    w = random.randint(490, 510)
    h = random.randint(340, 360)
    
    bg_color = (255 - random.randint(0, 8), 255 - random.randint(0, 8), 255 - random.randint(0, 8))
    img = Image.new("RGB", (w, h), bg_color)
    draw = ImageDraw.Draw(img)
    
    # Use green color scheme for faculty
    colors = {
        "primary": (34, random.randint(100, 139), 34),
        "secondary": (51, random.randint(150, 180), 68),
        "accent": (255, 255, 255),
        "text": (51, 51, 51)
    }
    
    font_title = get_font(random.randint(20, 24))
    font_text = get_font(random.randint(14, 17))
    font_small = get_font(random.randint(11, 13))
    
    # Header
    header_h = random.randint(45, 55)
    draw.rectangle([(0, 0), (w, header_h)], fill=colors["primary"])
    
    title = random.choice(["STAFF IDENTIFICATION", "FACULTY ID CARD", "EMPLOYEE BADGE"])
    draw.text((w // 2, header_h // 2), title, fill=colors["accent"], font=font_title, anchor="mm")
    
    # School name
    school_y = header_h + random.randint(20, 30)
    draw.text((w // 2, school_y), school[:45], fill=colors["primary"], font=font_text, anchor="mm")
    
    # Photo placeholder
    photo_x = random.randint(20, 30)
    photo_y = random.randint(95, 105)
    photo_w = random.randint(95, 105)
    photo_h = random.randint(115, 125)
    draw.rectangle([(photo_x, photo_y), (photo_x + photo_w, photo_y + photo_h)], 
                   outline=(200, 200, 200), width=2)
    draw.text((photo_x + photo_w // 2, photo_y + photo_h // 2), 
              "PHOTO", fill=(200, 200, 200), font=font_text, anchor="mm")
    
    # Teacher info
    teacher_id = f"T{random.randint(10000, 99999)}"
    current_year = int(time.strftime('%Y'))
    
    info_x = photo_x + photo_w + random.randint(15, 25)
    info_y = photo_y
    
    departments = ["Education", "Mathematics", "Science", "English", "History", "Computer Science"]
    
    info_lines = [
        f"Name: {first} {last}",
        f"ID: {teacher_id}",
        f"Position: {random.choice(['Teacher', 'Instructor', 'Faculty Member'])}",
        f"Department: {random.choice(departments)}",
        f"Status: Active"
    ]
    
    for line in info_lines:
        draw.text(randomize_position(info_x, info_y, 1), line, fill=colors["text"], font=font_text)
        info_y += random.randint(20, 25)
    
    # Valid date
    draw.text((info_x, info_y + 10), f"Valid: {current_year}-{current_year + 1} School Year", 
              fill=(100, 100, 100), font=font_small)
    
    # Footer
    footer_y = h - random.randint(32, 40)
    draw.rectangle([(0, footer_y), (w, h)], fill=colors["primary"])
    draw.text((w // 2, (footer_y + h) // 2), "Property of School District", 
              fill=colors["accent"], font=font_small, anchor="mm")
    
    # Add noise
    if add_noise:
        img = add_simple_noise(img, intensity=random.randint(2, 4))
    
    buf = BytesIO()
    img.save(buf, format="PNG", optimize=True)
    return buf.getvalue()


# ============ UTILITY FUNCTIONS ============

def get_document_type_weights() -> dict:
    """
    Get recommended document type weights based on success rates
    Transcripts generally have higher success rates than IDs
    """
    return {
        "transcript": 70,
        "student_id": 20,
        "enrollment_letter": 10
    }


def select_document_type() -> str:
    """Select document type based on weights"""
    weights = get_document_type_weights()
    total = sum(weights.values())
    r = random.uniform(0, total)
    
    cumulative = 0
    for doc_type, weight in weights.items():
        cumulative += weight
        if r <= cumulative:
            return doc_type
    return "transcript"


if __name__ == "__main__":
    print("Document Generator Test")
    print("-" * 50)
    
    # Test student ID
    print("\n1. Generating Student ID...")
    student_id = generate_student_id("John", "Doe", "Massachusetts Institute of Technology")
    print(f"   Size: {len(student_id) / 1024:.1f} KB")
    
    # Test transcript
    print("\n2. Generating Transcript...")
    transcript = generate_transcript("Jane", "Smith", "2003-05-15", "Stanford University")
    print(f"   Size: {len(transcript) / 1024:.1f} KB")
    
    # Test teacher badge
    print("\n3. Generating Teacher Badge...")
    badge = generate_teacher_badge("Robert", "Johnson", "Stuyvesant High School")
    print(f"   Size: {len(badge) / 1024:.1f} KB")
    
    print("\n" + "-" * 50)
    print("All documents generated successfully!")
    print("\nDocument Type Weights:")
    for doc_type, weight in get_document_type_weights().items():
        print(f"  {doc_type}: {weight}%")
