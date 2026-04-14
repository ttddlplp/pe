# Gmall - Custom Telegram iOS Client

## Project Overview
Gmall is a rebranded fork of Telegram-iOS. This repo contains the rebrand scripts, config, and assets. The actual Telegram-iOS source lives in `telegram-ios/` (a git submodule/clone, not committed to this repo).

## Current State
- Branch: `claude/fresh-start-6Jmqd`
- Telegram-iOS cloned into `telegram-ios/` via `scripts/setup_fork.sh`
- Working branch inside telegram-ios: `gmall/main`
- API credentials configured in `telegram-ios/config/gmall_configuration.json`
- Rebrand scripts already run (build, strings, colors)
- Xcode project generated at `telegram-ios/Telegram/Telegram.xcodeproj`
- Build mode: simulator-only (no paid Apple Developer account, free Apple ID with team_id `5TM446QYFD`)

## Build Commands
```bash
# From repo root — generate Xcode project (already done)
cd telegram-ios
python3 build-system/Make/Make.py \
    --cacheDir="$HOME/telegram-bazel-cache" \
    generateProject \
    --configurationPath config/gmall_configuration.json \
    --xcodeManagedCodesigning \
    --disableProvisioningProfiles \
    --disableExtensions

# Open in Xcode
open Telegram/Telegram.xcodeproj
```

## Rebrand Scripts (run from inside telegram-ios/)
```bash
python3 ../scripts/rebrand_build.py .      # Patch BUILD file
python3 ../scripts/rebrand_strings.py .    # Replace "Telegram" in .strings
python3 ../scripts/rebrand_colors.py .     # Update accent colors (0x6C5CE7)
python3 ../scripts/rebrand_swift.py .      # Scan Swift for hardcoded refs
../scripts/verify_rebrand.sh .             # Verify completeness
```

## Key Files
- `config/gmall_configuration.json` — build config template (no secrets)
- `telegram-ios/config/gmall_configuration.json` — active config WITH credentials
- `scripts/` — all rebrand and setup scripts
- `docs/SETUP_GUIDE.md` — detailed environment setup
- `docs/REBRAND_MANIFEST.md` — every file that gets modified
- `assets/brand_guidelines.md` — color palette, typography
- `research.md` — feasibility study

## Build Requirements
- Xcode 26.4 (pinned in telegram-ios/versions.json)
- macOS 26
- Bazel 8.4.2 (auto-downloaded)
- Python 3

## Credentials
- API credentials: configured (api_id: 33450869)
- Team ID: 5TM446QYFD (free Apple ID: ttddlplp@gmail.com)
- No paid Apple Developer account — sideloaded apps expire after 7 days
