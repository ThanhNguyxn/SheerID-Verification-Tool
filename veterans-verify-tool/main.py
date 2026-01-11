"""
Veterans Verification Tool
ChatGPT Plus Veterans/Military Verification

Written from scratch - based on SheerID API flow understanding
Author: ThanhNguyxn

Features:
- Proxy support
- Deduplication tracking
- Anti-detection with random User-Agents
"""

import json
import hashlib
import time
import re
import os
import sys
import argparse
import uuid
import base64
import imaplib
import email
from email.header import decode_header
from pathlib import Path
from typing import Optional, List

try:
    import requests
except ImportError:
    print("Error: requests library required. Install with: pip install requests")
    exit(1)

# Try cloudscraper for Cloudflare bypass (optional but recommended)
try:
    import cloudscraper
    HAS_CLOUDSCRAPER = True
except ImportError:
    HAS_CLOUDSCRAPER = False
    print("[WARN] cloudscraper not installed. Install for better Cloudflare bypass:")
    print("       pip install cloudscraper")

# Import anti-detection module
try:
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from anti_detect import get_headers, get_fingerprint, get_random_user_agent, random_delay, create_session
    HAS_ANTI_DETECT = True
    print("[INFO] Anti-detection module loaded")
except ImportError:
    HAS_ANTI_DETECT = False
    print("[WARN] anti_detect.py not found, using basic headers")



# Constants
SHEERID_API = "https://services.sheerid.com/rest/v2"
CHATGPT_API = "https://chatgpt.com/backend-api"
DEFAULT_PROGRAM_ID = "690415d58971e73ca187d8c9"

# File paths
PROXY_FILE = "proxy.txt"
USED_FILE = "used.txt"

# Military Branch Organization IDs
BRANCH_ORG_MAP = {
    "Army": {"id": 4070, "name": "Army"},
    "Air Force": {"id": 4073, "name": "Air Force"},
    "Navy": {"id": 4072, "name": "Navy"},
    "Marine Corps": {"id": 4071, "name": "Marine Corps"},
    "Coast Guard": {"id": 4074, "name": "Coast Guard"},
    "Space Force": {"id": 4544268, "name": "Space Force"},
    "Army National Guard": {"id": 4075, "name": "Army National Guard"},
    "Army Reserve": {"id": 4076, "name": "Army Reserve"},
    "Air National Guard": {"id": 4079, "name": "Air National Guard"},
    "Air Force Reserve": {"id": 4080, "name": "Air Force Reserve"},
    "Navy Reserve": {"id": 4078, "name": "Navy Reserve"},
    "Marine Corps Reserve": {"id": 4077, "name": "Marine Corps Forces Reserve"},
    "Coast Guard Reserve": {"id": 4081, "name": "Coast Guard Reserve"},
}

# Fallback User-Agent if anti_detect not available
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/131.0.0.0 Safari/537.36"


# ============ PROXY & DEDUPLICATION ============
def load_proxies(file_path: str = None) -> List[str]:
    """Load proxy list from file"""
    path = Path(file_path or PROXY_FILE)
    if not path.exists():
        return []
    
    proxies = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            # Handle format: host:port or host:port:user:pass
            if "://" not in line:
                parts = line.split(":")
                if len(parts) >= 2:
                    if len(parts) == 2:
                        line = f"http://{parts[0]}:{parts[1]}"
                    elif len(parts) == 4:
                        line = f"http://{parts[2]}:{parts[3]}@{parts[0]}:{parts[1]}"
            proxies.append(line)
    return proxies


def get_used_data() -> set:
    """Load used data records"""
    path = Path(__file__).parent / USED_FILE
    if not path.exists():
        return set()
    return set(line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip())


def is_data_used(first_name: str, last_name: str, dob: str) -> bool:
    """Check if data was already used"""
    key = f"{first_name.upper()}|{last_name.upper()}|{dob}"
    return key in get_used_data()


def mark_data_used(first_name: str, last_name: str, dob: str):
    """Mark data as used"""
    path = Path(__file__).parent / USED_FILE
    key = f"{first_name.upper()}|{last_name.upper()}|{dob}"
    with open(path, "a", encoding="utf-8") as f:
        f.write(key + "\n")


