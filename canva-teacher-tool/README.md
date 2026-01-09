# Canva Education Teacher Verification Tool

Bypass Canva Education verification for UK Teachers using generated documents.

## Features

- 📝 **Employment Letter** - UK school letterhead with teacher details
- 🪪 **Teacher ID Card** - School staff ID card with photo placeholder
- 📜 **Teaching License** - DfE QTS certificate style document

## Requirements

```bash
pip install httpx pymupdf pillow
```

## Usage

### Basic Usage

```bash
python main.py "https://services.sheerid.com/verify/...?verificationId=..."
```

### With Document Type

```bash
# Employment letter (default, recommended)
python main.py URL --doc-type employment_letter

# Teacher ID card
python main.py URL --doc-type teacher_id

# Teaching license
python main.py URL --doc-type teaching_license
```

### Test Mode

Generate a test document without verification:

```bash
python main.py --test-doc -d employment_letter
```

## How to Get the URL

1. Go to [Canva Education](https://www.canva.com/education)
2. Start the teacher verification process
3. Open Developer Tools (F12) → Network tab
4. Filter by `sheerid`
5. Find the request containing `verificationId=`
6. Copy the full URL

## Document Templates

Templates from [GitHub Issue #49](https://github.com/ThanhNguyxn/SheerID-Verification-Tool/issues/49):

- `Employment_Letter.pdf` - UK school employment confirmation
- `Teacher_ID_Card.pdf` - Staff ID card template
- `Teaching_License.pdf` - DfE QTS certificate

## UK Schools Database

Uses a curated list of UK schools. To add more schools, edit `data/uk_schools.json`:

```json
[
  {
    "name": "School Name",
    "address": "Street Address",
    "town": "City",
    "postcode": "XX00 0XX",
    "phone": "0000 000 0000",
    "lea": "Local Education Authority"
  }
]
```

## Credits

- Templates: [cruzzzdev](https://github.com/cruzzzdev)
- Tool: [ThanhNguyxn](https://github.com/ThanhNguyxn)

## Disclaimer

⚠️ This tool is for educational and research purposes only. Using fake documents for fraud is illegal.
