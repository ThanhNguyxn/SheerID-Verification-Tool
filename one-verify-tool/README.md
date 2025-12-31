# Google One (Gemini) Student Verification Tool

SheerID Student verification for Google One AI Premium (Gemini).

## Requirements

```bash
pip install httpx Pillow
```

## Usage

```bash
python main.py "https://services.sheerid.com/verify/PROGRAM_ID/?verificationId=YOUR_ID"
```

## How It Works

1. Generates fake student info (name, email, DOB)
2. Creates fake student ID card PNG
3. Submits via `collectStudentPersonalInfo`
4. Uploads document to SheerID S3

## Note

- Uses PSU (Pennsylvania State University) as fake school
- Student age: 18-25 years old
- Review usually takes 24-48 hours
- After approval, claim Google One AI Premium trial

## License

MIT