def generate_fingerprint():
    """Generate device fingerprint"""
    screens = ["1920x1080", "2560x1440", "1366x768"]
    screen = screens[hash(str(time.time())) % len(screens)]
    raw = f"{screen}|{time.time()}|{uuid.uuid4()}"
    return hashlib.md5(raw.encode()).hexdigest()


def generate_newrelic_headers():
    """Generate NewRelic tracking headers"""
    trace_id = uuid.uuid4().hex + uuid.uuid4().hex[:8]
    trace_id = trace_id[:32]
    span_id = uuid.uuid4().hex[:16]
    timestamp = int(time.time() * 1000)
    
    payload = {
        "v": [0, 1],
        "d": {
            "ty": "Browser",
            "ac": "364029",
            "ap": "134291347",
            "id": span_id,
            "tr": trace_id,
            "ti": timestamp
        }
    }
    
    return {
        "newrelic": base64.b64encode(json.dumps(payload).encode()).decode(),
        "traceparent": f"00-{trace_id}-{span_id}-01",
        "tracestate": f"364029@nr=0-1-364029-134291347-{span_id}----{timestamp}"
    }


def match_branch(input_str):
    """Map input string to branch name"""
    normalized = input_str.upper().replace("US ", "").strip()
    
    for branch in BRANCH_ORG_MAP:
        if branch.upper() == normalized:
            return branch
    
    # Fuzzy matching
    if "MARINE" in normalized and "RESERVE" not in normalized:
        return "Marine Corps"
    if "ARMY" in normalized and "NATIONAL" in normalized:
        return "Army National Guard"
    if "ARMY" in normalized and "RESERVE" in normalized:
        return "Army Reserve"
    if "ARMY" in normalized:
        return "Army"
    if "NAVY" in normalized and "RESERVE" in normalized:
        return "Navy Reserve"
    if "NAVY" in normalized:
        return "Navy"
    if "AIR" in normalized and "NATIONAL" in normalized:
        return "Air National Guard"
    if "AIR" in normalized and "RESERVE" in normalized:
        return "Air Force Reserve"
    if "AIR" in normalized:
        return "Air Force"
    if "COAST" in normalized and "RESERVE" in normalized:
        return "Coast Guard Reserve"
    if "COAST" in normalized:
        return "Coast Guard"
    if "SPACE" in normalized:
        return "Space Force"
    
    return "Army"


def parse_data_line(line):
    """Parse data line: firstName|lastName|branch|birthDate|dischargeDate"""
    parts = [p.strip() for p in line.split("|")]
    if len(parts) < 4:
        return None
    
    branch_name = match_branch(parts[2])
    org = BRANCH_ORG_MAP.get(branch_name, BRANCH_ORG_MAP["Army"])
    
    return {
        "firstName": parts[0],
        "lastName": parts[1],
        "branch": branch_name,
        "birthDate": parts[3],
        "dischargeDate": parts[4] if len(parts) > 4 else "2025-01-02",
        "organization": org
    }


class EmailClient:
    """Simple IMAP email client"""
    
    def __init__(self, config):
        self.server = config.get("imap_server", "imap.gmail.com")
        self.port = config.get("imap_port", 993)
        self.email = config.get("email_address", "")
        self.password = config.get("email_password", "")
        self.use_ssl = config.get("use_ssl", True)
        self.conn = None
    
    def connect(self):
        try:
            if self.use_ssl:
                self.conn = imaplib.IMAP4_SSL(self.server, self.port)
            else:
                self.conn = imaplib.IMAP4(self.server, self.port)
            self.conn.login(self.email, self.password)
            return True
        except Exception as e:
            print(f"   [ERROR] Email connection failed: {e}")
            self.conn = None  # Reset connection on failure
            if "LOGIN failed" in str(e):
                print("   [TIP] Check your email/password.")
                print("         - If using Gmail/Outlook/Yahoo with 2FA, use an App Password.")
                print("         - Check if IMAP is enabled in your email settings.")
            return False
    
    def get_latest_emails(self, count=5):
        if not self.conn:
            if not self.connect():
                return []
        
        try:
            self.conn.select("INBOX")
            _, messages = self.conn.search(None, "ALL")
            email_ids = messages[0].split()
            
            if not email_ids:
                return []
            
            latest_ids = email_ids[-count:] if len(email_ids) >= count else email_ids
            latest_ids = latest_ids[::-1]
            
            emails = []
            for eid in latest_ids:
                _, msg_data = self.conn.fetch(eid, "(RFC822)")
                for part in msg_data:
                    if isinstance(part, tuple):
                        msg = email.message_from_bytes(part[1])
                        content = self._get_content(msg)
                        emails.append({"content": content})
            return emails
        except Exception as e:
            print(f"   [WARN] Email fetch error: {e}")
            self.conn = None
            return []
    
    def _get_content(self, msg):
        content = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/html":
                    payload = part.get_payload(decode=True)
                    if payload:
                        charset = part.get_content_charset() or "utf-8"
                        content = payload.decode(charset, errors="ignore")
                        break
        else:
            payload = msg.get_payload(decode=True)
            if payload:
                charset = msg.get_content_charset() or "utf-8"
                content = payload.decode(charset, errors="ignore")
        return content
    
    def close(self):
        if self.conn:
            try:
                self.conn.logout()
            except:
                pass


