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

---

## 📦 Installation

1. Download/clone this folder
2. Open extensions page:
   - **Chrome**: `chrome://extensions/`
   - **Edge**: `edge://extensions/`
3. Enable **Developer mode** ✅
4. Click **Load unpacked**
5. Select `veterans-extension` folder

---

## 📋 Data Format

```
FirstName|LastName|Branch|DOB|DischargeDate
```

**Example:**
```
JOHN|DOE|Army|1985-01-15|2025-06-01
JANE|SMITH|Navy|1990-03-20|2025-08-15
```

> **Note:** Discharge date should be within last 12 months.

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

---

## 📊 Statistics Panel

The extension now tracks verification results:

| Stat | Description |
|------|-------------|
| ✅ Success | Verification passed |
| ❌ Failed | Error detected, auto-retry |
| ⏭️ Skipped | Data skipped |

Statistics are saved and persist across sessions.

---

## 📤 Export / Import

### Export
1. Click **📤 Export** button
2. Save the `.json` file

### Import
1. Click **📥 Import** button
2. Select your backup `.json` file
3. Config restored!

---

## 🔄 Workflow

```
📍 chatgpt.com/veterans-claim
           ↓
🔑 Extract accessToken
           ↓
📡 Call create_verification API
           ↓
🔗 Redirect to SheerID
           ↓
📝 Auto-fill form & submit
           ↓
✅ Success → Disable | ❌ Error → Retry
```

---

## 📁 Files

```
veterans-extension/
├── ⚙️ manifest.json    # Extension config
├── 🎨 popup.html       # UI with stats panel
├── 📜 popup.js         # Popup logic + export/import
├── 🔧 content.js       # Auto-fill + error detection
└── 📖 README.md
```

---

## ⚠️ Important Notes

> **📌 Requirements:**
> - Must be logged in to ChatGPT
> - Real veteran data required
> - Date format: `YYYY-MM-DD`
> - Discharge date within last 12 months

> **📌 Behavior:**
> - Extension auto-disables after success
> - Index auto-increments per attempt
> - Errors trigger auto-retry with new link

---

## 🔍 Error Detection

The extension detects 14 error patterns:

| Error Type | Action |
|------------|--------|
| `verification limit exceeded` | Retry with new data |
| `unable to verify` | Retry |
| `information does not match` | Retry |
| `already been used` | Skip, next data |
| `not approved` | Retry |

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

## 📜 License

MIT License

<p align="center">
  Made with ❤️ by <a href="https://github.com/ThanhNguyxn">ThanhNguyxn</a>
</p>
