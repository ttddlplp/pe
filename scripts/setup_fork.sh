#!/bin/bash
# Set up the Telegram-iOS fork for Gmall development.

set -euo pipefail

REPO_URL="https://github.com/TelegramMessenger/Telegram-iOS.git"
TARGET_DIR="telegram-ios"

echo "=== Gmall Fork Setup ==="
echo ""

if [ -d "$TARGET_DIR" ]; then
    echo "Directory '$TARGET_DIR' already exists."
    echo "Remove it first if you want a fresh clone: rm -rf $TARGET_DIR"
    exit 1
fi

echo "Cloning Telegram-iOS (this may take a while)..."
git clone --recursive -j8 "$REPO_URL" "$TARGET_DIR"

cd "$TARGET_DIR"

echo ""
echo "Setting up remotes..."
git remote rename origin upstream
echo "  upstream -> $REPO_URL"

echo ""
echo "Creating gmall branch..."
git checkout -b gmall/main
echo "  Created branch: gmall/main"

echo ""
echo "Checking required versions..."
if [ -f "versions.json" ]; then
    echo "  versions.json:"
    cat versions.json
else
    echo "  versions.json not found (check repo structure)"
fi

echo ""
echo "=== Setup Complete ==="
echo ""
echo "Next steps:"
echo "  1. Copy config:  cp ../config/gmall_configuration.json config/gmall_configuration.json"
echo "  2. Edit config:  Fill in api_id, api_hash, team_id"
echo "  3. Run rebrand:  python3 ../scripts/rebrand_build.py ."
echo "                   python3 ../scripts/rebrand_strings.py ."
echo "                   python3 ../scripts/rebrand_colors.py ."
echo "  4. Generate:     python3 build-system/Make/Make.py \\"
echo "                       --configurationPath config/gmall_configuration.json \\"
echo "                       generateProject --xcodeManagedCodesigning"
echo "  5. Build:        Open .xcodeproj in Xcode, select device, Cmd+R"
