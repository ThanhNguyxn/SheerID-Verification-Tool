# Canva Education - UK Teacher Document Generator

Generate UK Teacher documents for Canva Education verification.

## ⚠️ Important Notes

- **Canva uses Goodstack** (not SheerID) for teacher verification
- **Requires 2 documents**: Teaching ID + Teaching licence
- Documents must show: **Full name + School name + Teaching position**
- Upload manually at [canva.com/education](https://canva.com/education)

## Verification Workflow

Based on [Issue #49](https://github.com/ThanhNguyxn/SheerID-Verification-Tool/issues/49) and [Issue #55](https://github.com/ThanhNguyxn/SheerID-Verification-Tool/issues/55):

| Step | Action |
|------|--------|
| 1 | Go to canva.com/education → Click "Get Verified" |
| 2 | Select Country: **United Kingdom** |
| 3 | Enter School email (or tick "I don't have a school email") |
| 4 | Enter School location (e.g. "London SW19 4TT") |
| 5 | Search and select School name (e.g. "King's College School") |
| 6 | **Upload Document 1**: Teaching ID |
| 7 | **Upload Document 2**: Teaching licence |
| 8 | Enter Full name (must match documents) |
| 9 | Wait 24-48h for Goodstack review |

## Documents This Tool Generates

| Document | Filename | Use As |
|----------|----------|--------|
| Employment Letter | `employment_letter_*.png` | Teaching licence |
| Teacher ID Card | `teacher_id_*.png` | Teaching ID |
| Teaching License | `teaching_license_*.png` | Teaching licence (alternative) |

## Requirements

```bash
pip install pymupdf pillow
```

## Usage

### Generate All Documents (Recommended)

```bash
python main.py
```

### Generate Specific Document

```bash
python main.py -d teacher_id          # For "Document 1: Teaching ID"
python main.py -d employment_letter   # For "Document 2: Teaching licence"
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

Documents saved to `./output/` folder as PNG files.

## Credits

- Templates: [cruzzzdev](https://github.com/cruzzzdev) (Issue #49)
- Workflow research: Issue #55
- Tool: [ThanhNguyxn](https://github.com/ThanhNguyxn)

## Disclaimer

⚠️ Educational purposes only. Using fake documents for fraud is illegal.
