# Canva Education - UK Teacher Document Generator

Generate UK Teacher documents for Canva Education verification.

> ⚠️ **Note**: Canva Education does NOT use SheerID. You must upload documents manually at [canva.com/education](https://canva.com/education).

## Features

- 📝 **Employment Letter** - UK school letterhead with teacher details
- 🪪 **Teacher ID Card** - School staff ID card
- 📜 **Teaching License** - DfE QTS certificate style document

## Requirements

```bash
pip install pymupdf pillow
```

## Usage

### Generate All Documents

```bash
python main.py
```

### Generate Specific Document Type

```bash
python main.py -d employment_letter
python main.py -d teacher_id
python main.py -d teaching_license
```

### Custom Teacher Details

```bash
python main.py --name "John Smith" --school "Eton College" --position "Head of Mathematics"
```

### List Available Schools

```bash
python main.py --list-schools
```

## Output

Documents are saved to the `./output/` folder as PNG files.

## How to Verify on Canva

1. Go to [canva.com/education](https://canva.com/education)
2. Click "Get Verified" or "I'm a Teacher"
3. Fill in your details
4. Upload one of the generated documents
5. Wait 24-48 hours for manual review

## Templates

Based on templates from [GitHub Issue #49](https://github.com/ThanhNguyxn/SheerID-Verification-Tool/issues/49):

- `Employment_Letter.pdf` - UK school employment confirmation
- `Teacher_ID_Card.pdf` - Staff ID card template  
- `Teaching_License.pdf` - DfE QTS certificate

## Credits

- Templates: [cruzzzdev](https://github.com/cruzzzdev)
- Tool: [ThanhNguyxn](https://github.com/ThanhNguyxn)

## Disclaimer

⚠️ This tool is for educational purposes only. Using fake documents for fraud is illegal.
