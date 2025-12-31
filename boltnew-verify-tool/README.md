# Bolt.new Teacher Verification Tool

SheerID Teacher verification tool for Bolt.new.

## Requirements

- Python 3.8+
- httpx
- Pillow

## Quick Start

### 1. Install dependencies

```bash
pip install httpx Pillow
```

### 2. Run

```bash
python main.py "https://services.sheerid.com/verify/PROGRAM_ID/?verificationId=YOUR_ID"
```

Or run interactively:

```bash
python main.py
# Then paste your verification URL
```

## How It Works

1. Parses verification URL to extract `verificationId`
2. Generates fake teacher info (name, email, DOB)
3. Creates fake teacher certificate PNG
4. Submits teacher info via `collectTeacherPersonalInfo`
5. Skips SSO verification
6. Uploads document to SheerID S3
7. Waits for manual review

## Output Example

```
=======================================================
  Bolt.new Teacher Verification Tool
  SheerID Teacher Verification
=======================================================

[INFO] Processing URL...
   Teacher: John Smith
   Email: jsmith123@psu.edu
   School: Pennsylvania State University-Main Campus
   Birth Date: 1985-03-15
   Verification ID: abc123...

   -> Step 1/4: Generating teacher document...
      Document size: 12.34 KB
   -> Step 2/4: Submitting teacher info...
      Current step: docUpload
   -> Step 3/4: Skipping SSO...
   -> Step 4/4: Requesting upload URL...
   -> Uploading document to S3...
   [OK] Document uploaded successfully!

-------------------------------------------------------
  [SUCCESS] Verification submitted!
  Teacher: John Smith
  Email: jsmith123@psu.edu
-------------------------------------------------------
```

## Note

- Uses Pennsylvania State University (PSU) as fake school
- Generates fake teacher employment certificate
- Verification requires manual review (usually 24-48 hours)
- Program ID may need updating if expired

## License

MIT
