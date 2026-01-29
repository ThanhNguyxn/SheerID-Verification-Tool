"""
Anti-Detection Module for SheerID Verification Tools
Shared module for better anti-fraud bypass

Features:
- Random User-Agent rotation (Chrome, Firefox, Edge, Safari)
- Browser-like headers with proper ordering
- Random fingerprint generation
- Request delay randomization
- TLS fingerprint spoofing with Chrome impersonation (curl_cffi)
- NewRelic tracking headers (required for SheerID)
- Canvas/WebGL fingerprint simulation
- Proxy validation and formatting

Usage:
    from anti_detect import get_headers, get_fingerprint, random_delay, create_session
    from anti_detect import generate_newrelic_headers  # For SheerID API calls
    from anti_detect import make_request  # High-level request with impersonation

CRITICAL: For best results, install curl_cffi:
    pip install curl_cffi

Without curl_cffi, SheerID can detect Python's TLS fingerprint and reject requests.
"""

import random
import hashlib
import time
import uuid
import base64
import json
import sys

# ============ CHROME IMPERSONATION VERSIONS ============
# These are the Chrome versions that curl_cffi can impersonate
# Updated Jan 2026 - use latest stable versions
CHROME_VERSIONS = [
    "chrome131",  # Chrome 131 (stable)
    "chrome130",  # Chrome 130
    "chrome124",  # Chrome 124
    "chrome123",  # Chrome 123
    "chrome120",  # Chrome 120
    "chrome119",  # Chrome 119
    "chrome116",  # Chrome 116
    "chrome110",  # Chrome 110
    "chrome107",  # Chrome 107
    "chrome104",  # Chrome 104
    "chrome101",  # Chrome 101
    "chrome100",  # Chrome 100
    "chrome99",  # Chrome 99
]

# Multiple browser types for rotation (curl_cffi supports these)
IMPERSONATE_OPTIONS = {
    "chrome": ["chrome131", "chrome130", "chrome124", "chrome120"],
    "edge": ["edge131", "edge127", "edge101"],
    "safari": ["safari18", "safari17_2_ios", "safari17_0"],
}

# Default impersonation - use latest stable
DEFAULT_IMPERSONATE = "chrome131"

# ============ USER AGENTS ============
# Real browser User-Agents (updated Jan 2026)
# IMPORTANT: These must match the Chrome version we're impersonating
USER_AGENTS_CHROME = [
    # Chrome 131 Windows (matches chrome131 impersonation)
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    # Chrome 131 Mac
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    # Chrome 130 Windows
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    # Chrome 130 Mac
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
]

# Legacy list for backwards compatibility
USER_AGENTS = [
    # Chrome Windows
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
    # Chrome Mac
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    # Chrome Linux
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    # Edge Windows (Chromium-based)
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
]

