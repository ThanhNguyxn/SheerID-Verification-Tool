# Veterans Verification Tool

ChatGPT Plus verification tool for US Veterans using SheerID.

## Requirements

- Python 3.8+
- `requests` library
- `cloudscraper` library (recommended for Cloudflare bypass)

## Quick Start

### 1. Install dependencies

```bash
pip install requests cloudscraper
```

**[Optional] Enhanced Anti-Detection:**
```bash
pip install curl_cffi
```
> `curl_cffi` spoofs TLS fingerprint to look like real Chrome browser

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
| Outlook/Hotmail | outlook.office365.com | 993 |
| Yahoo | imap.mail.yahoo.com | 993 |
| iCloud | imap.mail.me.com | 993 |
| Zoho | imap.zoho.com | 993 |
| ProtonMail (Bridge) | 127.0.0.1 | 1143 |
| AOL | imap.aol.com | 993 |
| GMX | imap.gmx.com | 993 |
| Mail.com | imap.mail.com | 993 |
| Yandex | imap.yandex.com | 993 |
| FastMail | imap.fastmail.com | 993 |
| Tutanota | (No IMAP support) | - |
| Mailbox.org | imap.mailbox.org | 993 |
| Rambler | imap.rambler.ru | 993 |
| 163.com | imap.163.com | 993 |
| QQ Mail | imap.qq.com | 993 |
| Sina Mail | imap.sina.com | 993 |
| 126.com | imap.126.com | 993 |
| Naver | imap.naver.com | 993 |
| Daum | imap.daum.net | 993 |
| Comcast | imap.comcast.net | 993 |
| AT&T | imap.mail.att.net | 993 |
| Verizon | pop.verizon.net | 995 |
| Earthlink | imap.earthlink.net | 143 |
| Cox | imap.cox.net | 993 |
| Charter/Spectrum | mobile.charter.net | 993 |
| BellSouth | imap.mail.yahoo.com | 993 |
| Shaw.ca | imap.shaw.ca | 993 |
| Telus.net | imap.telus.net | 993 |
| Rogers.com | imap.mail.yahoo.com | 993 |
| Orange.fr | imap.orange.fr | 993 |
| Wanadoo.fr | imap.wanadoo.fr | 993 |
| Free.fr | imap.free.fr | 993 |
| SFR.fr | imap.sfr.fr | 993 |
| Laposte.net | imap.laposte.net | 993 |
| Web.de | imap.web.de | 993 |
| T-Online.de | secureimap.t-online.de | 993 |
| Freenet.de | mx.freenet.de | 993 |
| Mail.ru | imap.mail.ru | 993 |
| Libero.it | imapmail.libero.it | 993 |
| Virgilio.it | in.virgilio.it | 993 |
| Alice.it | in.alice.it | 993 |
| Tin.it | box.tin.it | 143 |
| Bol.com.br | imap.bol.com.br | 993 |
| Terra.com.br | imap.terra.com.br | 993 |
| UOL.com.br | imap.uol.com.br | 993 |
| IG.com.br | imap.ig.com.br | 993 |
| Rediffmail | imap.rediffmail.com | 993 |
| Indiatimes | imap.indiatimes.com | 993 |
| BigPond | imap.telstra.com | 993 |
| Optus | mail.optusnet.com.au | 993 |
| NetEase (163) | imap.163.com | 993 |
| NetEase (126) | imap.126.com | 993 |
| NetEase (yeah) | imap.yeah.net | 993 |
| Sohu | imap.sohu.com | 993 |
| 21cn | imap.21cn.com | 993 |
| Aliyun | imap.aliyun.com | 993 |

> **Note:** Most providers require "App Password" or "Less secure apps" enabled. Gmail specifically requires App Password with 2FA enabled.


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

Copy `proxy.example.txt` to `proxy.txt`:

```bash
cp proxy.example.txt proxy.txt
```

Edit `proxy.txt` with one proxy per line:

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

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `403 Forbidden` | accessToken expired | Get new token (see below) |
| `401 Unauthorized` | Invalid token | Check token format, get new one |
| `Not approved` | Data not in database OR IP blocked | Use proxy, try different data |
| `Document upload required` | Auto-verify failed | Data not in DoD/DEERS database |
| `Email connection failed` | IMAP settings wrong | Check server/port, use app password |
| `Data already verified` | Veteran already used | Try different data |
| `Already used, skipping` | Data in `used.txt` | Use `--no-dedup` flag |

---

### 🔴 403 Forbidden Error

**Most common issue!** Token expires after a few hours.

**Fix:**
1. Open https://chatgpt.com and login again
2. Go to https://chatgpt.com/api/auth/session
3. Copy the new `accessToken` value
4. Paste into `config.json`
5. Run again

---

### 🔴 "Not approved" from SheerID

**Two causes:**

1. **Data not in database**
   - SheerID checks against DoD/DEERS database
   - If veteran info not found → "Not approved"
   - Solution: Use verified real veteran data

2. **IP blocked/dirty**
   - Too many requests from same IP
   - Solution: Use proxy with `--proxy` flag
   ```bash
   python main.py --proxy 123.45.67.89:8080
   ```

---

### 🔴 Discharge Date Rules

SheerID has a **12-month rule** for ChatGPT Plus:
- Veteran must have separated within the **last 12 months**
- If discharge date is older → verification fails

**Solution:** Use a recent discharge date (e.g., current year)

---

### 🔴 Email Connection Failed

If you see `[ERROR] Email connection failed: b'LOGIN failed.'`, your email provider rejected the login.

**Common Causes:**
1. **2-Step Verification (2FA) is ON**: You cannot use your regular password. You MUST use an **App Password**.
2. **IMAP is OFF**: You must enable IMAP in your email settings.
3. **Less Secure Apps**: Some providers block third-party apps unless you allow them.

**How to fix (by provider):**

#### Gmail
1. Go to [Google Account Security](https://myaccount.google.com/security).
2. Enable **2-Step Verification**.
3. Go to **App Passwords** (search for it in the search bar).
4. Create new app password (Select "Mail" and "Windows Computer").
5. Use this 16-character password in `config.json`.

#### Outlook / Hotmail
1. Go to [Microsoft Account Security](https://account.live.com/proofs/manage/additional).
2. Enable **Two-step verification**.
3. Scroll down to **App passwords**.
4. Create a new app password and use it in `config.json`.

#### Yahoo Mail
1. Go to Account Security.
2. Generate a **Third-party app password**.
3. Use that password.

#### iCloud
1. Go to appleid.apple.com.
2. Generate an **App-Specific Password**.

> **Note:** If you still get errors, check if your firewall/antivirus is blocking the connection.

### 🛠 Debugging Tool

If you are unsure why the email connection is failing, run the included debug script:

```bash
python debug_email.py
```

This will test the connection to your email server and print detailed error messages to help you identify the problem (e.g., wrong password, blocked IP, SSL issues).


---

## Support

If you find this tool helpful, please consider supporting:

<a href="https://buymeacoffee.com/thanhnguyxn" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" height="50"></a>

[![GitHub Sponsors](https://img.shields.io/badge/Sponsor-GitHub-ea4aaa?logo=github)](https://github.com/sponsors/ThanhNguyxn)

## Disclaimer

This tool is for educational purposes only. Use at your own risk.

## License

MIT
