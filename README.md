# 🔐 SheerID Verification Tool

[![GitHub Stars](https://img.shields.io/github/stars/ThanhNguyxn/SheerID-Verification-Tool?style=social)](https://github.com/ThanhNguyxn/SheerID-Verification-Tool/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Documentation](https://img.shields.io/badge/Docs-Website-2ea44f?style=flat&logo=github&logoColor=white)](https://thanhnguyxn.github.io/SheerID-Verification-Tool/)

A comprehensive collection of tools for automating SheerID verification workflows for various services (Spotify, YouTube, Google One, etc.).

---

## 🛠️ Available Tools

| Tool | Type | Target | Description |
|------|------|--------|-------------|
| [spotify-verify-tool](./spotify-verify-tool/) | 🎵 Student | Spotify Premium | University student verification |
| [youtube-verify-tool](./youtube-verify-tool/) | 🎬 Student | YouTube Premium | University student verification |
| [one-verify-tool](./one-verify-tool/) | 🤖 Student | Gemini Advanced | Google One AI Premium verification |
| [boltnew-verify-tool](./boltnew-verify-tool/) | 👨‍🏫 Teacher | Bolt.new | Teacher verification (University) |
| [k12-verify-tool](./k12-verify-tool/) | 🏫 K12 | ChatGPT Plus | K12 Teacher verification (High School) |
| [veterans-verify-tool](./veterans-verify-tool/) | 🎖️ Military | General | Military status verification |
| [veterans-extension](./veterans-extension/) | 🧩 Chrome | Browser | Chrome extension for military verification |

### 🔗 External Tools

| Tool | Type | Description |
|------|------|-------------|
| [SheerID VIP Bot](https://t.me/SheerID_VIP_Bot?start=ref_REF001124) | ⚡ Bot | Alternative Telegram bot with faster processing |
| [SheerID VN Bot](https://t.me/sheeridvn_bot?start=invite_7762497789) | 🇻🇳 Bot | Vietnamese community Telegram bot |
| [Veterans Verify Bot](https://t.me/vgptplusbot?start=ref_7762497789) | 🎖️ Bot | Military verification bot |
| [Batch 1Key.me](https://batch.1key.me/) | 📦 Web | Batch verification for multiple URLs |
| [Student Card Generator](https://thanhnguyxn.github.io/student-card-generator/) | 🎓 Tool | Create student cards for manual verification |
| [Payslip Generator](https://thanhnguyxn.github.io/payslip-generator/) | 💰 Tool | Generate payslips for teacher verification |
| [RoxyBrowser](https://roxybrowser.com?code=01045PFA) | 🦊 Browser | **Anti-detect browser** — Safely manage multiple verified accounts without getting banned |

---

## 🧠 Core Architecture & Logic

All Python tools in this repository share a common, optimized architecture designed for high success rates.

### 1. The Verification Flow
The tools follow a standardized "Waterfall" process:
1.  **Data Generation**: Creates a realistic identity (Name, DOB, Email) matching the target demographic.
2.  **Submission (`collectStudentPersonalInfo`)**: Submits data to SheerID API.
3.  **SSO Skip (`DELETE /step/sso`)**: Crucial step. Bypasses the requirement to log in to a school portal.
4.  **Document Upload (`docUpload`)**: Uploads a generated proof document (Student ID, Transcript, or Teacher Badge).
5.  **Completion (`completeDocUpload`)**: Signals to SheerID that upload is finished.

### 2. Intelligent Strategies

#### 🎓 University Strategy (Spotify, YouTube, Gemini)
- **Weighted Selection**: Uses a curated list of **45+ Universities** (US, VN, JP, KR, etc.).
- **Success Tracking**: Universities with higher success rates are selected more often.
- **Document Gen**: Generates realistic-looking Student ID cards with dynamic names and dates.

#### 👨‍🏫 Teacher Strategy (Bolt.new)
- **Age Targeting**: Generates older identities (25-55 years old) to match teacher demographics.
- **Document Gen**: Creates "Employment Certificates" instead of Student IDs.
- **Endpoint**: Targets `collectTeacherPersonalInfo` instead of student endpoints.

#### 🏫 K12 Strategy (ChatGPT Plus)
- **School Type Targeting**: Specifically targets schools with `type: "K12"` (not `HIGH_SCHOOL`).
- **Auto-Pass Logic**: K12 verification often **auto-approves** without document upload if the school and teacher info match.
- **Fallback**: If upload is required, it generates a Teacher Badge.

#### 🎖️ Veterans Strategy (ChatGPT Plus)
- **Strict Eligibility**: Targets Active Duty or Veterans separated within the **last 12 months**.
- **Authoritative Check**: SheerID verifies against DoD/DEERS database.
- **Logic**: Defaults to recent discharge dates to maximize auto-approval chances.

---

## 📋 Quick Start

### Prerequisites
- Python 3.8+
- `pip`

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/ThanhNguyxn/SheerID-Verification-Tool.git
    cd SheerID-Verification-Tool
    ```

2.  **Install dependencies:**
    ```bash
    pip install httpx Pillow
    ```

3.  **Run a tool (e.g., Spotify):**
    ```bash
    cd spotify-verify-tool
    python main.py "YOUR_SHEERID_URL"
    ```

---

## 🦊 Official Partner: RoxyBrowser

🛡 **Anti-Detect Protection** — Unique fingerprint for each account, looks like different real devices.

📉 **Prevent Linkage** — Stops SheerID and platforms from linking your accounts.

🚀 **Ideal for Bulk Users** — Safely manage hundreds of verified accounts.

[![Try for free](https://img.shields.io/badge/Try%20for%20free-RoxyBrowser-ff6b35?style=for-the-badge&logo=googlechrome&logoColor=white)](https://roxybrowser.com?code=01045PFA)

---

## ⚠️ Disclaimer

This project is for **educational purposes only**. The tools demonstrate how verification systems work and how they can be tested.
- Do not use this for fraudulent purposes.
- The authors are not responsible for any misuse.
- Respect the Terms of Service of all platforms.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## ❤️ Support

If you find this project helpful, consider supporting me:

[![GitHub Sponsors](https://img.shields.io/badge/Sponsor-GitHub-ea4aaa?style=for-the-badge&logo=github)](https://github.com/sponsors/ThanhNguyxn)
[![Buy Me a Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://buymeacoffee.com/thanhnguyxn)

---

## 🌐 Translations

| 🇺🇸 [English](./README.md) | 🇻🇳 [Tiếng Việt](./docs/README.vi.md) | 🇨🇳 [中文](./docs/README.zh.md) | 🇯🇵 [日本語](./docs/README.ja.md) | 🇰🇷 [한국어](./docs/README.ko.md) |
|:---:|:---:|:---:|:---:|:---:|
| 🇪🇸 [Español](./docs/README.es.md) | 🇫🇷 [Français](./docs/README.fr.md) | 🇩🇪 [Deutsch](./docs/README.de.md) | 🇧🇷 [Português](./docs/README.pt-BR.md) | 🇷🇺 [Русский](./docs/README.ru.md) |
| 🇸🇦 [العربية](./docs/README.ar.md) | 🇮🇳 [हिन्दी](./docs/README.hi.md) | 🇹🇭 [ไทย](./docs/README.th.md) | 🇹🇷 [Türkçe](./docs/README.tr.md) | 🇵🇱 [Polski](./docs/README.pl.md) |
| 🇮🇹 [Italiano](./docs/README.it.md) | 🇮🇩 [Bahasa Indonesia](./docs/README.id.md) | | | |