# ============ SCREEN RESOLUTIONS ============
RESOLUTIONS = [
    "1920x1080",
    "1366x768",
    "1536x864",
    "1440x900",
    "1280x720",
    "2560x1440",
    "1600x900",
    "1680x1050",
    "1280x800",
    "1024x768",
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
# Must match User-Agent for consistency
PLATFORMS = [
    (
        "Windows",
        '"Windows"',
        '"Chromium";v="131", "Google Chrome";v="131", "Not_A Brand";v="24"',
    ),
    (
        "Windows",
        '"Windows"',
        '"Chromium";v="130", "Google Chrome";v="130", "Not_A Brand";v="24"',
    ),
    (
        "macOS",
        '"macOS"',
        '"Chromium";v="131", "Google Chrome";v="131", "Not_A Brand";v="24"',
    ),
    (
        "Linux",
        '"Linux"',
        '"Chromium";v="131", "Google Chrome";v="131", "Not_A Brand";v="24"',
    ),
]

# ============ WEBGL VENDORS ============
WEBGL_VENDORS = [
    "Google Inc. (NVIDIA)",
    "Google Inc. (Intel)",
    "Google Inc. (AMD)",
    "Google Inc. (Apple)",
]

WEBGL_RENDERERS = [
    "ANGLE (NVIDIA GeForce GTX 1080 Direct3D11 vs_5_0 ps_5_0)",
    "ANGLE (NVIDIA GeForce RTX 3060 Direct3D11 vs_5_0 ps_5_0)",
    "ANGLE (Intel(R) UHD Graphics 630 Direct3D11 vs_5_0 ps_5_0)",
    "ANGLE (AMD Radeon RX 580 Direct3D11 vs_5_0 ps_5_0)",
    "ANGLE (Apple M1 Pro)",
]


def get_random_user_agent() -> str:
    """Get a random User-Agent string"""
    return random.choice(USER_AGENTS)


def get_fingerprint() -> str:
    """Generate realistic browser fingerprint hash"""
    components = [
        str(int(time.time() * 1000)),
        str(random.random()),
        random.choice(RESOLUTIONS),
        str(random.choice(TIMEZONES)),
        random.choice(LANGUAGES).split(",")[0],
        random.choice(["Win32", "MacIntel", "Linux x86_64"]),
        random.choice(["Google Inc.", "Apple Computer, Inc.", ""]),
        str(random.randint(2, 16)),  # CPU cores
        str(random.randint(4, 32)),  # Device memory
        str(random.randint(0, 1)),  # Touch support
        str(uuid.uuid4()),  # Session ID
    ]
    return hashlib.md5("|".join(components).encode()).hexdigest()


def get_canvas_fingerprint() -> str:
    """Generate a realistic canvas fingerprint hash"""
    # Simulate canvas toDataURL hash
    seed = str(time.time()) + str(random.random())
    return hashlib.sha256(seed.encode()).hexdigest()[:32]


def get_webgl_fingerprint() -> dict:
    """Generate WebGL fingerprint data"""
    return {
        "vendor": random.choice(WEBGL_VENDORS),
        "renderer": random.choice(WEBGL_RENDERERS),
        "hash": hashlib.md5(str(random.random()).encode()).hexdigest(),
    }


def get_audio_fingerprint() -> str:
    """Generate audio context fingerprint"""
    # Simulate AudioContext fingerprint
    return str(random.uniform(124.0, 124.1))[:15]


def get_full_fingerprint() -> dict:
    """Generate complete browser fingerprint for anti-detection"""
    screen = random.choice(RESOLUTIONS)
    width, height = screen.split("x")

    return {
        "hash": get_fingerprint(),
        "canvas": get_canvas_fingerprint(),
        "webgl": get_webgl_fingerprint(),
        "audio": get_audio_fingerprint(),
        "screen": {
            "width": int(width),
            "height": int(height),
            "colorDepth": random.choice([24, 32]),
            "pixelRatio": random.choice([1, 1.25, 1.5, 2]),
        },
        "timezone": random.choice(TIMEZONES),
        "language": random.choice(LANGUAGES).split(",")[0],
        "platform": random.choice(["Win32", "MacIntel", "Linux x86_64"]),
        "cpuCores": random.randint(2, 16),
        "memory": random.randint(4, 32),
        "touchSupport": random.choice([True, False]),
        "sessionId": str(uuid.uuid4()),
    }


def generate_newrelic_headers() -> dict:
    """
    Generate NewRelic tracking headers required by SheerID API
    These headers help make requests look like they're from real browsers
    """
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
            "ti": timestamp,
        },
    }

    return {
        "newrelic": base64.b64encode(json.dumps(payload).encode()).decode(),
        "traceparent": f"00-{trace_id}-{span_id}-01",
        "tracestate": f"364029@nr=0-1-364029-134291347-{span_id}----{timestamp}",
    }


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
        nr_headers = generate_newrelic_headers()
        headers.update(
            {
                "content-type": "application/json",
                "clientversion": "2.158.0",
                "clientname": "jslib",
                "origin": "https://services.sheerid.com",
                "referer": "https://services.sheerid.com/",
                **nr_headers,  # Include NewRelic tracking headers
            }
        )

    if with_auth:
        headers["authorization"] = f"Bearer {with_auth}"
        headers["origin"] = "https://chatgpt.com"
        headers["referer"] = "https://chatgpt.com/"
        headers["oai-device-id"] = str(uuid.uuid4())
        headers["oai-language"] = "en-US"

    return headers


