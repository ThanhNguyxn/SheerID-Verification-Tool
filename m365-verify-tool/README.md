# 🎓 MS365 Education Verification Tool

> ⚠️ **WORK IN PROGRESS** - This tool is under development and NOT fully tested yet!
> Use at your own risk. Contributions welcome.

Python tool to automate Microsoft 365 Education student verification using Playwright browser automation.

## 📋 Requirements

- Python 3.8+
- Playwright (browser automation)
- httpx (HTTP client)
- Pillow (optional, for document generation)
- playwright-stealth (optional, for better anti-detection)

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install playwright httpx Pillow playwright-stealth
playwright install chromium
```

### 2. Run Tool

**Interactive Mode** (recommended for first use):
```bash
cd m365-verify-tool
python main.py
```

**Direct Mode** (with email):
```bash
python main.py --email yourname@university.edu
```

**Export Tokens Mode**:
```bash
python main.py --export-tokens
```

## ⚙️ How It Works

```
1. Launch Chromium browser via Playwright
2. Navigate to MS365 Student Checkout page
3. User signs in to Microsoft account
4. Script captures authentication tokens (Authorization, X-Auth)
5. Tokens used to call MS365 verification API
6. Verification email sent to student email
7. (Optional) SheerID document upload fallback
```

## 🔧 Usage Modes

| Mode | Command | Description |
|------|---------|-------------|
| Interactive | `python main.py` | Opens browser, guides through process |
| Direct | `python main.py --email user@edu` | Automatic verification with given email |
| Headless | `python main.py --email user@edu --headless` | No visible browser |
| Token Export | `python main.py --export-tokens` | Save tokens to `tokens.json` |

## 📁 Files

| File | Description |
|------|-------------|
| `main.py` | Main verification script |
| `tokens.json` | Exported tokens (generated) |

## ⚠️ Important Notes

1. **Microsoft Account Required**: You need a valid Microsoft account
2. **Student Email**: Must be a valid `.edu` or institutional email
3. **Manual Sign-in**: First run requires manual sign-in
4. **Token Expiry**: Captured tokens expire after ~1 hour

## 🛡️ Anti-Detection Features

- **playwright-stealth**: Removes automation markers (webdriver, plugins, etc.)
- Realistic browser fingerprint (Chrome 131)
- Proper viewport, user-agent, and timezone
- Human-like timing delays
- Native Chromium (not detected as automation)
- Additional Chrome args to disable automation signals

## 🔗 Related Tools

- [one-verify-tool](../one-verify-tool/) - Google One/Gemini verification
- [spotify-verify-tool](../spotify-verify-tool/) - Spotify Premium verification

## 📄 License

MIT License - See [LICENSE](../LICENSE)
