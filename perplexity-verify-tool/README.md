# Perplexity AI Verification Tool

Automated SheerID verification for Perplexity Pro student discount.

## Features

- **Automated Verification**: Generates student info, documents, and handles the verification flow.
- **Smart University Selection**: Picks universities with high success rates.
- **Cloudflare Bypass**: Uses `cloudscraper` (if installed) or standard requests.
- **Success Tracking**: Logs success rates per university to `stats.json`.

## Requirements

- Python 3.8+
- `httpx`
- `Pillow` (for document generation)

## Installation

```bash
pip install httpx Pillow
```

## Usage

1. **Get the Verification URL**:
   - Go to the Perplexity student sign-up page.
   - When the SheerID popup/iframe appears, open Developer Tools (F12).
   - Go to the **Console** tab.
   - Run this code to get the URL:
     ```javascript
     console.log(Array.from(document.querySelectorAll('iframe, embed, object')).map(el => el.src || el.data).filter(src => src && src.includes('sheerid'))[0]);
     ```
   - Copy the URL output (it should look like `https://services.sheerid.com/verify/...`).

2. **Run the Tool**:
   ```bash
   python main.py "YOUR_VERIFICATION_URL"
   ```
   Or just run `python main.py` and paste the URL when prompted.

## Configuration

- **Proxies**: To use proxies, create a `proxy.txt` file in the same directory (see `proxy.example.txt`).
- **Data**: To use custom student data, create `data.txt` (see `data.example.txt`).

## Disclaimer

This tool is for educational purposes only. Use responsibly.