def random_delay(min_ms: int = 300, max_ms: int = 1200):
    """
    Random delay with gamma distribution to mimic human behavior
    Gamma distribution is more realistic than uniform random
    """
    try:
        import numpy as np

        # Gamma distribution mimics human reaction times better
        shape, scale = 2.0, (max_ms - min_ms) / 4000
        delay = min_ms / 1000 + np.random.gamma(shape, scale)
        delay = min(delay, max_ms / 1000)  # Cap at max
    except ImportError:
        # Fallback to basic random with slight variation
        delay = random.randint(min_ms, max_ms) / 1000
        delay += random.uniform(0, 0.15)  # Add extra randomness

    time.sleep(delay)


def get_random_impersonate(browser_type: str = None) -> str:
    """
    Get random browser impersonation string for variety

    Args:
        browser_type: 'chrome', 'edge', 'safari' or None for weighted random

    Returns:
        Impersonation string like 'chrome131'
    """
    if browser_type and browser_type in IMPERSONATE_OPTIONS:
        return random.choice(IMPERSONATE_OPTIONS[browser_type])

    # Weight towards Chrome (most common, safest)
    weights = [0.75, 0.15, 0.10]
    browser = random.choices(["chrome", "edge", "safari"], weights=weights)[0]
    return random.choice(IMPERSONATE_OPTIONS[browser])


def validate_proxy(proxy: str) -> str:
    """Validate and format proxy string"""
    if not proxy:
        return None

    proxy = proxy.strip()

    # Already has scheme
    if "://" in proxy:
        return proxy

    parts = proxy.split(":")

    # host:port format
    if len(parts) == 2:
        return f"http://{parts[0]}:{parts[1]}"

    # host:port:user:pass format
    elif len(parts) == 4:
        return f"http://{parts[2]}:{parts[3]}@{parts[0]}:{parts[1]}"

    # user:pass@host:port format (already correct, just add scheme)
    elif "@" in proxy:
        return f"http://{proxy}"

    print(f"[WARN] Invalid proxy format: {proxy}")
    return None


def check_proxy_type(proxy: str) -> str:
    """
    Check if proxy is datacenter or residential
    Returns: 'residential', 'datacenter', 'unknown'
    """
    # This is a heuristic - actual check would require IP database lookup
    datacenter_indicators = [
        "vultr",
        "digitalocean",
        "linode",
        "aws",
        "azure",
        "gcp",
        "ovh",
        "hetzner",
        "contabo",
        "hostinger",
    ]

    residential_indicators = [
        "residential",
        "mobile",
        "isp",
        "roxy",
        "bright",
        "oxylabs",
        "smartproxy",
        "geosurf",
    ]

    proxy_lower = proxy.lower()

    for ind in residential_indicators:
        if ind in proxy_lower:
            return "residential"

    for ind in datacenter_indicators:
        if ind in proxy_lower:
            return "datacenter"

    return "unknown"


def get_proxy_country(proxy: str) -> str:
    """
    Try to determine proxy country from hostname
    Returns country code (US, NL, UK, etc.) or 'unknown'
    """
    country_indicators = {
        "us": ["us.", "-us-", ".us.", "america", "united-states"],
        "nl": ["nl.", "-nl-", ".nl.", "netherlands", "dutch", "amsterdam"],
        "uk": ["uk.", "-uk-", ".uk.", "london", "britain", "england"],
        "de": ["de.", "-de-", ".de.", "germany", "frankfurt", "berlin"],
        "fr": ["fr.", "-fr-", ".fr.", "france", "paris"],
        "ca": ["ca.", "-ca-", ".ca.", "canada", "toronto"],
        "au": ["au.", "-au-", ".au.", "australia", "sydney"],
    }

    proxy_lower = proxy.lower()

    for country, indicators in country_indicators.items():
        for ind in indicators:
            if ind in proxy_lower:
                return country.upper()

    return "unknown"


