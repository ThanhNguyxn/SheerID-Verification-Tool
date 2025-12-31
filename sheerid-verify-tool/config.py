"""
SheerID Verification Tool - Configuration
All services configuration in one place
"""

# ============ PROGRAM IDS ============
PROGRAMS = {
    "spotify": {
        "id": "67c8c14f5f17a83b745e3f82",
        "name": "Spotify Premium Student",
        "type": "student"
    },
    "youtube": {
        "id": "67c8c14f5f17a83b745e3f82",
        "name": "YouTube Premium Student",
        "type": "student"
    },
    "gemini": {
        "id": "67c8c14f5f17a83b745e3f82",
        "name": "Google One AI Premium (Gemini)",
        "type": "student"
    },
    "boltnew": {
        "id": "68cc6a2e64f55220de204448",
        "name": "Bolt.new Teacher",
        "type": "teacher"
    },
    "gpt": {
        "id": "61c72b1539a20f1ac0ba56d6",
        "name": "ChatGPT Teacher",
        "type": "teacher"
    },
    "k12": {
        "id": "68d47554aa292d20b9bec8f7",
        "name": "K12 Teacher (High School)",
        "type": "k12_teacher"
    }
}

# ============ API URLS ============
SHEERID_BASE_URL = "https://services.sheerid.com"
SHEERID_API_URL = f"{SHEERID_BASE_URL}/rest/v2"

# ============ REQUEST SETTINGS ============
MIN_DELAY = 300  # ms
MAX_DELAY = 800  # ms
MAX_RETRIES = 3
REQUEST_TIMEOUT = 30

# ============ VALID STEPS ============
VALID_START_STEPS = [
    "collectStudentPersonalInfo",
    "collectTeacherPersonalInfo",
    "collectActiveMilitaryPersonalInfo",
    "collectInactiveMilitaryPersonalInfo"
]

# ============ ERROR TYPES ============
ERROR_TYPES = {
    "INVALID_STEP": "invalidStep",
    "EXPIRED_LINK": "expiredLink",
    "ORGANIZATION_NOT_FOUND": "organization_not_found",
    "RATE_LIMITED": "rateLimited",
    "SSO_REQUIRED": "ssoRequired",
    "VERIFICATION_LIMIT": "verificationLimitExceeded"
}
