# 🏫 K12 Teacher Verification Tool

Python tool for ChatGPT Plus K12 teacher discount via SheerID.

---

## 📋 Requirements

- Python 3.8+
- `httpx` - HTTP client
- `Pillow` - Image generation

---

## 🚀 Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/ThanhNguyxn/SheerID-Verification-Tool.git
```

### 2. Go to Tool Directory

```bash
cd SheerID-Verification-Tool/k12-verify-tool
```

### 3. Install Dependencies

```bash
pip install httpx Pillow
```

**[Optional] Enhanced Anti-Detection:**
```bash
pip install curl_cffi cloudscraper
```
> `curl_cffi` spoofs TLS fingerprint to look like real Chrome browser

### 4. Run Tool

```bash
python main.py "https://services.sheerid.com/verify/xxx?verificationId=abc123"
```

### 5. Run with Proxy (Optional)

```bash
python main.py --proxy "http://user:pass@host:port"
```

---

## 🛠 CLI Options

| Option | Description |
|--------|-------------|
| `url` | Verification URL (optional, can be pasted interactively) |
| `--proxy` | HTTP/HTTPS proxy URL (e.g., `http://user:pass@host:port`) |

---

## 🧠 Intelligent Strategy: K12 Teacher

This tool leverages specific loopholes in K12 verification:

### 1. School Type Targeting
-   **Logic**: Targets schools with `type: "K12"` instead of `"HIGH_SCHOOL"`.
-   **Result**: High probability of **auto-approval** without document upload.

### 2. The "Waterfall" Flow
1.  **Submission**: Submits teacher PII (`collectTeacherPersonalInfo`).
2.  **Auto-Pass Check**: Checks if `currentStep` is `success` immediately.
3.  **SSO Bypass**: Skips school portal login (`DELETE /step/sso`).
4.  **Auto-Pass Check 2**: Checks again for success.
5.  **Fallback**: If upload needed, generates a Teacher Badge.

### 3. Success Factors
-   **Real Info**: Uses real teacher names found on school websites.
-   **IP Address**: Residential/Edu IPs work best.

---

## 📊 K12 Schools Database

| Category | Examples |
|----------|----------|
| **NYC Specialized** | Stuyvesant, Bronx Science, Brooklyn Tech |
| **Chicago Selective** | Payton Prep, Whitney Young, Northside |
| **Virginia/DC STEM** | Thomas Jefferson, McKinley Tech |
| **California Elite** | Whitney, Lowell, Palo Alto |
| **BASIS Charter** | Scottsdale, Tucson North, Mesa |
| **KIPP Network** | KIPP DC, KIPP SoCal |

---

## ⚠️ Important Notes

- **School type verification**: Use SheerID org search API to confirm school type is "K12"
- **If upload required**: Try pure white image 3 times, system may auto-approve
- **Real teacher names work better**: Search school websites for staff directories

---

## 📖 Reference

Based on research from: https://www.azx.us/posts/638
