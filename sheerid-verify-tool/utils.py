"""
SheerID Verification Tool - Utilities
Retry logic, stats tracking, fingerprint generation
"""

import time
import random
import hashlib
import json
from pathlib import Path
from typing import Callable, Any, Dict, Optional
from functools import wraps

# ============ STATS TRACKING ============
class VerificationStats:
    """Track success rates by university/school"""
    
    def __init__(self, stats_file: str = "stats.json"):
        self.stats_file = Path(__file__).parent / stats_file
        self.stats = self._load_stats()
    
    def _load_stats(self) -> Dict:
        if self.stats_file.exists():
            try:
                return json.loads(self.stats_file.read_text())
            except:
                pass
        return {"total": 0, "success": 0, "failed": 0, "by_organization": {}}
    
    def _save_stats(self):
        self.stats_file.write_text(json.dumps(self.stats, indent=2))
    
    def record_success(self, org_name: str):
        self.stats["total"] += 1
        self.stats["success"] += 1
        
        if org_name not in self.stats["by_organization"]:
            self.stats["by_organization"][org_name] = {"success": 0, "failed": 0}
        self.stats["by_organization"][org_name]["success"] += 1
        
        self._save_stats()
    
    def record_failure(self, org_name: str):
        self.stats["total"] += 1
        self.stats["failed"] += 1
        
        if org_name not in self.stats["by_organization"]:
            self.stats["by_organization"][org_name] = {"success": 0, "failed": 0}
        self.stats["by_organization"][org_name]["failed"] += 1
        
        self._save_stats()
    
    def get_success_rate(self) -> float:
        if self.stats["total"] == 0:
            return 0.0
        return self.stats["success"] / self.stats["total"] * 100
    
    def get_org_success_rate(self, org_name: str) -> float:
        if org_name not in self.stats["by_organization"]:
            return 50.0  # Default for new orgs
        org = self.stats["by_organization"][org_name]
        total = org["success"] + org["failed"]
        if total == 0:
            return 50.0
        return org["success"] / total * 100
    
    def get_best_organizations(self, top_n: int = 5) -> list:
        """Get top performing organizations"""
        orgs = []
        for name, data in self.stats["by_organization"].items():
            total = data["success"] + data["failed"]
            if total >= 3:  # Minimum attempts
                rate = data["success"] / total * 100
                orgs.append((name, rate, total))
        
        orgs.sort(key=lambda x: (-x[1], -x[2]))  # Sort by rate desc, then by total desc
        return orgs[:top_n]
    
    def print_stats(self):
        print(f"\n📊 Verification Statistics:")
        print(f"   Total: {self.stats['total']} | Success: {self.stats['success']} | Failed: {self.stats['failed']}")
        print(f"   Success Rate: {self.get_success_rate():.1f}%")
        
        best = self.get_best_organizations(3)
        if best:
            print(f"   Top Organizations:")
            for name, rate, total in best:
                print(f"      - {name[:40]}: {rate:.0f}% ({total} attempts)")


# Global stats instance
stats = VerificationStats()


# ============ RETRY LOGIC ============
def retry_with_backoff(max_retries: int = 3, base_delay: float = 1.0):
    """Decorator for retry with exponential backoff"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_exception = None
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_retries - 1:
                        delay = base_delay * (2 ** attempt) + random.uniform(0, 1)
                        print(f"      Retry {attempt + 1}/{max_retries} in {delay:.1f}s...")
                        time.sleep(delay)
            raise last_exception
        return wrapper
    return decorator


def random_delay(min_ms: int = 300, max_ms: int = 800):
    """Add random delay to avoid rate limiting"""
    delay = random.randint(min_ms, max_ms) / 1000
    time.sleep(delay)


# ============ FINGERPRINT GENERATION ============
def generate_fingerprint() -> str:
    """Generate realistic device fingerprint"""
    screens = ["1920x1080", "2560x1440", "1366x768", "1536x864", "1440x900"]
    timezones = ["-480", "-420", "-360", "-300", "-240", "0", "60", "120"]
    
    components = [
        random.choice(screens),
        random.choice(timezones),
        str(random.randint(1, 32)),  # cores
        str(random.randint(4, 64)),  # memory
        "24",  # color depth
        str(time.time()),
        str(random.random())
    ]
    
    raw = "|".join(components)
    return hashlib.md5(raw.encode()).hexdigest()


# ============ NAME GENERATION ============
FIRST_NAMES = [
    "James", "John", "Robert", "Michael", "William", "David", "Richard", "Joseph",
    "Thomas", "Christopher", "Mary", "Patricia", "Jennifer", "Linda", "Elizabeth",
    "Barbara", "Susan", "Jessica", "Sarah", "Karen", "Daniel", "Matthew", "Anthony",
    "Mark", "Donald", "Steven", "Andrew", "Paul", "Joshua", "Kenneth", "Emma",
    "Olivia", "Ava", "Isabella", "Sophia", "Mia", "Charlotte", "Amelia", "Harper"
]

LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
    "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
    "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson",
    "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker"
]


def generate_name() -> tuple:
    """Generate random first and last name"""
    return random.choice(FIRST_NAMES), random.choice(LAST_NAMES)


def generate_email(first_name: str, last_name: str, domain: str = None) -> str:
    """Generate email address"""
    suffix = random.randint(100, 9999)
    patterns = [
        f"{first_name[0].lower()}{last_name.lower()}{suffix}",
        f"{first_name.lower()}.{last_name.lower()}{suffix}",
        f"{first_name.lower()}{last_name[0].lower()}{suffix}",
        f"{last_name.lower()}{first_name[0].lower()}{suffix}"
    ]
    username = random.choice(patterns)
    
    if domain:
        return f"{username}@{domain}"
    else:
        domains = ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com"]
        return f"{username}@{random.choice(domains)}"


def generate_birth_date(min_age: int = 18, max_age: int = 25) -> str:
    """Generate random birth date within age range"""
    import datetime
    today = datetime.date.today()
    
    min_year = today.year - max_age
    max_year = today.year - min_age
    
    year = random.randint(min_year, max_year)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    
    return f"{year}-{month:02d}-{day:02d}"
