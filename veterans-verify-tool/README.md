# Veterans Verification Tool

ChatGPT Plus verification tool for US Veterans using SheerID.

## Requirements

- Python 3.8+
- `requests` library

## Quick Start

### 1. Install dependencies

```bash
pip install requests
```

### 2. Configure

Copy `config.example.json` to `config.json`:

```bash
cp config.example.json config.json
```

Edit `config.json`:

```json
{
    "accessToken": "YOUR_CHATGPT_ACCESS_TOKEN",
    "programId": "690415d58971e73ca187d8c9",
    "email": {
        "imap_server": "imap.gmail.com",
        "imap_port": 993,
        "email_address": "your_email@gmail.com",
        "email_password": "your_app_password",
        "use_ssl": true
    }
}
```

#### How to get accessToken

1. Login to https://chatgpt.com
2. Open browser DevTools (F12) → Console
3. Visit https://chatgpt.com/api/auth/session
4. Find and copy the `accessToken` value

#### Email Configuration

For Gmail:
1. Enable 2-Step Verification in Google Account
2. Go to Security → App passwords
3. Create a new app password for "Mail"
4. Use this password in `email_password`

Common IMAP servers:
| Provider | IMAP Server | Port |
|----------|-------------|------|
| Gmail | imap.gmail.com | 993 |
| Outlook | outlook.office365.com | 993 |
| Yahoo | imap.mail.yahoo.com | 993 |

### 3. Add veteran data

Copy `data.example.txt` to `data.txt`:

```bash
cp data.example.txt data.txt
```

Add veteran data (one per line):

```
JOHN|SMITH|Army|1990-05-15|2025-06-01
DAVID|JOHNSON|Marine Corps|1988-12-20|2025-03-15
```

Format: `firstName|lastName|branch|birthDate|dischargeDate`

**Supported branches:**
- Army, Navy, Air Force, Marine Corps, Coast Guard, Space Force
- Army National Guard, Army Reserve
- Air National Guard, Air Force Reserve
- Navy Reserve, Marine Corps Reserve, Coast Guard Reserve

**Date format:** YYYY-MM-DD

> **Note:** Discharge date should be within the last 12 months for eligibility.

### 4. Run

```bash
python main.py
```

---

## CLI Options

| Option | Required | Description |
|--------|----------|-------------|
| `--proxy HOST:PORT` | No | Use a proxy server |
| `--no-dedup` | No | Disable deduplication check |

### Examples

```bash
# Default (read from data.txt)
python main.py

# Use proxy
python main.py --proxy 123.45.67.89:8080

# Disable deduplication (allow re-using data)
python main.py --no-dedup
```

---

## Proxy Configuration

### Option 1: Command line

```bash
python main.py --proxy YOUR_PROXY:PORT
```

### Option 2: Proxy file

Create `proxy.txt` with one proxy per line:

```
# Format: host:port or host:port:user:pass
123.45.67.89:8080
proxy.example.com:1080:username:password
```

The tool will automatically load proxies from `proxy.txt` if it exists.

---

## Deduplication

The tool tracks used data in `used.txt` to prevent re-verifying the same veteran.

- **Format:** `FIRSTNAME|LASTNAME|DOB` (one per line)
- **Auto-created:** After each verification attempt
- **Disable:** Use `--no-dedup` flag

---

## How It Works

1. Creates verification request via ChatGPT API
2. Submits military status (VETERAN) to SheerID
3. Submits personal info (name, DOB, branch, discharge date)
4. Waits for verification email
5. Extracts and submits email token
6. Verification complete!

---

## Output Example

```
=======================================================
  Veterans Verification Tool
  ChatGPT Plus - US Veterans Verification
=======================================================

[INFO] Loaded 2 records

[1/2] JOHN SMITH (Army)
   -> Creating verification request...
   [OK] Verification ID: abc123...
   -> Submitting military status (VETERAN)...
   [OK] Status submitted
   -> Submitting personal info...
   [OK] Personal info submitted - Step: emailLoop
   -> Waiting for verification email...
      Waiting... (1/20)
   -> Submitting email token: 12345...
   [SUCCESS]

-------------------------------------------------------
  Verification successful! Stopping...
-------------------------------------------------------
```

---

## Important Notes

- **Real data required**: SheerID verifies against US military database
- **One verification per identity**: Each veteran can only be verified once
- **Email required**: You need access to the email inbox for verification
- **accessToken expires**: Get a new one if you see authentication errors
- **Recent discharge**: Date should be within last 12 months

---

## Troubleshooting

| Error | Solution |
|-------|----------|
| `accessToken missing` | Get token from chatgpt.com/api/auth/session |
| `Email connection failed` | Check IMAP settings, use app password for Gmail |
| `Data already verified` | This veteran data was already used |
| `Document upload required` | Data couldn't be verified, needs manual upload |
| `Already used, skipping` | Data in `used.txt`, use `--no-dedup` to retry |

---

## Support

If you find this tool helpful, please consider supporting:

<a href="https://buymeacoffee.com/thanhnguyxn" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" height="50"></a>

[![GitHub Sponsors](https://img.shields.io/badge/Sponsor-GitHub-ea4aaa?logo=github)](https://github.com/sponsors/ThanhNguyxn)

## Disclaimer

This tool is for educational purposes only. Use at your own risk.

## License

MIT