def get_matched_proxy(target_country: str, proxies: list) -> str:
    """
    Get proxy matching target country (for university location matching)

    Args:
        target_country: Country code (US, NL, UK, etc.)
        proxies: List of proxy URLs

    Returns:
        Matched proxy URL or random proxy if no match
    """
    if not proxies:
        return None

    target = target_country.upper()
    matched = []

    for proxy in proxies:
        proxy_country = get_proxy_country(proxy)
        if proxy_country == target:
            matched.append(proxy)

    if matched:
        return random.choice(matched)

    # No match - return random residential if available
    residential = [p for p in proxies if check_proxy_type(p) == "residential"]
    if residential:
        return random.choice(residential)

    return random.choice(proxies)


def create_session(proxy: str = None, impersonate: str = None):
    """
    Create HTTP session with best available library
    Priority: curl_cffi (with impersonation) > cloudscraper > httpx > requests

    CRITICAL: curl_cffi with Chrome impersonation is STRONGLY recommended.
    Without it, SheerID can detect Python's TLS fingerprint (JA3/JA4).

    Args:
        proxy: Proxy URL (will be formatted if needed)
        impersonate: Chrome version to impersonate (e.g., "chrome131")
                    If None, uses DEFAULT_IMPERSONATE

    Returns:
        tuple: (session, library_name, impersonate_version)
    """
    # Validate and format proxy
    proxy = validate_proxy(proxy)
    proxies = None
    if proxy:
        proxies = {"http": proxy, "https": proxy, "all://": proxy}

        # Warn if using datacenter proxy
        proxy_type = check_proxy_type(proxy)
        if proxy_type == "datacenter":
            print("[WARN] ⚠️  Datacenter proxy detected! SheerID may reject requests.")
            print("[WARN]    Residential proxies are STRONGLY recommended.")

    # Determine impersonation version
    imp_version = impersonate or DEFAULT_IMPERSONATE

    # Try curl_cffi first (BEST - TLS fingerprint spoofing)
    try:
        from curl_cffi import requests as curl_requests

        # Test if impersonation is supported
        try:
            if proxies:
                session = curl_requests.Session(
                    proxies=proxies, impersonate=imp_version
                )
            else:
                session = curl_requests.Session(impersonate=imp_version)

            print(f"[Anti-Detect] ✅ Using curl_cffi with {imp_version} impersonation")
            print(f"[Anti-Detect]    TLS fingerprint will match real Chrome browser")
            return session, "curl_cffi", imp_version

        except Exception as e:
            # Try without impersonation if version not supported
            print(
                f"[WARN] Impersonation '{imp_version}' not supported, trying fallback..."
            )

            # Try older versions
            for fallback_ver in ["chrome120", "chrome110", "chrome100"]:
                try:
                    if proxies:
                        session = curl_requests.Session(
                            proxies=proxies, impersonate=fallback_ver
                        )
                    else:
                        session = curl_requests.Session(impersonate=fallback_ver)
                    print(
                        f"[Anti-Detect] ✅ Using curl_cffi with {fallback_ver} impersonation"
                    )
                    return session, "curl_cffi", fallback_ver
                except:
                    continue

            # Last resort - no impersonation
            if proxies:
                session = curl_requests.Session(proxies=proxies)
            else:
                session = curl_requests.Session()
            print("[Anti-Detect] ⚠️  curl_cffi loaded but impersonation failed")
            print("[Anti-Detect]    TLS fingerprint may be detectable!")
            return session, "curl_cffi", None

    except ImportError:
        print("\n" + "=" * 60)
        print("⚠️  CRITICAL: curl_cffi NOT INSTALLED!")
        print("=" * 60)
        print("Without curl_cffi, your TLS fingerprint is DETECTABLE.")
        print("SheerID will likely REJECT your verification attempts.")
        print("")
        print("Install now with: pip install curl_cffi")
        print("=" * 60 + "\n")

    # Try cloudscraper (Cloudflare bypass, but no TLS spoofing)
    try:
        import cloudscraper

        session = cloudscraper.create_scraper(
            browser={"browser": "chrome", "platform": "windows", "mobile": False}
        )
        if proxies:
            session.proxies = proxies
        print("[Anti-Detect] ⚠️  Using cloudscraper (no TLS impersonation)")
        return session, "cloudscraper", None
    except ImportError:
        pass

    # Try httpx (async support, but detectable TLS)
    try:
        import httpx

        proxy_url = proxies.get("all://") if proxies else None
        session = httpx.Client(timeout=30, proxy=proxy_url)
        print("[Anti-Detect] ⚠️  Using httpx (TLS fingerprint DETECTABLE!)")
        print(
            "[Anti-Detect]    Expected success rate: ~20-40% (vs 60-80% with curl_cffi)"
        )
        return session, "httpx", None
    except ImportError:
        pass

    # Fallback to requests (most detectable)
    import requests

    session = requests.Session()
    if proxies:
        session.proxies = proxies
    print("[Anti-Detect] ❌ Using requests (VERY HIGH detection risk!)")
    print("[Anti-Detect]    Expected success rate: ~5-20%")
    print("[Anti-Detect]    Run: pip install curl_cffi")
    return session, "requests", None