class VeteransVerifier:
    """Veterans verification handler"""
    
    def __init__(self, config, proxy: str = None):
        self.access_token = config.get("accessToken", "")
        self.program_id = config.get("programId", DEFAULT_PROGRAM_ID)
        self.email_client = EmailClient(config.get("email", {}))
        self.email_address = config.get("email", {}).get("email_address", "")
        # Setup proxy
        if proxy:
            if "://" not in proxy:
                parts = proxy.split(":")
                if len(parts) == 2:
                    proxy = f"http://{parts[0]}:{parts[1]}"
                elif len(parts) == 4:
                    proxy = f"http://{parts[2]}:{parts[3]}@{parts[0]}:{parts[1]}"
            self.proxies = {"http": proxy, "https": proxy}
        else:
            self.proxies = None
        
        # Create session for ChatGPT API (use cloudscraper if available for Cloudflare bypass)
        if HAS_CLOUDSCRAPER:
            self.session = cloudscraper.create_scraper(
                browser={'browser': 'chrome', 'platform': 'windows', 'mobile': False}
            )
            print("[INFO] Using cloudscraper for Cloudflare bypass")
        else:
            self.session = requests.Session()
            print("[INFO] Using requests (no Cloudflare bypass)")
    
    def _get_headers(self, sheerid=False):
        base = {
            "sec-ch-ua": '"Chromium";v="131", "Google Chrome";v="131"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "user-agent": USER_AGENT,
            "accept": "application/json",
            "content-type": "application/json",
            "accept-language": "en-US,en;q=0.9"
        }
        
        if sheerid:
            nr = generate_newrelic_headers()
            return {
                **base,
                "clientversion": "2.157.0",
                "clientname": "jslib",
                "newrelic": nr["newrelic"],
                "traceparent": nr["traceparent"],
                "tracestate": nr["tracestate"],
                "origin": "https://services.sheerid.com"
            }
        
        # Enhanced headers for ChatGPT API to bypass Cloudflare
        return {
            **base,
            "authorization": f"Bearer {self.access_token}",
            "origin": "https://chatgpt.com",
            "referer": "https://chatgpt.com/veterans-claim",
            # Critical headers for Cloudflare bypass
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            # OpenAI specific headers
            "oai-device-id": str(uuid.uuid4()),
            "oai-language": "en-US",
        }
    
    def create_verification(self):
        """Step 1: Create verification ID from ChatGPT"""
        print("   -> Creating verification request...")
        
        try:
            # Use self.session (cloudscraper if available)
            resp = self.session.post(
                f"{CHATGPT_API}/veterans/create_verification",
                headers=self._get_headers(),
                json={"program_id": self.program_id},
                timeout=30,
                proxies=self.proxies
            )
            resp.raise_for_status()
            return resp.json().get("verification_id")
        except requests.exceptions.HTTPError as e:
            if resp.status_code == 403:
                print("   [ERROR] 403 Forbidden - AccessToken expired or invalid!")
                print("")
                print("   ┌─────────────────────────────────────────────────────┐")
                print("   │  HOW TO FIX:                                        │")
                print("   │                                                     │")
                print("   │  1. Open https://chatgpt.com in your browser        │")
                print("   │  2. Make sure you are LOGGED IN                     │")
                print("   │  3. Visit: https://chatgpt.com/api/auth/session     │")
                print("   │  4. Copy the 'accessToken' value (long string)      │")
                print("   │  5. Paste into config.json -> accessToken field     │")
                print("   │  6. Run this tool again                             │")
                print("   └─────────────────────────────────────────────────────┘")
            elif resp.status_code == 401:
                print("   [ERROR] 401 Unauthorized - Invalid accessToken!")
                print("           Please check your accessToken in config.json")
            raise

    
    def submit_military_status(self, verification_id):
        """Step 2: Submit status as VETERAN"""
        print("   -> Submitting military status (VETERAN)...")
        
        resp = self.session.post(
            f"{SHEERID_API}/verification/{verification_id}/step/collectMilitaryStatus",
            headers=self._get_headers(sheerid=True),
            json={"status": "VETERAN"},
            timeout=30,
            proxies=self.proxies
        )
        resp.raise_for_status()
    
    def submit_personal_info(self, verification_id, user_data):
        """Step 3: Submit personal information"""
        print("   -> Submitting personal info...")
        
        fingerprint = generate_fingerprint()
        referer = f"https://services.sheerid.com/verify/{self.program_id}/?verificationId={verification_id}"
        
        payload = {
            "firstName": user_data["firstName"],
            "lastName": user_data["lastName"],
            "birthDate": user_data["birthDate"],
            "email": self.email_address,
            "phoneNumber": "",
            "organization": user_data["organization"],
            "dischargeDate": user_data["dischargeDate"],
            "deviceFingerprintHash": fingerprint,
            "locale": "en-US",
            "country": "US",
            "metadata": {
                "marketConsentValue": False,
                "refererUrl": referer,
                "verificationId": verification_id,
                "submissionOptIn": "By submitting the personal information above, I acknowledge..."
            }
        }
        
        headers = self._get_headers(sheerid=True)
        headers["referer"] = referer
        
        resp = self.session.post(
            f"{SHEERID_API}/verification/{verification_id}/step/collectInactiveMilitaryPersonalInfo",
            headers=headers,
            json=payload,
            timeout=30,
            proxies=self.proxies
        )
        
        data = resp.json()
        
        if resp.status_code == 429 or "verificationLimitExceeded" in str(data.get("errorIds", [])):
            data["_already_verified"] = True
        
        return data
    
    def wait_for_email(self, verification_id, max_attempts=20):
        """Step 4: Wait for verification email"""
        print("   -> Waiting for verification email...")
        
        for i in range(max_attempts):
            time.sleep(3)
            
            emails = self.email_client.get_latest_emails(5)
            for e in emails:
                content = e.get("content", "")
                if "You're almost there" in content or "Finish Verifying" in content:
                    match = re.search(r"https://services\.sheerid\.com/verify/[^\s\"'<>]+emailToken=\d+", content)
                    if match and verification_id in match.group(0):
                        return match.group(0).replace("&amp;", "&")
            
            print(f"      Waiting... ({i+1}/{max_attempts})")
        
        return None
    
    def submit_email_token(self, verification_id, email_token):
        """Step 5: Submit email token"""
        print(f"   -> Submitting email token: {email_token}...")
        
        resp = self.session.post(
            f"{SHEERID_API}/verification/{verification_id}/step/emailLoop",
            headers=self._get_headers(sheerid=True),
            json={
                "emailToken": email_token,
                "deviceFingerprintHash": generate_fingerprint()
            },
            timeout=30,
            proxies=self.proxies
        )
        return resp.json()
    
    def verify(self, user_data):
        """Main verification flow"""
        try:
            # Step 1
            verification_id = self.create_verification()
            print(f"   [OK] Verification ID: {verification_id}")
            
            # Step 2
            self.submit_military_status(verification_id)
            print("   [OK] Status submitted")
            
            # Step 3
            result = self.submit_personal_info(verification_id, user_data)
            step = result.get("currentStep")
            print(f"   [OK] Personal info submitted - Step: {step}")
            
            if result.get("_already_verified"):
                return {"success": False, "message": "Data already verified", "skip": True}
            
            if step == "success":
                return {"success": True, "message": "Verification successful!"}
            
            if step == "docUpload":
                return {"success": False, "message": "Document upload required"}
            
            if step == "error":
                return {"success": False, "message": f"Error: {result.get('errorIds')}"}
            
            # Step 4: Email loop
            if step == "emailLoop":
                link = self.wait_for_email(verification_id)
                if not link:
                    return {"success": False, "message": "Email not received"}
                
                token_match = re.search(r"emailToken=(\d+)", link)
                if not token_match:
                    return {"success": False, "message": "Cannot extract emailToken"}
                
                # Step 5
                email_result = self.submit_email_token(verification_id, token_match.group(1))
                if email_result.get("currentStep") == "success":
                    return {"success": True, "message": "Verification successful!"}
                
                return {"success": False, "message": f"Email verify failed: {email_result.get('errorIds')}"}
            
            if step == "collectInactiveMilitaryPersonalInfo":
                if result.get("errorIds"):
                    return {"success": False, "message": f"Error: {result.get('errorIds')}"}
                return {"success": False, "message": "Stuck on personal info step (check data format/validity)"}
            
            return {"success": False, "message": f"Unknown step: {step}"}
            
        except Exception as e:
            return {"success": False, "error": str(e)}


