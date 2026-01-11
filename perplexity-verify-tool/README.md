# Perplexity AI Verification Tool

Automated SheerID verification for Perplexity Pro student discount.

## Features

- **Automated Verification**: Generates student info, documents, and handles the verification flow.
- **Smart University Selection**: Picks universities with high success rates.
- **Groningen Bypass**: Specialized mode for University of Groningen using high-quality PDF invoice generation.
- **Success Tracking**: Logs success rates per university to `stats.json`.

## Requirements

- Python 3.8+
- `httpx`
- `Pillow` (for image processing)
- `PyMuPDF` (for PDF text replacement)

## Installation

```bash
pip install httpx Pillow PyMuPDF
```

**[Optional] Enhanced Anti-Detection:**
```bash
pip install curl_cffi cloudscraper
```
> `curl_cffi` spoofs TLS fingerprint to look like real Chrome browser

## Setup

1. Ensure the `assets` folder contains:
   - `docs.pdf`: The base tuition fee invoice template (University of Groningen).
   - `groningen_logo.png`: (Optional) Logo for fallback generation.
   - `signature.png`: (Optional) Signature for fallback generation.

## Usage

### Step 1: Get the Verification URL

1. **IMPORTANT**: Switch your IP to **Netherlands** (VPN/Proxy) *before* accessing Perplexity.
2. Go to [Perplexity Settings](https://www.perplexity.ai/settings/account) or the student discount page.
3. When the SheerID verification popup/iframe appears, open **DevTools** (press `F12`).
4. Go to the **Network** tab.
5. Filter by `sheerid`.
6. Look for a request that starts with `verification` or the ID (e.g., `695a...`).
7. Right-click the request -> **Copy URL**.
   - The URL should look like: `https://services.sheerid.com/rest/v2/verification/695a...`

### Step 2: Run the Tool

```bash
# Option 1: Standard run (interactive)
python main.py

# Option 2: Pass URL as argument
python main.py "https://services.sheerid.com/verify/...?verificationId=..."
```

**Note:** This tool is configured to use the **University of Groningen** bypass strategy by default. You must use a **Netherlands IP address** for this to work.

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
