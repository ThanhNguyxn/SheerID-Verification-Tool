# 🤖 Google One (Gemini) Verification Tool

Python tool for Google One AI Premium student discount via SheerID.

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
cd SheerID-Verification-Tool/one-verify-tool
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

**With proxy (recommended to avoid fraud detection):**
```bash
python main.py "URL" --proxy 123.45.67.89:8080
python main.py "URL" --proxy http://user:pass@proxy.example.com:8080
```

---

## 🛡️ Avoiding Fraud Detection (`fraudRulesReject`)

If you encounter `fraudRulesReject` error, try:

| Solution | Description |
|----------|-------------|
| **Residential Proxy** | Use `--proxy` flag with residential IP (not datacenter) |
| **Wait Between Attempts** | 5-10 minutes between verifications |
| **Different University** | Tool uses weighted selection for higher success |
| **Fresh Verification Link** | Get a new link if previous one failed |

## ⚙️ How It Works

```
1. Parse verificationId
2. Check link state
3. Generate student identity
4. Generate student ID card
5. Submit → collectStudentPersonalInfo
6. Skip SSO → DELETE /step/sso
7. Upload document → S3
8. Complete → completeDocUpload
```

---

## 🎁 Benefits After Verification

Once verified, you get:

| Benefit | Description |
|---------|-------------|
| **Gemini Advanced** | Most powerful AI model |
| **2TB Google Drive** | Cloud storage |
| **NotebookLM Pro** | AI-powered notes |
| **AI Video Credits** | Veo video generation |

---

## 🧠 Intelligent Strategy: University Student

Optimized for Google One (Gemini Advanced) verification:

### 1. Weighted University Selection
-   **Database**: 45+ Universities (Global).
-   **Smart Weighting**: Selects high-success institutions.

### 2. The "Waterfall" Flow
1.  **Submission**: Submits PII.
2.  **SSO Bypass**: Skips school portal login (`DELETE /step/sso`).
3.  **Document Gen**: Creates realistic Student ID cards.
4.  **Completion**: Finalizes upload via `completeDocUpload`.

### 3. Success Factors
-   **Age Targeting**: 18-24 demographic.
-   **Clean Images**: Optimized for OCR.