def print_anti_detect_info():
    """Print info about anti-detection configuration"""
    session, lib, imp = create_session()
    print(f"\n{'=' * 50}")
    print(f"Anti-Detection Configuration")
    print(f"{'=' * 50}")
    print(f"  HTTP Library: {lib}")
    print(f"  Impersonation: {imp or 'None (detectable!)'}")
    print(f"  User-Agents: {len(USER_AGENTS)} variants")
    print(f"  Resolutions: {len(RESOLUTIONS)} variants")
    print(f"  Chrome Versions: {len(CHROME_VERSIONS)} available")

    if lib == "curl_cffi" and imp:
        print(f"\n  ✅ TLS Fingerprint: Spoofed as {imp}")
        print(f"  ✅ Detection Risk: LOW")
    elif lib == "curl_cffi":
        print(f"\n  ⚠️  TLS Fingerprint: Partially spoofed")
        print(f"  ⚠️  Detection Risk: MEDIUM")
    else:
        print(f"\n  ❌ TLS Fingerprint: Python signature (detectable)")
        print(f"  ❌ Detection Risk: HIGH")

    print(f"{'=' * 50}\n")

    # Cleanup
    if hasattr(session, "close"):
        session.close()


def make_request(session, method: str, url: str, impersonate: str = None, **kwargs):
    """
    Make HTTP request with proper impersonation for curl_cffi

    This is a helper to ensure impersonation is used per-request
    for libraries that support it.

    Args:
        session: HTTP session from create_session()
        method: HTTP method (GET, POST, PUT, DELETE)
        url: Request URL
        impersonate: Chrome version to impersonate (for curl_cffi)
        **kwargs: Additional arguments (json, headers, etc.)

    Returns:
        Response object
    """
    imp = impersonate or DEFAULT_IMPERSONATE

    # Check if this is a curl_cffi session
    session_type = type(session).__module__

    if "curl_cffi" in session_type:
        # curl_cffi supports per-request impersonation
        try:
            return session.request(method, url, impersonate=imp, **kwargs)
        except TypeError:
            # Older version doesn't support per-request impersonate
            return session.request(method, url, **kwargs)
    else:
        # Other libraries - just make the request
        return session.request(method, url, **kwargs)


def get_matched_ua_for_impersonate(impersonate: str = None) -> str:
    """
    Get a User-Agent that matches the Chrome version we're impersonating

    IMPORTANT: The User-Agent MUST match the TLS fingerprint version,
    otherwise SheerID can detect the mismatch.
    """
    imp = impersonate or DEFAULT_IMPERSONATE

    # Extract version number
    version = imp.replace("chrome", "").replace("edge", "").replace("safari", "")

    # Find matching UA
    for ua in USER_AGENTS_CHROME:
        if f"Chrome/{version}." in ua:
            return ua

    # Fallback to first Chrome UA
    return USER_AGENTS_CHROME[0]