def main():
    # Parse arguments
    parser = argparse.ArgumentParser(description="Veterans Verification Tool")
    parser.add_argument("--proxy", type=str, help="Use specific proxy (host:port)")
    parser.add_argument("--no-dedup", action="store_true", help="Disable deduplication check")
    args = parser.parse_args()
    
    print()
    print("=" * 55)
    print("  Veterans Verification Tool")
    print("  ChatGPT Plus - US Veterans Verification")
    print("=" * 55)
    print()
    
    # Load config
    config_path = Path(__file__).parent / "config.json"
    if not config_path.exists():
        print("[ERROR] config.json not found!")
        print("        Copy config.example.json to config.json and fill in your details")
        return
    
    config = json.loads(config_path.read_text(encoding="utf-8"))
    
    if not config.get("accessToken"):
        print("[ERROR] accessToken missing in config.json!")
        print("        1. Login to https://chatgpt.com")
        print("        2. Visit https://chatgpt.com/api/auth/session")
        print("        3. Copy the accessToken value")
        return
    
    # Load proxies
    proxies = []
    if args.proxy:
        proxies = [args.proxy]
    else:
        proxies = load_proxies(str(Path(__file__).parent / PROXY_FILE))
    if proxies:
        print(f"[INFO] Loaded {len(proxies)} proxies")
    
    # Load data from data.txt
    data_path = Path(__file__).parent / "data.txt"
    if not data_path.exists():
        print("[ERROR] data.txt not found!")
        print("        Copy data.example.txt to data.txt and add your data")
        return
    
    lines = [l.strip() for l in data_path.read_text(encoding="utf-8").split("\n")
             if l.strip() and not l.startswith("#")]
    
    if not lines:
        print("[ERROR] data.txt is empty!")
        return
    
    print(f"[INFO] Loaded {len(lines)} records")
    print()

    
    verifier = VeteransVerifier(config, proxy=proxies[0] if proxies else None)
    
    success = 0
    fail = 0
    skip = 0
    
    for i, line in enumerate(lines):
        user_data = parse_data_line(line)
        if not user_data:
            print(f"[{i+1}/{len(lines)}] Invalid format, skipping")
            continue
        
        name = f"{user_data['firstName']} {user_data['lastName']}"
        
        # Check deduplication
        if not args.no_dedup and is_data_used(user_data['firstName'], user_data['lastName'], user_data['birthDate']):
            print(f"[{i+1}/{len(lines)}] {name} - Already used, skipping")
            skip += 1
            continue
        
        print(f"[{i+1}/{len(lines)}] {name} ({user_data['branch']})")
        
        result = verifier.verify(user_data)
        
        # Mark as used regardless of result
        if not args.no_dedup:
            mark_data_used(user_data['firstName'], user_data['lastName'], user_data['birthDate'])
        
        if result.get("success"):
            success += 1
            print(f"   [SUCCESS]\n")
            print("-" * 55)
            print("  Verification successful! Stopping...")
            print("-" * 55)
            break
        elif result.get("skip"):
            skip += 1
            print(f"   [SKIP] {result['message']}\n")
        else:
            fail += 1
            print(f"   [FAIL] {result.get('message') or result.get('error')}\n")
        
        if i < len(lines) - 1:
            time.sleep(2)
    
    verifier.email_client.close()
    
    print()
    print("-" * 55)
    print(f"  Done! Success: {success} | Skip: {skip} | Fail: {fail}")
    print("-" * 55)


if __name__ == "__main__":
    main()
