# Gmall

A custom Telegram client for iOS, built as a full rebrand fork of [Telegram-iOS](https://github.com/TelegramMessenger/Telegram-iOS).

Gmall provides full Telegram feature parity with a distinct brand identity — new name, icon, color scheme, and UI text.

## Status

**V1 — Feature Parity Release**
- Full Telegram messaging functionality (inherited from fork)
- Complete visual rebrand (Gmall branding, colors, icons)
- Sideload deployment via Xcode (no App Store)

## Building

### Prerequisites

- macOS (version per `versions.json` in Telegram-iOS repo)
- Xcode (version per `versions.json`)
- Python 3
- Free Apple ID (sign in via Xcode > Settings > Accounts)
- API credentials from [my.telegram.org](https://my.telegram.org)
- iPhone connected via USB

### Quick Start

```bash
# 1. Clone and set up the fork
./scripts/setup_fork.sh

# 2. Copy and fill in your credentials
cp config/gmall_configuration.json telegram-ios/config/gmall_configuration.json
# Edit the file with your api_id, api_hash, and team_id

# 3. Run the rebrand scripts
cd telegram-ios
../scripts/rebrand_build.py
../scripts/rebrand_strings.py
../scripts/rebrand_colors.py

# 4. Generate Xcode project
python3 build-system/Make/Make.py \
    --configurationPath config/gmall_configuration.json \
    generateProject \
    --xcodeManagedCodesigning

# 5. Open in Xcode, select your device, hit Run
```

### Sideload Notes

With a free Apple ID, the app expires after 7 days and must be re-deployed. This is an iOS limitation for non-developer-program accounts. A paid Apple Developer account ($99/year) removes this restriction.

## Project Structure

```
├── README.md                  # This file
├── LICENSE                    # GPL v2 (matching Telegram-iOS)
├── research.md                # Feasibility study
├── config/
│   └── gmall_configuration.json   # Build config template (no secrets)
├── docs/
│   ├── SETUP_GUIDE.md         # Detailed environment setup
│   └── REBRAND_MANIFEST.md    # Every file that gets modified
├── scripts/
│   ├── setup_fork.sh          # Clone + init Telegram-iOS fork
│   ├── rebrand_build.py       # Patch Telegram/BUILD
│   ├── rebrand_strings.py     # Replace "Telegram" in .strings files
│   ├── rebrand_colors.py      # Replace accent colors in theme files
│   ├── rebrand_swift.py       # Scan Swift code for hardcoded refs
│   └── verify_rebrand.sh      # Post-rebrand verification
└── assets/
    ├── brand_guidelines.md    # Color palette, typography
    └── app_icons/             # Icon assets (placeholder)
```

## How It Works

Gmall is a direct fork of Telegram's official iOS client. It connects to the same Telegram servers using the same protocol — all messages, contacts, groups, and channels work identically across all Telegram clients. The difference is purely in branding and UI presentation.

## Legal

- This project is licensed under **GPL v2**, matching the upstream Telegram-iOS license
- This app uses the [Telegram API](https://core.telegram.org/api)
- "Telegram" is a registered trademark of Telegram FZE LLC. Gmall is an independent project
- API credentials are obtained per [Telegram's API Terms of Service](https://core.telegram.org/api/terms)

## Attribution

Based on [Telegram-iOS](https://github.com/TelegramMessenger/Telegram-iOS) by Telegram Messenger LLP.
