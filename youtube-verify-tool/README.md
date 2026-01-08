# 🎬 YouTube Student Verification Tool

Python tool for YouTube Premium student discount via SheerID.

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
cd SheerID-Verification-Tool/youtube-verify-tool
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

---

## ⚙️ How It Works

Same logic as Spotify tool:

```
1. Parse verificationId from URL
2. Check link validity
3. Generate student identity (name, email, DOB)
4. Generate student ID card (PNG)
5. Submit → collectStudentPersonalInfo
6. Skip SSO
7. Upload to S3
8. Complete upload
```

---

## 🧠 Intelligent Strategy: University Student

This tool shares the same advanced logic as the Spotify tool:

### 1. Weighted University Selection
-   **Database**: 45+ Universities (US, VN, JP, KR, etc.).
-   **Smart Weighting**: Prioritizes universities with "easier" verification thresholds.

### 2. The "Waterfall" Flow
1.  **Submission**: Submits PII.
2.  **SSO Bypass**: Skips school portal login (`DELETE /step/sso`).
3.  **Document Gen**: Creates realistic Student ID cards on-the-fly.
4.  **Completion**: Finalizes upload via `completeDocUpload`.

### 3. Success Factors
-   **Age Targeting**: 18-24 demographic.
-   **Clean Images**: Generated IDs are optimized for SheerID's OCR.

---

## 📝 Note

This tool uses the same codebase as Spotify tool, just with YouTube Premium branding.
