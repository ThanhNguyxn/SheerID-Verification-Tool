"""
SheerID Verification Tool - Document Generators
Generate fake documents (student ID, teacher badge, etc.)
"""

import time
import random
from io import BytesIO

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("Error: Pillow required. Install: pip install Pillow")
    exit(1)


def _get_fonts():
    """Get fonts, fallback to default if not available"""
    try:
        title = ImageFont.truetype("arial.ttf", 28)
        text = ImageFont.truetype("arial.ttf", 20)
        small = ImageFont.truetype("arial.ttf", 14)
    except:
        title = ImageFont.load_default()
        text = ImageFont.load_default()
        small = ImageFont.load_default()
    return title, text, small


def generate_student_id(first_name: str, last_name: str, school_name: str, student_id: str = None) -> bytes:
    """Generate fake student ID card PNG"""
    width, height = 650, 400
    img = Image.new("RGB", (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    title_font, text_font, small_font = _get_fonts()
    
    # Header
    draw.rectangle([(0, 0), (width, 65)], fill=(0, 51, 102))
    draw.text((width//2, 32), "STUDENT IDENTIFICATION CARD", fill=(255, 255, 255), 
              font=title_font, anchor="mm")
    
    # School name
    draw.text((width//2, 95), school_name[:50], fill=(0, 51, 102), font=text_font, anchor="mm")
    
    # Photo placeholder
    draw.rectangle([(30, 130), (160, 290)], outline=(180, 180, 180), width=2)
    draw.text((95, 210), "PHOTO", fill=(180, 180, 180), font=text_font, anchor="mm")
    
    # Student info
    if not student_id:
        student_id = f"STU{random.randint(100000, 999999)}"
    
    info_y = 140
    lines = [
        f"Name: {first_name} {last_name}",
        f"Student ID: {student_id}",
        f"Program: Undergraduate",
        f"Major: Computer Science",
        f"Status: Full-time Student",
        f"Valid: {time.strftime('%Y')} - {int(time.strftime('%Y'))+1}"
    ]
    
    for line in lines:
        draw.text((185, info_y), line, fill=(51, 51, 51), font=text_font)
        info_y += 28
    
    # Footer
    draw.rectangle([(0, height-45), (width, height)], fill=(0, 51, 102))
    draw.text((width//2, height-23), "This card remains property of the university", 
              fill=(255, 255, 255), font=small_font, anchor="mm")
    
    # Barcode placeholder
    for i in range(20):
        x = 450 + i * 8
        h = random.randint(30, 60)
        draw.rectangle([(x, 290), (x+4, 290+h)], fill=(0, 0, 0))
    
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return buffer.getvalue()


def generate_teacher_certificate(first_name: str, last_name: str, school_name: str) -> bytes:
    """Generate fake teacher employment certificate PNG"""
    width, height = 800, 550
    img = Image.new("RGB", (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    title_font, text_font, small_font = _get_fonts()
    
    # Border
    draw.rectangle([(15, 15), (width-15, height-15)], outline=(0, 51, 102), width=3)
    draw.rectangle([(25, 25), (width-25, height-25)], outline=(0, 51, 102), width=1)
    
    # Header
    draw.text((width//2, 60), "CERTIFICATE OF EMPLOYMENT", fill=(0, 51, 102), 
              font=title_font, anchor="mm")
    draw.line([(100, 90), (width-100, 90)], fill=(0, 51, 102), width=2)
    
    # School name
    draw.text((width//2, 130), school_name, fill=(51, 51, 51), font=text_font, anchor="mm")
    
    # Content
    content_y = 180
    lines = [
        "This is to certify that",
        "",
        f"{first_name} {last_name}",
        "",
        "is currently employed as a Faculty Member",
        f"in the Department of Education",
        "",
        f"Employment Status: Active",
        f"Position: Full-time Teacher",
        f"Issue Date: {time.strftime('%B %d, %Y')}"
    ]
    
    for line in lines:
        if line == f"{first_name} {last_name}":
            draw.text((width//2, content_y), line, fill=(0, 51, 102), font=title_font, anchor="mm")
        else:
            draw.text((width//2, content_y), line, fill=(51, 51, 51), font=text_font, anchor="mm")
        content_y += 30
    
    # Signature line
    draw.line([(150, height-100), (350, height-100)], fill=(0, 0, 0), width=1)
    draw.text((250, height-80), "Authorized Signature", fill=(100, 100, 100), font=small_font, anchor="mm")
    
    # Seal placeholder
    draw.ellipse([(width-200, height-150), (width-100, height-50)], outline=(0, 51, 102), width=2)
    draw.text((width-150, height-100), "SEAL", fill=(0, 51, 102), font=text_font, anchor="mm")
    
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return buffer.getvalue()


def generate_teacher_badge(first_name: str, last_name: str, school_name: str) -> bytes:
    """Generate fake K12 teacher badge PNG"""
    width, height = 500, 350
    img = Image.new("RGB", (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    title_font, text_font, small_font = _get_fonts()
    
    # Header (green for K12)
    draw.rectangle([(0, 0), (width, 55)], fill=(34, 139, 34))
    draw.text((width//2, 28), "STAFF IDENTIFICATION", fill=(255, 255, 255), 
              font=title_font, anchor="mm")
    
    # School name
    draw.text((width//2, 80), school_name[:45], fill=(34, 139, 34), font=text_font, anchor="mm")
    
    # Photo placeholder
    draw.rectangle([(25, 110), (130, 240)], outline=(180, 180, 180), width=2)
    draw.text((77, 175), "PHOTO", fill=(180, 180, 180), font=text_font, anchor="mm")
    
    # Teacher info
    teacher_id = f"T{random.randint(10000, 99999)}"
    info_y = 115
    lines = [
        f"Name: {first_name} {last_name}",
        f"ID: {teacher_id}",
        f"Position: Teacher",
        f"Department: Education",
        f"Status: Active"
    ]
    
    for line in lines:
        draw.text((150, info_y), line, fill=(51, 51, 51), font=text_font)
        info_y += 25
    
    # Valid year
    year = int(time.strftime("%Y"))
    draw.text((150, info_y + 10), f"Valid: {year}-{year+1} School Year", 
              fill=(100, 100, 100), font=small_font)
    
    # Footer
    draw.rectangle([(0, height-40), (width, height)], fill=(34, 139, 34))
    draw.text((width//2, height-20), "Property of School District", 
              fill=(255, 255, 255), font=small_font, anchor="mm")
    
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return buffer.getvalue()


def generate_enrollment_letter(first_name: str, last_name: str, school_name: str) -> bytes:
    """Generate fake enrollment verification letter PNG"""
    width, height = 700, 900
    img = Image.new("RGB", (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    title_font, text_font, small_font = _get_fonts()
    
    # Letterhead
    draw.text((width//2, 50), school_name, fill=(0, 51, 102), font=title_font, anchor="mm")
    draw.text((width//2, 80), "Office of the Registrar", fill=(100, 100, 100), font=text_font, anchor="mm")
    draw.line([(50, 110), (width-50, 110)], fill=(0, 51, 102), width=2)
    
    # Date
    draw.text((width-100, 150), time.strftime("%B %d, %Y"), fill=(51, 51, 51), font=text_font, anchor="rm")
    
    # Body
    body_y = 200
    paragraphs = [
        "ENROLLMENT VERIFICATION",
        "",
        "To Whom It May Concern:",
        "",
        f"This letter is to verify that {first_name} {last_name} is currently",
        f"enrolled as a full-time student at {school_name[:40]}.",
        "",
        "Student Information:",
        f"   Name: {first_name} {last_name}",
        f"   Status: Full-time Student",
        f"   Program: Undergraduate",
        f"   Expected Graduation: {int(time.strftime('%Y'))+2}",
        "",
        "This verification is valid for the current academic year.",
        "",
        "If you have any questions, please contact our office.",
        "",
        "Sincerely,",
        "",
        "",
        "________________________",
        "Registrar's Office"
    ]
    
    for line in paragraphs:
        if line == "ENROLLMENT VERIFICATION":
            draw.text((width//2, body_y), line, fill=(0, 51, 102), font=title_font, anchor="mm")
        else:
            draw.text((60, body_y), line, fill=(51, 51, 51), font=text_font)
        body_y += 28
    
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return buffer.getvalue()
