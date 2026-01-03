# Perplexity AI Verification Tool

Automated SheerID verification for Perplexity Pro student discount.

## Features

- **Automated Verification**: Generates student info, documents, and handles the verification flow.
- **Smart University Selection**: Picks universities with high success rates.
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

### Step 1: Get the Verification URL

1. Go to [Perplexity Settings](https://www.perplexity.ai/settings/account) or the student discount page.
2. When the SheerID verification popup/iframe appears, open **DevTools** (press `F12`).
3. Go to the **Console** tab.
4. Paste and run this JavaScript code:

```javascript
console.log(Array.from(document.querySelectorAll('iframe, embed, object')).map(el => el.src || el.data).filter(src => src && src.includes('sheerid'))[0]);
```

5. Copy the URL that appears in the console. It should look like:
   ```
   https://services.sheerid.com/verify/XXXXXXX/?verificationId=XXXXXXX
   ```

### Step 2: Run the Tool

```bash
# Option 1: Pass URL as argument
python main.py "https://services.sheerid.com/verify/...?verificationId=..."

# Option 2: Run interactively (paste URL when prompted)
python main.py
```

## Configuration

- **Proxies**: Create a `proxy.txt` file in the same directory (see `proxy.example.txt`).
- **Custom Data**: Create `data.txt` for custom student data (see `data.example.txt`).

## Troubleshooting

### "Invalid URL" Error

Make sure your URL:
- Contains `sheerid.com`
- Has a `verificationId` parameter (e.g., `?verificationId=abc123...`)

If the JavaScript snippet doesn't return a URL, the SheerID iframe may not have loaded yet. Wait for the verification popup to fully load and try again.

### "Already verified" or "Already pending"

The verification link has already been used. You need to generate a new link from Perplexity.

## Disclaimer

This tool is for educational purposes only. Use responsibly.
