# 👨‍🏫 Bolt.new Teacher Verification Tool

Python tool for Bolt.new teacher discount via SheerID.

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
cd SheerID-Verification-Tool/boltnew-verify-tool
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

### Teacher Verification Flow

```
1. Parse verificationId from URL
2. Generate teacher identity:
   - Name (from name pool)
   - University email
   - DOB (25-55 years old - teachers are older)
3. Generate employment certificate (PNG)
4. Submit → collectTeacherPersonalInfo  ← Different from student!
5. Skip SSO → DELETE /step/sso
6. Upload document → S3
7. Complete → completeDocUpload
```

### Key Difference from Student Tools

| Aspect | Student | Teacher |
|--------|---------|---------|
| API Endpoint | `collectStudentPersonalInfo` | `collectTeacherPersonalInfo` |
| Age Range | 18-25 | 25-55 |
| Document | Student ID Card | Employment Certificate |

---

## 🧠 Intelligent Strategy: Teacher

This tool is specifically tuned for Teacher verification:

### 1. Teacher Demographics
-   **Age Targeting**: Generates identities aged **25-55** (unlike students who are 18-24).
-   **Employment Proof**: Generates "Employment Certificates" instead of Student IDs.

### 2. The "Waterfall" Flow
1.  **Submission**: Submits teacher PII (`collectTeacherPersonalInfo`).
2.  **SSO Bypass**: Skips school portal login (`DELETE /step/sso`).
3.  **Document Gen**: Creates realistic employment certificates.
4.  **Completion**: Finalizes upload via `completeDocUpload`.

### 3. Success Factors
-   **Valid Schools**: Uses a list of 12+ major universities known to have teacher programs.
-   **Document Clarity**: Certificates are generated with clear, legible text for OCR.

---

## 📝 Output Example

```
=========================================================
  Bolt.new Teacher Verification Tool
=========================================================

   Teacher: Mary Johnson
   Email: mjohnson456@psu.edu
   School: Pennsylvania State University-Main Campus
   Birth Date: 1985-03-12

   -> Step 1/4: Generating teacher document...
      Document size: 38.50 KB
   -> Step 2/4: Submitting teacher info...
      Current step: docUpload
   -> Step 3/4: Skipping SSO...
   -> Step 4/5: Requesting upload URL...
   -> Uploading document to S3...
   [OK] Document uploaded!
   -> Step 5/5: Completing upload...
      Upload completed: pending

---------------------------------------------------------
  [SUCCESS] Verification submitted!
```
