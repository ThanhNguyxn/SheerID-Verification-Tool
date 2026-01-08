"""
Anti-Detection Module for SheerID Verification Tools
Shared module for better anti-fraud bypass

Features:
- Random User-Agent rotation (Chrome, Firefox, Edge, Safari)
- Browser-like headers with proper ordering
- Random fingerprint generation
- Request delay randomization
- TLS fingerprint spoofing (if curl_cffi available)

Usage:
    from anti_detect import get_headers, get_fingerprint, random_delay, create_session
"""

import random
import hashlib
import time
import uuid

# ============ USER AGENTS ============
# Real browser User-Agents (updated Jan 2025)
USER_AGENTS = [
    # Chrome Windows
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
    # Chrome Mac
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    # Firefox Windows
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:132.0) Gecko/20100101 Firefox/132.0",
    # Firefox Mac
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:133.0) Gecko/20100101 Firefox/133.0",
    # Edge
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
    # Safari Mac
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1 Safari/605.1.15",
]

# ============ SCREEN RESOLUTIONS ============
RESOLUTIONS = [
    "1920x1080", "1366x768", "1536x864", "1440x900", "1280x720",
    "2560x1440", "1600x900", "1680x1050", "1280x800", "1024x768"
]

# ============ TIMEZONES ============
TIMEZONES = [-8, -7, -6, -5, -4, -3, 0, 1, 2, 3, 5.5, 8, 9, 10]

# ============ LANGUAGES ============
LANGUAGES = [
    "en-US,en;q=0.9",
    "en-US,en;q=0.9,es;q=0.8",
    "en-GB,en;q=0.9",
    "en-CA,en;q=0.9",
    "en-AU,en;q=0.9",
]

# ============ PLATFORMS ============
PLATFORMS = [
    ("Windows", '"Windows"', '"Chromium";v="131", "Google Chrome";v="131"'),
    ("Windows", '"Windows"', '"Chromium";v="130", "Google Chrome";v="130"'),
    ("macOS", '"macOS"', '"Chromium";v="131", "Google Chrome";v="131"'),
    ("Linux", '"Linux"', '"Chromium";v="131", "Google Chrome";v="131"'),
]


def get_random_user_agent() -> str:
    """Get a random User-Agent string"""
    return random.choice(USER_AGENTS)


def get_fingerprint() -> str:
    """Generate realistic browser fingerprint"""
    components = [
        str(int(time.time() * 1000)),
        str(random.random()),
        random.choice(RESOLUTIONS),
        str(random.choice(TIMEZONES)),
        random.choice(LANGUAGES).split(",")[0],
        random.choice(["Win32", "MacIntel", "Linux x86_64"]),
        random.choice(["Google Inc.", "Apple Computer, Inc.", ""]),
        str(random.randint(2, 16)),   # CPU cores
        str(random.randint(4, 32)),   # Device memory
        str(random.randint(0, 1)),    # Touch support
        str(uuid.uuid4()),            # Session ID
    ]
    return hashlib.md5("|".join(components).encode()).hexdigest()


def get_headers(for_sheerid: bool = True, with_auth: str = None) -> dict:
    """
    Generate browser-like headers with proper ordering
    
    Args:
        for_sheerid: If True, use SheerID-specific headers
        with_auth: Bearer token for Authorization header
    """
    ua = get_random_user_agent()
    platform = random.choice(PLATFORMS)
    language = random.choice(LANGUAGES)
    
    # Base headers (proper ordering like real browser)
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": language,
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "sec-ch-ua": platform[2],
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": platform[1],
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": ua,
    }
    
    if for_sheerid:
        headers.update({
            "content-type": "application/json",
            "clientversion": "2.157.0",
            "clientname": "jslib",
            "origin": "https://services.sheerid.com",
            "referer": "https://services.sheerid.com/",
        })
    
    if with_auth:
        headers["authorization"] = f"Bearer {with_auth}"
        headers["origin"] = "https://chatgpt.com"
        headers["referer"] = "https://chatgpt.com/"
        headers["oai-device-id"] = str(uuid.uuid4())
        headers["oai-language"] = "en-US"
    
    return headers


def random_delay(min_ms: int = 200, max_ms: int = 800):
    """Random delay to avoid detection"""
    time.sleep(random.randint(min_ms, max_ms) / 1000)


def create_session(proxy: str = None):
    """
    Create HTTP session with best available library
    Priority: curl_cffi > cloudscraper > httpx > requests
    
    Returns:
        tuple: (session, library_name)
    """
    proxies = None
    if proxy:
        if "://" not in proxy:
            parts = proxy.split(":")
            if len(parts) == 2:
                proxy = f"http://{parts[0]}:{parts[1]}"
            elif len(parts) == 4:
                proxy = f"http://{parts[2]}:{parts[3]}@{parts[0]}:{parts[1]}"
        proxies = {"http": proxy, "https": proxy, "all://": proxy}
    
    # Try curl_cffi first (best TLS fingerprint spoofing)
    try:
        from curl_cffi import requests as curl_requests
        session = curl_requests.Session(impersonate="chrome131", proxies=proxies)
        return session, "curl_cffi"
    except ImportError:
        pass
    
    # Try cloudscraper (Cloudflare bypass)
    try:
        import cloudscraper
        session = cloudscraper.create_scraper(
            browser={'browser': 'chrome', 'platform': 'windows', 'mobile': False}
        )
        if proxies:
            session.proxies = proxies
        return session, "cloudscraper"
    except ImportError:
        pass
    
    # Try httpx
    try:
        import httpx
        proxy_url = proxies.get("all://") if proxies else None
        session = httpx.Client(timeout=30, proxy=proxy_url)
        return session, "httpx"
    except ImportError:
        pass
    
    # Fallback to requests
    import requests
    session = requests.Session()
    if proxies:
        session.proxies = proxies
    return session, "requests"


def print_anti_detect_info():
    """Print info about anti-detection configuration"""
    _, lib = create_session()
    print(f"[Anti-Detect] Using {lib} for HTTP requests")
    print(f"[Anti-Detect] User-Agents: {len(USER_AGENTS)} variants")
    print(f"[Anti-Detect] Resolutions: {len(RESOLUTIONS)} variants")


if __name__ == "__main__":
    # Test
    print("Anti-Detection Module Test")
    print("-" * 40)
    print_anti_detect_info()
    print(f"\nSample UA: {get_random_user_agent()[:60]}...")
    print(f"Sample FP: {get_fingerprint()}")
    print(f"\nSample Headers:")
    for k, v in get_headers().items():
        print(f"  {k}: {v[:50]}{'...' if len(v) > 50 else ''}")