def warm_session(session, program_id: str = None, headers: dict = None):
    """
    Warm up session before verification attempt
    Makes requests look more like a real browser by establishing session first

    Args:
        session: HTTP session from create_session()
        program_id: SheerID program ID (optional)
        headers: Headers to use (optional)

    Returns:
        session: Warmed up session
    """
    base_url = "https://services.sheerid.com"
    hdrs = headers or get_headers(for_sheerid=True)

    try:
        # Step 1: Load main API (like browser would on page load)
        session.get(f"{base_url}/rest/v2/config", headers=hdrs, timeout=10)
        random_delay(500, 1000)
    except:
        pass

    if program_id:
        try:
            # Step 2: Load program info
            session.get(
                f"{base_url}/rest/v2/program/{program_id}", headers=hdrs, timeout=10
            )
            random_delay(300, 700)
        except:
            pass

    try:
        # Step 3: Check organization endpoint (search with empty term)
        params = {"country": "US", "term": ""}
        if program_id:
            params["programId"] = program_id
        session.get(
            f"{base_url}/rest/v2/organization/search",
            params=params,
            headers=hdrs,
            timeout=10,
        )
        random_delay(200, 500)
    except:
        pass

    return session


def generate_student_email(
    first_name: str, last_name: str, university: dict = None
) -> str:
    """
    Generate realistic student email matching university domain

    Args:
        first_name: Student first name
        last_name: Student last name
        university: University dict with 'domain' key (optional)

    Returns:
        Generated email address
    """
    first = first_name.lower().strip()
    last = last_name.lower().strip()

    domain = university.get("domain", "") if university else ""

    if not domain:
        # Generic email providers
        domains = ["gmail.com", "outlook.com", "yahoo.com", "icloud.com"]
        domain = random.choice(domains)

    # Common university email patterns
    patterns = [
        f"{first[0]}{last}@{domain}",  # jsmith@university.edu
        f"{first}.{last}@{domain}",  # john.smith@university.edu
        f"{first}{last[0]}@{domain}",  # johns@university.edu
        f"{first}_{last}@{domain}",  # john_smith@university.edu
        f"{last}{first[0]}@{domain}",  # smithj@university.edu
        f"{first}{random.randint(1, 99)}@{domain}",  # john42@university.edu
    ]

    return random.choice(patterns)


FRAUD_ERROR_HELP = """\
🚨 Fraud Rule Rejection Detected (fraudRulesReject)

SheerID's fraud/risk engine rejected this attempt. This is usually triggered by one or more risk signals:
- TLS fingerprint mismatch (Python http stacks vs real browsers)
- Datacenter / flagged IP reputation
- Reused device fingerprint / headers / NewRelic patterns across attempts
- High retry velocity or repeated failures from the same IP
- Geo mismatch (IP country/region vs organization)

✅ Workarounds (try these, in order):
  1) Install curl_cffi for TLS spoofing:
     pip install curl_cffi
  2) Use a residential proxy instead of a datacenter proxy
  3) Wait 24-48 hours before retrying (risk score often cools down)
  4) Try a different university/organization (some are stricter)
  5) Check if your IP is blacklisted (switch IP / provider if needed)

Notes:
- Retrying instantly with the same IP + fingerprint can make the block stick longer.
- If you cannot install curl_cffi, expect a much higher fraud reject rate.
"""


def should_retry_fraud(retry_count: int):
    """Decide whether to retry after a fraudRulesReject.

    Implements a capped exponential backoff schedule:
    - 30s, 60s, 120s
    - max 3 retries

    Args:
        retry_count: Number of retries already attempted (0-based).

    Returns:
        (should_retry, delay_seconds)
    """
    if retry_count < 0:
        retry_count = 0

    backoff_schedule = [30, 60, 120]

    if retry_count >= len(backoff_schedule):
        return False, 0

    return True, backoff_schedule[retry_count]


