"""
Microsoft 365 Education Student Verification Tool
Automates the MS365 student verification process using Playwright

Features:
- Automated browser session with token capture
- Direct MS API calls for student verification
- SheerID document upload fallback
- Anti-detection with realistic browser fingerprint

Requirements:
- playwright: pip install playwright && playwright install chromium
- httpx: pip install httpx
- Pillow: pip install Pillow (for document generation)

Usage:
    python main.py                    # Interactive mode
    python main.py --email user@edu   # Direct mode with email
    python main.py --headless         # Headless browser mode

Author: ThanhNguyxn
"""

import os
import sys
import json
import time
import random
import asyncio
import argparse
from pathlib import Path
from typing import Dict, Optional, Tuple
from dataclasses import dataclass

try:
    import httpx
except ImportError:
    print("Error: httpx required. Install: pip install httpx")
    sys.exit(1)

# Import document generator if available
try:
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from doc_generator import generate_student_id, generate_transcript

    HAS_DOC_GEN = True
except ImportError:
    HAS_DOC_GEN = False
    print("[WARN] doc_generator not found, document upload will use placeholder")


# ============ CONFIG ============
MS365_CHECKOUT_URL = "https://checkout.microsoft365.com/acquire/purchase"
MS365_API_BASE = "https://checkout.microsoft365.com/api"
SHEERID_API_BASE = "https://services.sheerid.com/rest/v2"

# Query params for student checkout
CHECKOUT_PARAMS = {
    "language": "en-US",
    "market": "US",
    "requestedDuration": "Month",
    "scenario": "microsoft-365-student",
    "client": "poc",
    "campaign": "StudentFree12M",
}


@dataclass
class CapturedTokens:
    """Captured authentication tokens from MS365"""

    bearer: str
    x_auth: str
    cookies: str
    timestamp: float

    @property
    def is_valid(self) -> bool:
        """Check if tokens are still valid (1 hour expiry assumed)"""
        return time.time() - self.timestamp < 3600

    def to_headers(self) -> Dict[str, str]:
        """Convert to request headers"""
        return {
            "Authorization": self.bearer,
            "X-Auth": self.x_auth,
            "Cookie": self.cookies,
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        }


