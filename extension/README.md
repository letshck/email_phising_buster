# Email Phishing Detector Browser Extension

## Installation

1. Start the Flask API:
   ```
   cd d:\emailphis
   D:/emailphis/.venv/Scripts/activate.ps1
   python src/app.py
   ```

2. Load extension in Chrome:
   - Open Chrome and go to `chrome://extensions/`
   - Enable "Developer mode"
   - Click "Load unpacked"
   - Select the `d:\emailphis\extension` folder

## Usage

1. Navigate to Gmail, Outlook, or Yahoo Mail
2. Open an email
3. Click the extension icon
4. Click "Analyze Current Email" to extract and analyze
5. Or paste email text manually and click "Analyze Email"

## Features

- Detects phishing emails with confidence scores
- Works with Gmail, Outlook, Yahoo Mail
- Manual text input option
- Real-time analysis via local API