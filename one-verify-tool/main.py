",
    "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill",
    "Flores", "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell",
    "Mitchell", "Carter", "Roberts", "Turner", "Phillips", "Evans", "Parker", "Edwards"
]


def random_delay():
    time.sleep(random.randint(MIN_DELAY, MAX_DELAY) / 1000)


def generate_fingerprint() -> str:
    """Generate realistic browser fingerprint to avoid fraud detection"""
    # Realistic screen resolutions
    resolutions = ["1920x1080", "1366x768", "1536x864", "1440x900", "1280x720", "2560x1440"]
    # Common timezones
    timezones = [-8, -7, -6, -5, -4, 0, 1, 2, 3, 5.5, 8, 9, 10]
    # Common languages
    languages = ["en-US", "en-GB", "en-CA", "en-AU", "es-ES", "fr-FR", "de-DE", "pt-BR"]
    # Common platforms
    platforms = ["Win32", "MacIntel", "Linux x86_64"]
    # Browser vendors
    vendors = ["Google Inc.", "Apple Computer, Inc.", ""]
    
    components = [
        str(int(time.time() * 1000)),
        str(random.random()),
        random.choice(resolutions),
        str(random.choice(timezones)),
        random.choice(languages),
        random.choice(platforms),
        random.choice(vendors),
        str(random.randint(1, 16)),  # hardware concurrency (CPU cores)
        str(random.randint(2, 32)),  # device memory GB
        str(random.randint(0, 1)),   # touch support
    ]
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
# ============ DOCUMENT GENERATOR ============
def generate_transcript(first: str, last: str, school: str, dob: str) -> bytes:
    """Generate fake academic transcript (higher success rate)"""
    w, h = 850, 1100
    img = Image.new("RGB", (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    try:
        font_header = ImageFont.truetype("arial.ttf", 32)
        font_title = ImageFont.truetype("arial.ttf", 24)
        font_text = ImageFont.truetype("arial.ttf", 16)
        font_bold = ImageFont.truetype("arialbd.ttf", 16)
    except:
        font_header = font_title = font_text = font_bold = ImageFont.load_default()
    
    # 1. Header
    draw.text((w//2, 50), school.upper(), fill=(0, 0, 0), font=font_header, anchor="mm")
    draw.text((w//2, 90), "OFFICIAL ACADEMIC TRANSCRIPT", fill=(50, 50, 50), font=font_title, anchor="mm")
    draw.line([(50, 110), (w-50, 110)], fill=(0, 0, 0), width=2)
    
    # 2. Student Info
    y = 150
    draw.text((50, y), f"Student Name: {first} {last}", fill=(0, 0, 0), font=font_bold)
    draw.text((w-300, y), f"Student ID: {random.randint(10000000, 99999999)}", fill=(0, 0, 0), font=font_text)
    y += 30
    draw.text((50, y), f"Date of Birth: {dob}", fill=(0, 0, 0), font=font_text)
    draw.text((w-300, y), f"Date Issued: {time.strftime('%Y-%m-%d')}", fill=(0, 0, 0), font=font_text)
    y += 40
    
    # 3. Current Enrollment Status
    draw.rectangle([(50, y), (w-50, y+40)], fill=(240, 240, 240))
    draw.text((w//2, y+20), "CURRENT STATUS: ENROLLED (SPRING 2025)", fill=(0, 100, 0), font=font_bold, anchor="mm")
    y += 70
    
    # 4. Courses
    courses = [
        ("CS 101", "Intro to Computer Science", "4.0", "A"),
        ("MATH 201", "Calculus I", "3.0", "A-"),
        ("ENG 102", "Academic Writing", "3.0", "B+"),
        ("PHYS 150", "Physics for Engineers", "4.0", "A"),
        ("HIST 110", "World History", "3.0", "A")
    ]
    
    # Table Header
    draw.text((50, y), "Course Code", font=font_bold, fill=(0,0,0))
    draw.text((200, y), "Course Title", font=font_bold, fill=(0,0,0))
    draw.text((600, y), "Credits", font=font_bold, fill=(0,0,0))
    draw.text((700, y), "Grade", font=font_bold, fill=(0,0,0))
    y += 20
    draw.line([(50, y), (w-50, y)], fill=(0, 0, 0), width=1)
    y += 20
    
    for code, title, cred, grade in courses:
        draw.text((50, y), code, font=font_text, fill=(0,0,0))
        draw.text((200, y), title, font=font_text, fill=(0,0,0))
        draw.text((600, y), cred, font=font_text, fill=(0,0,0))
        draw.text((700, y), grade, font=font_text, fill=(0,0,0))
        y += 30
    
    y += 20
    draw.line([(50, y), (w-50, y)], fill=(0, 0, 0), width=1)
    y += 30
    
    # 5. Summary
    draw.text((50, y), "Cumulative GPA: 3.85", font=font_bold, fill=(0,0,0))
    draw.text((w-300, y), "Academic Standing: Good", font=font_bold, fill=(0,0,0))
    
    # 6. Watermark / Footer
    draw.text((w//2, h-50), "This document is electronically generated and valid without signature.", fill=(100, 100, 100), font=font_text, anchor="mm")
    
    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

def generate_student_id(first: str, last: str, school: str) -> bytes:
    """Generate fake student ID card (Improved)"""
    w, h = 650, 400
    # Randomize background color slightly
    bg_color = (random.randint(240, 255), random.randint(240, 255), random.randint(240, 255))
    img = Image.new("RGB", (w, h), bg_color)
    draw = ImageDraw.Draw(img)
    
    try:
        font_lg = ImageFont.truetype("arial.ttf", 26)
        font_md = ImageFont.truetype("arial.ttf", 18)
        font_sm = ImageFont.truetype("arial.ttf", 14)
        font_bold = ImageFont.truetype("arialbd.ttf", 20)
    except:
        font_lg = font_md = font_sm = font_bold = ImageFont.load_default()
    
    # Header color based on school name hash to be consistent but varied
    header_color = (random.randint(0, 50), random.randint(0, 50), random.randint(50, 150))
    
    draw.rectangle([(0, 0), (w, 80)], fill=header_color)
    draw.text((w//2, 40), school.upper(), fill=(255, 255, 255), font=font_lg, anchor="mm")
    
    # Photo placeholder
    draw.rectangle([(30, 100), (160, 280)], outline=(100, 100, 100), width=2, fill=(220, 220, 220))
    draw.text((95, 190), "PHOTO", fill=(150, 150, 150), font=font_md, anchor="mm")
    
    # Info
    x_info = 190
    y = 110
    draw.text((x_info, y), f"{first} {last}", fill=(0, 0, 0), font=font_bold)
    y += 40
    draw.text((x_info, y), "Student ID:", fill=(100, 100, 100), font=font_sm)
    draw.text((x_info + 80, y), str(random.randint(10000000, 99999999)), fill=(0, 0, 0), font=font_md)
    y += 30
    draw.text((x_info, y), "Role:", fill=(100, 100, 100), font=font_sm)
    draw.text((x_info + 80, y), "Student", fill=(0, 0, 0), font=font_md)
    y += 30
    draw.text((x_info, y), "Valid Thru:", fill=(100, 100, 100), font=font_sm)
    draw.text((x_info + 80, y), f"05/{int(time.strftime('%Y'))+1}", fill=(0, 0, 0), font=font_md)
    
    # Barcode strip
    draw.rectangle([(0, 320), (w, 380)], fill=(255, 255, 255))
    for i in range(40):
        x = 50 + i * 14
        if random.random() > 0.3:
            draw.rectangle([(x, 330), (x+8, 370)], fill=(0, 0, 0))
            
    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


# ============ VERIFIER ============
class GeminiVerifier:
    """Gemini Student Verification with enhanced features"""
    
    def __init__(self, url: str, proxy: str = None):
        self.url = url
        self.vid = self._parse_id(url)
        self.fingerprint = generate_fingerprint()
        
        # Configure proxy if provided
        proxies = None
        if proxy:
            if not proxy.startswith("http"):
                proxy = f"http://{proxy}"
            proxies = {"all://": proxy}
        
        self.client = httpx.Client(timeout=30, proxies=proxies)
        self.org = None
    
    def __del__(self):
        if hasattr(self, "client"):
            self.client.close()
    
    @staticmethod
    def _parse_id(url: str) -> Optional[str]:
        match = re.search(r"verificationId=([a-f0-9]+)", url, re.IGNORECASE)
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
            self.org = select_university()
            email = generate_email(first, last, self.org["domain"])
            dob = generate_birth_date()
            
            print(f"\n   🎓 Student: {first} {last}")
            print(f"   📧 Email: {email}")
            print(f"   🏫 School: {self.org['name']}")
            print(f"   🎂 DOB: {dob}")
            print(f"   🔑 ID: {self.vid[:20]}...")
            print(f"   📍 Starting step: {current_step}")
            
            # Step 1: Generate document
            doc_type = "transcript" if random.random() < 0.7 else "id_card"
            if doc_type == "transcript":
                print("\n   ▶ Step 1/3: Generating academic transcript...")
                doc = generate_transcript(first, last, self.org["name"], dob)
                filename = "transcript.png"
            else:
                print("\n   ▶ Step 1/3: Generating student ID...")
                doc = generate_student_id(first, last, self.org["name"])
                filename = "student_card.png"
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
                        "refererUrl": f"https://services.sheerid.com/verify/{PROGRAM_ID}/?verificationId={self.vid}",
                        "flags": '{"collect-info-step-email-first":"default","doc-upload-considerations":"default","doc-upload-may24":"default","doc-upload-redesign-use-legacy-message-keys":false,"docUpload-assertion-checklist":"default","font-size":"default","include-cvec-field-france-student":"not-labeled-optional"}',
                        "submissionOptIn": "By submitting the personal information above, I acknowledge that my personal information is being collected under the privacy policy of the business from which I am seeking a discount"
                    }
                }
                
                data, status = self._request("POST", f"/verification/{self.vid}/step/collectStudentPersonalInfo", body)
                
                if status != 200:
                    stats.record(self.org["name"], False)
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
            upload_body = {"files": [{"fileName": filename, "mimeType": "image/png", "fileSize": len(doc)}]}
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
    parser = argparse.ArgumentParser(description="Google One (Gemini) Student Verification Tool")
    parser.add_argument("url", nargs="?", help="Verification URL")
    parser.add_argument("--proxy", help="Proxy server (host:port or http://user:pass@host:port)")
    args = parser.parse_args()
    
    print()
    print("╔" + "═" * 56 + "╗")
    print("║" + " 🤖 Google One (Gemini) Verification Tool".center(56) + "║")
    print("║" + " SheerID Student Discount".center(56) + "║")
    print("╚" + "═" * 56 + "╝")
    print()
    
    # Get URL
    if args.url:
        url = args.url
    else:
        url = input("   Enter verification URL: ").strip()
    
    if not url or "sheerid.com" not in url:
        print("\n   ❌ Invalid URL. Must contain sheerid.com")
        return
    
    # Show proxy info
    if args.proxy:
        print(f"   🔒 Using proxy: {args.proxy}")
    
    print("\n   ⏳ Processing...")
    
    verifier = GeminiVerifier(url, proxy=args.proxy)
    
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