class MS365Verifier:
    """Microsoft 365 Education Student Verifier"""

    def __init__(self, headless: bool = False):
        self.headless = headless
        self.tokens: Optional[CapturedTokens] = None
        self.browser = None
        self.page = None

    async def launch_browser(self):
        """Launch Playwright browser with anti-detection"""
        try:
            from playwright.async_api import async_playwright
        except ImportError:
            print("Error: Playwright required. Install:")
            print("  pip install playwright")
            print("  playwright install chromium")
            sys.exit(1)

        # Try to import stealth plugin for better anti-detection
        try:
            from playwright_stealth import stealth_async

            HAS_STEALTH = True
        except ImportError:
            HAS_STEALTH = False
            print("[WARN] playwright-stealth not installed (optional but recommended)")
            print("[WARN] Install with: pip install playwright-stealth")

        self.playwright = await async_playwright().start()

        # Launch with realistic settings
        self.browser = await self.playwright.chromium.launch(
            headless=self.headless,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--disable-dev-shm-usage",
                "--no-sandbox",
                "--disable-infobars",
                "--disable-background-timer-throttling",
                "--disable-popup-blocking",
                "--disable-backgrounding-occluded-windows",
            ],
        )

        # Create context with realistic fingerprint
        self.context = await self.browser.new_context(
            viewport={"width": 1920, "height": 1080},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            locale="en-US",
            timezone_id="America/New_York",
            color_scheme="light",
            device_scale_factor=1,
        )

        # Setup request interception
        self.page = await self.context.new_page()

        # Apply stealth patches if available
        if HAS_STEALTH:
            await stealth_async(self.page)
            print("[INFO] Stealth patches applied")

        # Intercept requests to capture tokens
        self.page.on("request", self._on_request)

        print("[INFO] Browser launched successfully")

    def _on_request(self, request):
        """Intercept requests to capture authentication tokens"""
        url = request.url

        # Look for requests to MS365 API
        if "checkout.microsoft365.com" in url and "/api/" in url:
            headers = request.headers

            bearer = headers.get("authorization", "")
            x_auth = headers.get("x-auth", "")

            if bearer and x_auth:
                # Capture cookies from context
                cookies_list = asyncio.get_event_loop().run_until_complete(
                    self.context.cookies()
                )
                cookies_str = "; ".join(
                    [f"{c['name']}={c['value']}" for c in cookies_list]
                )

                self.tokens = CapturedTokens(
                    bearer=bearer,
                    x_auth=x_auth,
                    cookies=cookies_str,
                    timestamp=time.time(),
                )
                print(f"[INFO] Tokens captured at {time.strftime('%H:%M:%S')}")

    async def navigate_to_checkout(self) -> bool:
        """Navigate to MS365 student checkout page"""
        # Build URL with params
        params = "&".join([f"{k}={v}" for k, v in CHECKOUT_PARAMS.items()])
        url = f"{MS365_CHECKOUT_URL}?{params}"

        print(f"[INFO] Navigating to checkout page...")
        print(f"[INFO] URL: {url}")

        try:
            await self.page.goto(url, wait_until="networkidle", timeout=60000)

            # Check if we need to sign in
            if (
                "login.microsoftonline.com" in self.page.url
                or "login.live.com" in self.page.url
            ):
                print("\n" + "=" * 50)
                print("   Microsoft Sign-In Required")
                print("=" * 50)
                print("   Please sign in to your Microsoft account")
                print("   in the browser window that opened.")
                print("   ")
                print("   Once signed in, the script will continue")
                print("   automatically.")
                print("=" * 50 + "\n")

                # Wait for sign-in to complete
                await self.page.wait_for_url(
                    "**/checkout.microsoft365.com/**",
                    timeout=300000,  # 5 minutes for sign-in
                )
                print("[INFO] Sign-in completed!")

            return True

        except Exception as e:
            print(f"[ERROR] Navigation failed: {e}")
            return False

    async def wait_for_tokens(self, timeout: int = 30) -> bool:
        """Wait for tokens to be captured from requests"""
        print("[INFO] Waiting for authentication tokens...")

        start = time.time()
        while time.time() - start < timeout:
            if self.tokens and self.tokens.is_valid:
                return True
            await asyncio.sleep(0.5)

        print("[WARN] Token capture timeout")
        return False

    async def trigger_verification_flow(self) -> bool:
        """Trigger the student verification flow on the page"""
        try:
            # Look for verification input or button
            # This varies based on page state

            # Try to find email input
            email_input = await self.page.query_selector('input[type="email"]')
            if email_input:
                print("[INFO] Found email input field")
                return True

            # Try to find verify button
            verify_btn = await self.page.query_selector('button:has-text("Verify")')
            if verify_btn:
                await verify_btn.click()
                await asyncio.sleep(2)
                return True

            print("[WARN] Could not find verification elements")
            return False

        except Exception as e:
            print(f"[ERROR] Failed to trigger verification: {e}")
            return False

    def verify_student_email(self, email: str) -> Dict:
        """
        Submit student email for verification
        This calls the MS365 internal API
        """
        if not self.tokens or not self.tokens.is_valid:
            return {"success": False, "error": "No valid tokens"}

        endpoint = f"{MS365_API_BASE}/verifystudent/sendemail"

        payload = {"email": email, "locale": "en-US"}

        try:
            with httpx.Client(timeout=30) as client:
                resp = client.post(
                    endpoint, json=payload, headers=self.tokens.to_headers()
                )

                if resp.status_code == 200:
                    data = resp.json()
                    return {
                        "success": True,
                        "message": "Verification email sent",
                        "data": data,
                    }
                else:
                    return {
                        "success": False,
                        "error": f"HTTP {resp.status_code}",
                        "body": resp.text,
                    }

        except Exception as e:
            return {"success": False, "error": str(e)}

    def check_verification_status(self) -> Dict:
        """Check current verification status"""
        if not self.tokens or not self.tokens.is_valid:
            return {"success": False, "error": "No valid tokens"}

        endpoint = f"{MS365_API_BASE}/verifystudent/status"

        try:
            with httpx.Client(timeout=30) as client:
                resp = client.get(endpoint, headers=self.tokens.to_headers())

                if resp.status_code == 200:
                    return {"success": True, "data": resp.json()}
                else:
                    return {"success": False, "error": f"HTTP {resp.status_code}"}

        except Exception as e:
            return {"success": False, "error": str(e)}

    async def upload_document_sheerid(self, first: str, last: str, school: str) -> Dict:
        """
        Fallback: Upload document via SheerID if embedded in page
        This is used when email verification fails
        """
        if not HAS_DOC_GEN:
            return {"success": False, "error": "doc_generator not available"}

        # Generate document
        print("[INFO] Generating student document...")
        if random.random() < 0.7:
            doc_bytes = generate_transcript(first, last, "2003-05-15", school)
            doc_name = "transcript.png"
        else:
            doc_bytes = generate_student_id(first, last, school)
            doc_name = "student_id.png"

        print(f"[INFO] Generated {doc_name} ({len(doc_bytes) / 1024:.1f} KB)")

        # Look for SheerID iframe or form in page
        try:
            sheerid_frame = await self.page.query_selector('iframe[src*="sheerid"]')
            if sheerid_frame:
                print("[INFO] Found SheerID verification frame")
                # Handle SheerID upload...
                # This would need more implementation based on actual page structure
                return {
                    "success": False,
                    "error": "SheerID frame handling not yet implemented",
                }
            else:
                return {"success": False, "error": "No SheerID frame found"}

        except Exception as e:
            return {"success": False, "error": str(e)}

    async def close(self):
        """Clean up browser resources"""
        if self.browser:
            await self.browser.close()
        if hasattr(self, "playwright"):
            await self.playwright.stop()


