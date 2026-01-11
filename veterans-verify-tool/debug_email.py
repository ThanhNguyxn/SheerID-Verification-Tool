import imaplib
import json
import sys
import os
from pathlib import Path

def debug_email():
    print("=== Email Connection Debugger ===")
    
    config_path = Path("config.json")
    if not config_path.exists():
        print("[ERROR] config.json not found")
        return

    try:
        config = json.loads(config_path.read_text(encoding="utf-8"))
        email_config = config.get("email", {})
    except Exception as e:
        print(f"[ERROR] Failed to parse config.json: {e}")
        return

    server = email_config.get("imap_server")
    port = email_config.get("imap_port")
    user = email_config.get("email_address")
    password = email_config.get("email_password")
    use_ssl = email_config.get("use_ssl", True)

    print(f"Server: {server}")
    print(f"Port: {port}")
    print(f"User: {user}")
    print(f"SSL: {use_ssl}")
    print(f"Password length: {len(password) if password else 0}")

    if not all([server, port, user, password]):
        print("[ERROR] Missing email configuration fields")
        return

    print("\nAttempting connection...")
    try:
        if use_ssl:
            print(f"Connecting to {server}:{port} over SSL...")
            mail = imaplib.IMAP4_SSL(server, port)
        else:
            print(f"Connecting to {server}:{port} (No SSL)...")
            mail = imaplib.IMAP4(server, port)
        
        print("Connection established. Attempting login...")
        try:
            mail.login(user, password)
            print("[SUCCESS] Login successful!")
            
            print("Listing mailboxes...")
            status, boxes = mail.list()
            if status == 'OK':
                print(f"Found {len(boxes)} mailboxes.")
            else:
                print(f"[WARN] Could not list mailboxes: {status}")
                
            mail.logout()
            
        except imaplib.IMAP4.error as e:
            print(f"\n[FAIL] Login failed: {e}")
            print("Possible causes:")
            print("1. App Password is incorrect (check for spaces?)")
            print("2. IMAP is disabled in account settings")
            print("3. 'Less secure apps' is blocked")
            print(f"4. User '{user}' does not match the password account")
            
    except Exception as e:
        print(f"\n[FAIL] Connection error: {e}")

if __name__ == "__main__":
    # Ensure we are in the right directory
    if Path("veterans-verify-tool").exists():
        os.chdir("veterans-verify-tool")
    elif Path("main.py").exists() and Path("config.json").exists():
        pass # Already in the tool dir
        
    import os
    if not Path("config.json").exists():
         # Try to find where we are
         if Path("veterans-verify-tool/config.json").exists():
             os.chdir("veterans-verify-tool")
    
    debug_email()
