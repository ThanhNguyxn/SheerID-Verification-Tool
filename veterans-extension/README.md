# 🎖️ Veterans Extension

<p align="center">
  <img src="https://img.shields.io/badge/Chrome-Extension-4285F4?style=for-the-badge&logo=googlechrome&logoColor=white" alt="Chrome">
  <img src="https://img.shields.io/badge/Edge-Supported-0078D7?style=for-the-badge&logo=microsoftedge&logoColor=white" alt="Edge">
  <img src="https://img.shields.io/badge/Veterans-ChatGPT-10A37F?style=for-the-badge&logo=openai&logoColor=white" alt="Veterans">
</p>

<p align="center">
  <b>🎖️ Auto-fill SheerID Veterans verification for ChatGPT Plus</b>
</p>

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🔄 **Auto Redirect** | veterans-claim → SheerID |
| 📝 **Batch Fill** | Multiple veteran data support |
| 🔁 **Auto Retry** | Detect errors, get new link |
| ✅ **Success Detection** | Auto-disable on success |
| 📊 **Statistics** | Track Success / Failed / Skipped |
| 📤 **Export/Import** | Backup and restore config |
| 💾 **Persistence** | Save config & track entries |
| 📧 **TempMail Support** | Auto-verify with 1secmail, Mail.tm |

---

## 📦 Installation

### Step 1: Download Extension

```bash
git clone https://github.com/ThanhNguyxn/SheerID-Verification-Tool.git
cd SheerID-Verification-Tool/veterans-extension
```

Or download ZIP and extract.

### Step 2: Load in Browser

**Chrome:**
1. Open `chrome://extensions/`
2. Enable **Developer mode** (toggle in top-right corner)
3. Click **Load unpacked**
4. Select the `veterans-extension` folder

**Edge:**
1. Open `edge://extensions/`
2. Enable **Developer mode** (toggle in left sidebar)
3. Click **Load unpacked**
4. Select the `veterans-extension` folder

---

## 📚 How to Use (Step-by-Step)

### Step 1: Login to ChatGPT

1. Go to https://chatgpt.com
2. Login with your account

### Step 2: Add Veteran Data

1. Click the extension icon in your browser toolbar
2. In the **Data** text box, enter veteran info:

```
JOHN|DOE|Army|1985-01-15|2025-06-01
JANE|SMITH|Navy|1990-03-20|2025-08-15
```

**Format:** `FirstName|LastName|Branch|DOB|DischargeDate`

> ⚠️ **Important:** 
> - Date format: `YYYY-MM-DD`
> - Discharge date must be within last **12 months**
> - One entry per line

### Step 3: Enable Extension

1. Toggle **Enable** switch to ON
2. The extension is now active

### Step 4: Start Verification

1. Go to https://chatgpt.com/veterans-claim
2. The extension will automatically:
   - Extract your accessToken
   - Create verification request
   - Redirect to SheerID
   - Auto-fill the form
   - Submit and handle results

### Step 5: Monitor Results

- Check the **Statistics** panel in the popup
- ✅ Success = Verification passed
- ❌ Failed = Error, will auto-retry
- ⏭️ Skipped = Data was skipped

---

## 📧 TempMail Auto-Verify

The extension can automatically check TempMail inboxes for verification emails and submit the token.

### Supported TempMail Services

| Service | Domains |
|---------|---------|
| **1secmail** | 1secmail.com, 1secmail.org, 1secmail.net, wwjmp.com, esiix.com |
| **Mail.tm** | mail.tm, mail.gw |

### How It Works

1. Enter a TempMail email address in the Email field (e.g., `myname@1secmail.com`)
2. The extension will auto-detect the TempMail service
3. After form submission, it polls the TempMail API for verification email
4. When found, it extracts the token and auto-submits

> **Note:** For Mail.tm, you may need to create the account first on mail.tm website.

---

## 🎖️ Supported Branches

| Branch | Aliases |
|--------|---------|
| 🪖 Army | US ARMY |
| ✈️ Air Force | US AIR FORCE |
| ⚓ Navy | US NAVY |
| 🔱 Marine Corps | USMC, MARINES |
| ⛵ Coast Guard | USCG |
| 🚀 Space Force | USSF |
| 🛡️ Army National Guard | ARNG |
| 🛡️ Army Reserve | USAR |
| 🛡️ Air National Guard | ANG |
| 🛡️ Air Force Reserve | AFR |
| 🛡️ Navy Reserve | NR |
| 🛡️ Marine Corps Reserve | MCR |
| 🛡️ Coast Guard Reserve | CGR |

---

## 📚 Workflow Diagram

```
📍 You visit: chatgpt.com/veterans-claim
            ↓
🔑 Extension extracts accessToken from page
            ↓
📡 Calls: POST /backend-api/veterans/create_verification
            ↓
🔗 Gets verification_id, redirects to SheerID
            ↓
📝 Auto-fills form with your veteran data
            ↓
✅ Success → Extension disables, shows stats
❌ Error → Increments index, retries with next data
```

---

## 📤 Export / Import Config

### Export (Backup)
1. Click **📤 Export** button
2. Save the `.json` file

### Import (Restore)
1. Click **📥 Import** button
2. Select your backup `.json` file
3. Config and data restored!

---

## 🔍 Error Detection

The extension automatically detects and handles these errors:

| Error Pattern | Action |
|---------------|--------|
| `verification limit exceeded` | Retry with new data |
| `unable to verify` | Retry |
| `information does not match` | Retry |
| `already been used` | Skip, use next data |
| `not approved` | Retry |
| `fraudRulesReject` | Retry with different data |
| `We couldn't verify` | Retry |
| `ineligible` | Retry |

---

## ⚠️ Troubleshooting

### Extension not working?

1. **Check if logged in**: Go to https://chatgpt.com and make sure you're logged in
2. **Check Developer mode**: Make sure Developer mode is ON in browser extensions
3. **Reload extension**: Click the refresh button on the extension card
4. **Check console**: Press F12 → Console tab to see error messages

### 403 Forbidden Error?

This means Cloudflare is blocking the request. Try:
1. Clear cookies and login again to ChatGPT
2. Use a different browser/incognito
3. Try with a VPN/proxy

### "Not approved" errors?

This means SheerID couldn't verify the data. Possible causes:
- Data not in DoD/DEERS database
- Discharge date too old (must be within 12 months)
- Name/DOB doesn't match records

---

## 📁 Files

```
veterans-extension/
├── ⚙️ manifest.json    # Extension config (permissions, content scripts)
├── 🎨 popup.html       # UI with data input & stats panel
├── 📜 popup.js         # Popup logic, export/import, storage
├── 🔧 content.js       # Auto-fill logic, error detection, API calls
├── 🖼️ icon*.png        # Extension icons
└── 📖 README.md
```

---

## 💖 Support

<p align="center">
  <a href="https://buymeacoffee.com/thanhnguyxn">
    <img src="https://img.shields.io/badge/Buy%20Me%20A%20Coffee-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black" alt="Buy Me A Coffee">
  </a>
  <a href="https://github.com/sponsors/ThanhNguyxn">
    <img src="https://img.shields.io/badge/GitHub%20Sponsors-EA4AAA?style=for-the-badge&logo=github-sponsors&logoColor=white" alt="GitHub Sponsors">
  </a>
</p>

---

## 📜 Disclaimer

This tool is for **educational purposes only**. 
- Real veteran data is required (SheerID verifies against DoD database)
- Use at your own risk
- One verification per identity

---

## 📜 License

MIT License

<p align="center">
  Made with ❤️ by <a href="https://github.com/ThanhNguyxn">ThanhNguyxn</a>
</p>