async def interactive_mode():
    """Interactive mode - opens browser for manual flow with token capture"""
    print("\n" + "=" * 60)
    print("   MS365 Education Verification Tool - Interactive Mode")
    print("=" * 60)

    verifier = MS365Verifier(headless=False)

    try:
        await verifier.launch_browser()

        if not await verifier.navigate_to_checkout():
            print("[ERROR] Failed to navigate to checkout")
            return

        print("\n" + "-" * 60)
        print("   Browser is open. Please complete the following steps:")
        print("-" * 60)
        print("   1. Sign in to your Microsoft account (if needed)")
        print("   2. Enter your student email when prompted")
        print("   3. Complete the verification process")
        print("")
        print("   The script will capture tokens automatically.")
        print("   Press Ctrl+C when done.")
        print("-" * 60 + "\n")

        # Keep running until user stops
        while True:
            await asyncio.sleep(1)

            if verifier.tokens and verifier.tokens.is_valid:
                print(
                    f"[STATUS] Tokens valid (captured {int(time.time() - verifier.tokens.timestamp)}s ago)"
                )

            await asyncio.sleep(4)

    except KeyboardInterrupt:
        print("\n[INFO] Stopped by user")
    finally:
        await verifier.close()


async def direct_mode(email: str, headless: bool = True):
    """Direct mode - automatically submit verification"""
    print("\n" + "=" * 60)
    print("   MS365 Education Verification Tool - Direct Mode")
    print("=" * 60)
    print(f"   Email: {email}")
    print("=" * 60 + "\n")

    verifier = MS365Verifier(headless=headless)

    try:
        await verifier.launch_browser()

        if not await verifier.navigate_to_checkout():
            print("[ERROR] Failed to navigate to checkout")
            return

        # Wait for tokens
        if not await verifier.wait_for_tokens(timeout=60):
            print("[ERROR] Could not capture tokens")
            return

        print("[INFO] Tokens captured, submitting verification...")

        # Submit email verification
        result = verifier.verify_student_email(email)

        if result.get("success"):
            print("\n" + "=" * 60)
            print("   SUCCESS!")
            print("=" * 60)
            print(f"   Verification email sent to: {email}")
            print("   Check your inbox and click the verification link.")
            print("=" * 60)
        else:
            print(f"\n[ERROR] Verification failed: {result.get('error')}")
            if result.get("body"):
                print(f"[DEBUG] Response: {result.get('body')[:200]}")

    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        await verifier.close()


async def token_export_mode():
    """Export captured tokens for use with other tools"""
    print("\n" + "=" * 60)
    print("   MS365 Token Export Mode")
    print("=" * 60)

    verifier = MS365Verifier(headless=False)

    try:
        await verifier.launch_browser()

        if not await verifier.navigate_to_checkout():
            return

        print("[INFO] Complete sign-in and any page interaction...")
        print("[INFO] Tokens will be saved when captured.")

        # Wait for tokens
        if await verifier.wait_for_tokens(timeout=120):
            # Save tokens to file
            tokens_file = Path(__file__).parent / "tokens.json"
            with open(tokens_file, "w") as f:
                json.dump(
                    {
                        "bearer": verifier.tokens.bearer,
                        "x_auth": verifier.tokens.x_auth,
                        "cookies": verifier.tokens.cookies,
                        "timestamp": verifier.tokens.timestamp,
                    },
                    f,
                    indent=2,
                )

            print(f"\n[SUCCESS] Tokens saved to: {tokens_file}")
            print("[INFO] You can now use these tokens with other tools.")
        else:
            print("[ERROR] Token capture failed")

    except KeyboardInterrupt:
        print("\n[INFO] Stopped by user")
    finally:
        await verifier.close()


def main():
    parser = argparse.ArgumentParser(
        description="Microsoft 365 Education Student Verification Tool"
    )
    parser.add_argument("--email", help="Student email for direct verification")
    parser.add_argument(
        "--headless", action="store_true", help="Run browser in headless mode"
    )
    parser.add_argument(
        "--export-tokens", action="store_true", help="Export captured tokens to file"
    )
    args = parser.parse_args()

    print()
    print("+" + "=" * 58 + "+")
    print("|" + " MS365 Education Verification Tool".center(58) + "|")
    print("|" + " Student Discount Automation".center(58) + "|")
    print("+" + "=" * 58 + "+")
    print()

    if args.export_tokens:
        asyncio.run(token_export_mode())
    elif args.email:
        asyncio.run(direct_mode(args.email, args.headless))
    else:
        asyncio.run(interactive_mode())


if __name__ == "__main__":
    main()
