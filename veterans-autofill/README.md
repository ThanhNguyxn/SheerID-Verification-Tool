# 🎖️ Veterans Autofill Extension

Auto-fill SheerID Veterans verification forms with tempmail support.

## ✨ Features

| Feature | Description |
|---------|-------------|
| 📧 **Auto Email** | Generate temp email (mail.tm) |
| 📝 **User Data** | Fill in your veteran info |
| 🔄 **Auto-Fill** | One-click form fill |
| 📬 **Get OTP** | Fetch verification code from email |
| 🛡️ **Anti-Detect** | Fingerprint spoofing for bypass |

---

## 📦 Installation

1. Clone or download this repository
2. Open `chrome://extensions/` (Chrome) or `edge://extensions/` (Edge)
3. Enable **Developer mode**
4. Click **Load unpacked**
5. Select the `veterans-autofill` folder

---

## 🛡️ Anti-Detection Features

The extension includes `fingerprint-spoofer.js` which:
- **Canvas Spoofing**: Adds noise to prevent canvas fingerprinting
- **WebGL Spoofing**: Randomizes GPU vendor/renderer info
- **Audio Spoofing**: Modifies AudioContext fingerprint
- **Navigator Spoofing**: Hides webdriver flag, randomizes hardware info
- **Screen Spoofing**: Randomizes screen resolution
- **Timezone Spoofing**: Randomizes to common US timezones

---

## 📚 How to Use

### Step 1: Generate Email
1. Click the extension icon
2. Click **Generate** to create a temp email

### Step 2: Fill Your Info
- **First Name** - Your first name
- **Last Name** - Your last name
- **Branch** - Military branch (Army, Navy, etc.)
- **Date of Birth** - Your birthdate
- **Discharge Date** - Must be within 12 months

### Step 3: Navigate to SheerID
Go to the Veterans verification page (e.g., ChatGPT veterans-claim)

### Step 4: Fill Form
Click **Fill Form** button - the extension will auto-fill all fields

### Step 5: Submit & Get OTP
1. Submit the form on SheerID
2. Wait for email to arrive
3. Click **Get OTP** or **Get Link**
4. Click **Open** to complete verification

---

## 📧 Supported Email Services

| Service | Domain | Notes |
|---------|--------|-------|
| **Mail.tm** | @mail.tm, @mail.gw | Best option, auto-token |
| **1secmail** | @1secmail.com | Backup option |

---

## 🎖️ Supported Branches

- 🪖 Army
- ✈️ Air Force
- ⚓ Navy
- 🔱 Marine Corps
- ⛵ Coast Guard
- 🚀 Space Force

---

## 📁 Files

```
veterans-autofill/
├── manifest.json          # Extension config
├── popup.html             # UI panel
├── popup.js               # Popup logic + email API
├── content.js             # Auto-fill logic
├── fingerprint-spoofer.js # Anti-fingerprint
├── icon*.png              # Icons
└── README.md
```

---

## ⚠️ Disclaimer

This tool is for **educational purposes only**.
- Real veteran data is required
- Use at your own risk

---

## 📜 License

MIT License
