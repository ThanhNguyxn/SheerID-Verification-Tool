# K12 Teacher Verification Tool

SheerID K12 Teacher verification for High School teachers.

## Requirements

```bash
pip install httpx Pillow
```

## Usage

```bash
python main.py "https://services.sheerid.com/verify/PROGRAM_ID/?verificationId=YOUR_ID"
```

## How It Works

1. Generates fake K12 teacher info (name, email, DOB)
2. Creates fake teacher badge PNG (school ID style)
3. Submits via `collectTeacherPersonalInfo`
4. Skips SSO verification
5. Uploads document to SheerID S3

## Schools Used

Uses Springfield High School (multiple locations):
- Springfield, OR
- Springfield, OH
- Springfield, IL
- Springfield, PA

## Note

- This is for **High School (K-12) teachers**, not University
- Teacher age: 25-55 years old
- Uses generic email domains (gmail, yahoo, etc.)
- Review usually takes 24-48 hours

## Difference from Boltnew

| Feature | Boltnew | K12 |
|---------|---------|-----|
| School Type | University | High School |
| Email | @psu.edu | @gmail.com |
| Document | Employment certificate | Staff badge |
| Program ID | Different | Different |

## License

MIT
