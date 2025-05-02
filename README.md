# CloudGram

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

CloudGram is a command-line tool for sending messages and files to your Telegram Saved Messages. Perfect for quick notes, file backups, or syncing content across devices.

## Features

- Send text messages to Saved Messages
- Attach files or entire folders (automatically zipped)
- Tag messages for organization
- Cross-platform support
- Simple authentication flow

## Installation

### Using Homebrew (macOS/Linux)
```bash
brew tap ArturArutunyan/cloudgram
brew install cloudgram
```
### Using Homebrew (macOS/Linux)
1. Clone the repository
   ```bash
   git clone https://github.com/ArturArutunyan/cloudgram.git
   cd cloudgram
   ```
2. Create virtual environment:
   ```bash
   python3.12 -m venv .venv
   source .venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## First-Time Setup
1. Get your Telegram API credentials:
  -  Visit [my.telegram.org](https://my.telegram.org "Telegram API development platform")
  -  Create new application (Name: CloudGram, Platform: Desktop)
   ```bash
    cloudgram "Test message"
   ```

## Usage

### Basic Commands
```bash
# Send simple message
cloudgram "Hello from CloudGram!"

# Send message with custom tag
cloudgram "Important note" -t important
```

### File Operations
```bash
# Send single file
cloudgram "Check this document" -f document.pdf

# Send entire folder (will be zipped)
cloudgram "Project backup" -f ./my_project/
```

### File Operations
```bash
cloudgram --help
```

## Configuration

  - Session data is stored in cloudgram_*.session files
  - Configuration saved in config.json
  - To reset credentials, delete these files and restart

## Troubleshooting

If you get authentication errors:
  1. Delete config.json and session files
  2. Restart CloudGram
  3. Re-enter your API credentials

## License

MIT License

Copyright (c) 2025 Artur Arutunyan

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
