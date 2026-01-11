# 🎵 Spotify Student Verification Tool

Python tool for Spotify Premium student discount via SheerID.

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
cd SheerID-Verification-Tool/spotify-verify-tool
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

**With URL argument:**
```bash
python main.py "https://services.sheerid.com/verify/xxx?verificationId=abc123"
```

**With proxy (recommended to avoid fraud detection):**
```bash
python main.py "URL" --proxy 123.45.67.89:8080
python main.py "URL" --proxy http://user:pass@proxy.example.com:8080
```

**Interactive mode:**
```bash
python main.py
# Enter your SheerID URL when prompted
```

---

## 🛡️ Avoiding Fraud Detection (`fraudRulesReject`)

If you encounter `fraudRulesReject` error, try these solutions:

### 1. Use Residential Proxy
```bash
python main.py "URL" --proxy residential-proxy.com:8080
```
- **Datacenter IPs** are more likely to be blocked
- **Residential proxies** have higher success rate

### 2. Wait Between Attempts
- Don't run too many verifications in a row
- Wait at least 5-10 minutes between attempts

### 3. Try Different Universities
- Some universities have higher success rates
- The tool uses weighted selection based on historical success

---

## ⚙️ How It Works

### Verification Flow

```
1. Parse URL → Extract verificationId
2. Check link state → Ensure link is valid
3. Generate student identity:
   - Random name (from 60 first + 55 last names)
   - University email (from 45 universities)
   - Birthday (18-25 years old)
4. Generate student ID card (PNG)
5. Submit to SheerID → collectStudentPersonalInfo
6. Skip SSO → DELETE /step/sso
7. Upload document → docUpload + S3
8. Complete → completeDocUpload
```

### API Endpoints Used

| Step | Method | Endpoint |
|------|--------|----------|
| Check | GET | `/verification/{id}` |
| Submit | POST | `/step/collectStudentPersonalInfo` |
| Skip SSO | DELETE | `/step/sso` |
| Upload | POST | `/step/docUpload` |
| Complete | POST | `/step/completeDocUpload` |

---

## 🧠 Intelligent Strategy: University Student

This tool uses a sophisticated "Waterfall" verification logic designed for high success rates:

### 1. Weighted University Selection
-   **Database**: Uses a curated list of **45+ Universities** across US, VN, JP, KR, CN, DE, FR, SG, AU, BR.
-   **Smart Weighting**: Universities with historically higher success rates (e.g., specific US state colleges or international schools) are selected more frequently.
-   **Dynamic Data**: Generates student data (Name, DOB, Email) that matches the specific format required by each university.

### 2. The "Waterfall" Flow
1.  **Submission**: Submits student PII to SheerID.
2.  **SSO Bypass**: Automatically sends `DELETE /step/sso` to skip the school login requirement.
3.  **Document Generation**: If instant verification fails, generates a **high-quality Student ID card** with:
    -   University Logo & Name
    -   Student Name & Photo
    -   Valid Expiration Date (Current Academic Year)
4.  **Completion**: Uploads the document and triggers `completeDocUpload`.

### 3. Success Factors
-   **Age Targeting**: Targets 18-24 year old demographic.
-   **Metadata Stripping**: Cleans image metadata to pass OCR checks.
-   **Auto-Retry**: Implements exponential backoff for network issues.

---

## 📝 Output Example

```
╔════════════════════════════════════════════════════════╗
║  🎵 Spotify Student Verification Tool                  ║
╚════════════════════════════════════════════════════════╝

   🎓 Student: John Smith
   📧 Email: jsmith123@psu.edu
   🏫 School: Pennsylvania State University-Main Campus
   🎂 DOB: 2002-05-15

   ▶ Step 1/5: Generating student ID...
     📄 Size: 45.2 KB
   ▶ Step 2/5: Submitting student info...
     📍 Current step: docUpload
   ▶ Step 3/4: Skipping SSO...
   ▶ Step 4/5: Uploading document...
     ✅ Document uploaded!
   ▶ Step 5/5: Completing upload...
     ✅ Upload completed: pending

   ════════════════════════════════════════════════════════
   ✅ SUCCESS! Wait 24-48h for review.
```
