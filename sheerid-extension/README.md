# SheerID Verification Chrome Extension

A comprehensive Chrome extension for automated SheerID verification across multiple services. No need to run Python scripts on your PC!

## 🎯 Supported Services

### 🎓 Student Verification
- **Spotify Premium** - University student discount
- **YouTube Premium** - University student discount
- **Google One / Gemini Advanced** - University student discount (US only)
- **Perplexity** - University student discount
- **Cursor IDE** - Free 1-year pro subscription (.edu email required)

### 👨‍🏫 Teacher Verification
- **Bolt.new** - University teacher verification
- **Canva Education** - UK K-12 teacher verification
- **K12 / ChatGPT Plus** - K-12 teacher verification

### 🎖️ Military Verification
- **Veterans / ChatGPT Plus** - Military veteran verification

## 📦 Installation

### Method 1: Load Unpacked Extension (Development Mode)

1. Download or clone this repository
2. Open Chrome and go to `chrome://extensions/`
3. Enable "Developer mode" (toggle in top right)
4. Click "Load unpacked"
5. Select the `sheerid-extension` folder
6. The extension will appear in your toolbar!

### Method 2: From Release Package

1. Download the latest `.zip` release
2. Extract to a folder
3. Follow Method 1 steps 2-6

## 🚀 Usage

### Quick Start

1. **Select Service**: Click the extension icon and choose your desired service from the dropdown
2. **Configure**:
   - Leave email empty for automatic generation (recommended)
   - For veterans: Add your data in the format shown
3. **Save Configuration**: Click "💾 Save Configuration"
4. **Navigate**: Go to the verification page for your chosen service
5. **Fill Form**: The extension will auto-fill the form, or click "📝 Fill Form" manually
6. **Submit**: Review and submit the form

### Service-Specific Instructions

#### Student Services (Spotify, YouTube, Google One, Perplexity, Cursor)

1. Select the service from dropdown
2. Click "Save Configuration"
3. Navigate to the verification page:
   - **Spotify**: `https://www.spotify.com/student/`
   - **YouTube**: `https://www.youtube.com/premium/student`
   - **Google One**: `https://one.google.com/about/plans` (must be in US)
   - **Perplexity**: Go to settings → Upgrade
   - **Cursor**: `https://services.sheerid.com/verify/681044b7729fba7beccd3565/`
4. The extension will auto-fill with a random university student profile
5. Submit and wait for verification (24-48 hours for manual review)

#### Teacher Services (Bolt.new, Canva, K12)

1. Select the teacher service
2. Save configuration
3. Navigate to the teacher verification page
4. Auto-fill will generate appropriate teacher credentials
5. Submit and wait for approval

#### Veterans (ChatGPT Plus)

1. Select "Veterans / ChatGPT Plus"
2. Enter veteran data in format:
   ```
   JOHN|DOE|US ARMY|1985-01-15|2024-06-01
   ```
   (First|Last|Branch|DOB|Discharge Date)
3. Save configuration
4. Go to `https://chatgpt.com/veterans-claim`
5. Extension will auto-redirect and fill the form

### Features

- **Auto-Fill**: Automatically fills verification forms with realistic data
- **Smart Generation**: Uses weighted university selection for higher success rates
- **Statistics Tracking**: Track your success/failure/pending verifications
- **Export/Import**: Backup and restore your configuration
- **Multiple Services**: One extension for all SheerID verifications

## 📊 Statistics

The extension tracks:
- ✅ **Success**: Verifications that passed
- ❌ **Failed**: Verifications that were rejected
- ⏭️ **Pending**: Verifications under review

View stats in the popup interface.

## ⚙️ Advanced Options

### Auto Mode

Click "🚀 Auto Run" to enable automatic retry on errors. The extension will:
- Detect verification failures
- Automatically retry with new data
- Continue until success or manual stop

### Manual Control

- **Fill Form**: Manually trigger form filling
- **Enable/Disable**: Toggle extension on/off
- **Clear Stats**: Reset all statistics

## 🔒 Privacy & Security

- All data generation happens locally in your browser
- No data is sent to external servers (except SheerID API)
- Generated identities are randomized and realistic
- Extension only activates on SheerID and service pages

## ⚠️ Important Notes

1. **Google One/Gemini**: Only works with US IP addresses (use US proxy if needed)
2. **Cursor**: Requires .edu email - extension generates from university domain
3. **Manual Review**: Most verifications require 24-48 hours for manual document review
4. **Success Rate**: Varies by service - university selection is optimized for higher success
5. **Document Upload**: Extension can generate student IDs and transcripts if required

## 🛠️ Troubleshooting

### Extension Not Working

1. Check that extension is enabled (green toggle)
2. Refresh the verification page
3. Check browser console for errors (F12)
4. Try disabling and re-enabling the extension

### Form Not Filling

1. Ensure you're on a SheerID verification page
2. Click "Fill Form" manually from popup
3. Check that JavaScript is enabled
4. Try reloading the extension

### Verification Failed

1. Try a different university from the pool
2. Check if service requires specific document type
3. For Gemini/Google One, ensure you're using US IP
4. Wait 24-48 hours for manual review

## 📝 File Structure

```
sheerid-extension/
├── manifest.json              # Extension configuration
├── popup.html                 # Popup interface
├── popup.js                   # Popup logic
├── background.js              # Background service worker
├── content.js                 # Main content script
├── lib/
│   ├── anti-detect.js        # Anti-detection utilities
│   ├── doc-generator.js      # Document generation
│   └── utils.js              # Helper functions
├── data/
│   ├── universities.js       # University database
│   └── schools.js            # K-12 schools database
└── icons/                     # Extension icons
```

## 🤝 Contributing

This extension is part of the [SheerID Verification Tool](https://github.com/ThanhNguyxn/SheerID-Verification-Tool) project.

## 📄 License

MIT License - See repository for details

## ⚠️ Disclaimer

This tool is for **educational purposes only**. Use responsibly and in accordance with service terms.

## 💖 Support

If you find this helpful:
- ⭐ Star the repository
- 🐛 Report bugs via GitHub issues
- ☕ [Buy me a coffee](https://buymeacoffee.com/thanhnguyxn)
- ❤️ [Become a sponsor](https://github.com/sponsors/ThanhNguyxn)

---

**Made with ❤️ by [ThanhNguyxn](https://github.com/ThanhNguyxn)**
