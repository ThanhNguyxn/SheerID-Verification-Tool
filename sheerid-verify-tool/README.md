# SheerID Verification Tool 🎓

Unified Python verification tool for all SheerID services.

## Features

✅ **All Services in One Tool**
- Spotify Premium (Student)
- YouTube Premium (Student)
- Google One / Gemini (Student)
- Bolt.new (Teacher)
- ChatGPT (Teacher)
- K12 (High School Teacher)

✅ **Smart Features**
- Success rate tracking per organization
- Weighted university selection (picks high success rate schools)
- Retry with exponential backoff
- Rate limiting avoidance
- Automatic document generation

## Requirements

```bash
pip install httpx Pillow
```

## Usage

### Command Line

```bash
# Spotify verification
python main.py spotify "https://services.sheerid.com/verify/...?verificationId=..."

# Bolt.new Teacher verification
python main.py boltnew "https://services.sheerid.com/verify/...?verificationId=..."

# K12 Teacher verification
python main.py k12 "https://services.sheerid.com/verify/...?verificationId=..."

# Show statistics
python main.py --stats

# List available services
python main.py --list
```

### Interactive Mode

```bash
python main.py
# Follow prompts to select service and enter URL
```

## Available Services

| Service | Type | Description |
|---------|------|-------------|
| `spotify` | Student | Spotify Premium Student discount |
| `youtube` | Student | YouTube Premium Student discount |
| `gemini` | Student | Google One AI Premium (Gemini) |
| `boltnew` | Teacher | Bolt.new Teacher discount |
| `gpt` | Teacher | ChatGPT Teacher discount |
| `k12` | K12 Teacher | High School Teacher verification |

## Statistics Tracking

The tool tracks success/failure rates per organization:

```
📊 Verification Statistics:
   Total: 15 | Success: 12 | Failed: 3
   Success Rate: 80.0%
   Top Organizations:
      - Pennsylvania State University-Main Campus: 90% (10 attempts)
      - University of California-Los Angeles: 75% (4 attempts)
```

See stats anytime with:
```bash
python main.py --stats
```

## How It Works

1. **Parse URL** - Extract verification ID
2. **Check State** - Verify link is valid
3. **Generate Info** - Name, email, DOB, document
4. **Submit Info** - Send to SheerID API
5. **Upload Document** - Upload fake ID/certificate
6. **Record Stats** - Track success/failure

## File Structure

```
sheerid-verify-tool/
├── main.py          # CLI interface
├── verifier.py      # Core verification logic
├── config.py        # Configuration & program IDs
├── utils.py         # Utilities (stats, retry, generators)
├── universities.py  # University data with weights
├── generators.py    # Document generators (PNG)
├── stats.json       # Statistics file (auto-created)
└── README.md
```

## Notes

- Documents are PNG images (student ID, teacher certificate, badge)
- Review usually takes 24-48 hours
- Program IDs may change - update `config.py` if needed
- Uses Pennsylvania State University (high success rate)

## License

MIT
