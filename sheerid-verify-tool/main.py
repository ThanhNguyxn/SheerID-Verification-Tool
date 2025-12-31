#!/usr/bin/env python3
"""
SheerID Verification Tool - CLI
Unified verification tool for all services
"""

import sys
import argparse

# Add parent directory to path for imports
sys.path.insert(0, str(__file__).rsplit('\\', 1)[0])

from verifier import SheerIDVerifier
from config import PROGRAMS
from utils import stats


def print_banner():
    print()
    print("=" * 60)
    print("   🎓 SheerID Verification Tool")
    print("   Unified Student/Teacher Verification")
    print("=" * 60)
    print()


def print_services():
    print("   Available services:")
    print("   ─" * 25)
    for key, prog in PROGRAMS.items():
        print(f"   • {key:12} - {prog['name']} ({prog['type']})")
    print()


def main():
    parser = argparse.ArgumentParser(
        description="SheerID Verification Tool - Unified verification for all services",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py spotify "https://services.sheerid.com/verify/...?verificationId=..."
  python main.py boltnew "https://services.sheerid.com/verify/...?verificationId=..."
  python main.py k12 "https://services.sheerid.com/verify/...?verificationId=..."
  python main.py --stats
  python main.py --list
        """
    )
    
    parser.add_argument(
        "service",
        nargs="?",
        help="Service type (spotify, youtube, gemini, boltnew, gpt, k12)"
    )
    parser.add_argument(
        "url",
        nargs="?",
        help="Verification URL from SheerID"
    )
    parser.add_argument(
        "--stats",
        action="store_true",
        help="Show verification statistics"
    )
    parser.add_argument(
        "--list", "-l",
        action="store_true",
        help="List available services"
    )
    
    args = parser.parse_args()
    
    print_banner()
    
    # Show stats
    if args.stats:
        stats.print_stats()
        return
    
    # List services
    if args.list:
        print_services()
        return
    
    # Interactive mode if no args
    if not args.service or not args.url:
        print_services()
        
        # Get service
        service = input("   Enter service type: ").strip().lower()
        if service not in PROGRAMS:
            print(f"\n   [ERROR] Unknown service: {service}")
            return
        
        # Get URL
        url = input("   Enter verification URL: ").strip()
        if not url or "sheerid.com" not in url:
            print("\n   [ERROR] Invalid URL")
            return
    else:
        service = args.service.lower()
        url = args.url
        
        if service not in PROGRAMS:
            print(f"   [ERROR] Unknown service: {service}")
            print_services()
            return
        
        if "sheerid.com" not in url:
            print("   [ERROR] Invalid URL. Must contain sheerid.com")
            return
    
    # Run verification
    print(f"   [INFO] Starting verification...")
    
    verifier = SheerIDVerifier(url, service)
    result = verifier.verify()
    
    print()
    print("-" * 60)
    
    if result.get("success"):
        print("   ✅ SUCCESS!")
        print(f"   Name: {result.get('name')}")
        print(f"   Email: {result.get('email')}")
        print(f"   School: {result.get('school')}")
        print()
        print("   ⏳ Wait 24-48 hours for manual review")
    else:
        print(f"   ❌ FAILED: {result.get('error')}")
    
    print("-" * 60)
    
    # Show updated stats
    stats.print_stats()


if __name__ == "__main__":
    main()