def handle_fraud_rejection(
    *,
    retry_count: int = 0,
    error_payload=None,
    message: str = None,
):
    """Print a visible fraud banner + actionable help, then return retry guidance.

    This handler is intended to be called when SheerID responds with
    the `fraudRulesReject` error.

    Args:
        retry_count: Number of retries already attempted (0-based).
        error_payload: Optional API error JSON payload to display (best-effort).
        message: Optional human-readable message/context to display.

    Returns:
        (should_retry, delay_seconds)
    """
    # ANSI colors (no external deps). If terminal doesn't support ANSI, output is still readable.
    red = "\x1b[31m"
    yellow = "\x1b[33m"
    cyan = "\x1b[36m"
    bold = "\x1b[1m"
    reset = "\x1b[0m"

    banner = "\n".join(
        [
            "+--------------------------------------------------------------+",
            "|                  !!! FRAUD DETECTION HIT !!!                 |",
            "|                 SheerID returned fraudRulesReject             |",
            "+--------------------------------------------------------------+",
        ]
    )

    print(f"\n{red}{bold}{banner}{reset}")
    print(f"{yellow}❌ Verification blocked by SheerID fraud rules.{reset}")

    if message:
        print(f"{cyan}🧾 Context:{reset} {message}")

    # Best-effort extraction of useful fields without assuming a strict schema.
    if isinstance(error_payload, dict) and error_payload:
        interesting_keys = [
            "code",
            "errorCode",
            "message",
            "detail",
            "details",
            "error",
            "errors",
        ]
        extracted = {}
        for k in interesting_keys:
            if k in error_payload and error_payload.get(k) not in (None, ""):
                extracted[k] = error_payload.get(k)

        if extracted:
            # Keep this compact to avoid dumping huge payloads into the console.
            print(f"{cyan}🔎 SheerID error payload (high-signal fields):{reset}")
            for k, v in extracted.items():
                v_str = str(v)
                if len(v_str) > 400:
                    v_str = v_str[:400] + "..."
                print(f"  - {k}: {v_str}")

    print("\n" + "=" * 62)
    print(FRAUD_ERROR_HELP)
    print("=" * 62)

    should_retry, delay_seconds = should_retry_fraud(retry_count)
    if should_retry:
        print(
            f"{yellow}⏳ Suggested retry:{reset} attempt #{retry_count + 1}/3 in {delay_seconds}s"
        )
        print(
            f"{yellow}💡 Tip:{reset} rotate IP/fingerprint before retrying; avoid rapid-fire retries."
        )
    else:
        print(f"{red}🛑 Max retries reached.{reset} Do NOT keep spamming requests.")
        print(
            f"{yellow}✅ Best next step:{reset} wait 24-48h and change IP/fingerprint."
        )

    return should_retry, delay_seconds


if __name__ == "__main__":
    # Test
    print("\n" + "=" * 60)
    print(" Anti-Detection Module Test ")
    print("=" * 60 + "\n")

    print_anti_detect_info()

    print(f"Sample Fingerprints:")
    print(f"  Basic Hash: {get_fingerprint()}")
    print(f"  Canvas FP: {get_canvas_fingerprint()}")
    print(f"  Audio FP: {get_audio_fingerprint()}")

    webgl = get_webgl_fingerprint()
    print(f"  WebGL Vendor: {webgl['vendor']}")
    print(f"  WebGL Renderer: {webgl['renderer'][:40]}...")

    print(f"\nSample User-Agent:")
    ua = get_matched_ua_for_impersonate()
    print(f"  {ua[:70]}...")

    print(f"\nSample Headers (SheerID):")
    headers = get_headers(for_sheerid=True)
    for k, v in list(headers.items())[:8]:
        print(f"  {k}: {str(v)[:50]}{'...' if len(str(v)) > 50 else ''}")

    print(f"\nNewRelic Headers:")
    nr = generate_newrelic_headers()
    print(f"  traceparent: {nr['traceparent'][:50]}...")

    print("\n" + "=" * 60)
    print(" Recommendations ")
    print("=" * 60)
    print("""
1. Install curl_cffi for TLS spoofing:
   pip install curl_cffi

2. Use residential proxies (datacenter IPs are often blocked)

3. Match proxy location to university country

4. Generate unique fingerprints for each verification attempt
""")
