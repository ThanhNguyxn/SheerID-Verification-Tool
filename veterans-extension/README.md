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
JOHN|DOE|US ARMY|1985-01-15|2024-06-01
JANE|SMITH|US NAVY|1990-03-20|2024-08-15
```

---

## 🎖️ Supported Branches

| Branch | Alias |
|--------|-------|
| 🪖 Army | US ARMY |
| ✈️ Air Force | US AIR FORCE |
| ⚓ Navy | US NAVY |
| 🔱 Marine Corps | USMC, MARINES |
| ⛵ Coast Guard | USCG |
| 🚀 Space Force | USSF |

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
├── 🎨 popup.html       # UI
├── 📜 popup.js         # Popup logic
├── 🔧 content.js       # Auto-fill script
└── 📖 README.md
```

---

## ⚠️ Notes

> **📌 Important:**
> - Requires **real veteran data**
> - Date format: `YYYY-MM-DD`
> - Extension auto-disables after success
> - Index auto-increments per attempt

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
