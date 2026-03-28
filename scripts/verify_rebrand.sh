#!/bin/bash
# Verify the Gmall rebrand is complete — check for remaining "Telegram" references.

set -euo pipefail

ROOT="${1:-.}"

echo "=== Gmall Rebrand Verification ==="
echo "Scanning: $ROOT"
echo ""

# Acceptable patterns (module names, URLs, protocol terms)
EXCLUDE_PATTERN='(TelegramCore|TelegramUI|TelegramApi|TelegramPresentationData|TelegramCallsUI|TelegramVoip|TelegramStringFormatting|TelegramBaseController|TelegramNotices|TelegramAudio|TelegramMediaResources|TelegramUniversalVideoContent|TelegramAnimatedStickerNode|import Telegram|@testable import|telegram\.org|telegram\.me|core\.telegram\.org|t\.me|MTProto|\.git/|Pods/|build/|DerivedData/)'

echo "--- User-visible strings (.strings files) ---"
STRINGS_COUNT=$(grep -r "Telegram" "$ROOT" --include="*.strings" 2>/dev/null | grep -vE "$EXCLUDE_PATTERN" | wc -l || true)
if [ "$STRINGS_COUNT" -gt 0 ]; then
    echo "WARNING: $STRINGS_COUNT remaining references in .strings files:"
    grep -rn "Telegram" "$ROOT" --include="*.strings" 2>/dev/null | grep -vE "$EXCLUDE_PATTERN" | head -20
else
    echo "PASS: No remaining references in .strings files"
fi

echo ""
echo "--- Info.plist files ---"
PLIST_COUNT=$(grep -r "Telegram" "$ROOT" --include="*.plist" --include="*.strings" 2>/dev/null | grep -i "InfoPlist\|Info\.plist" | grep -vE "$EXCLUDE_PATTERN" | wc -l || true)
if [ "$PLIST_COUNT" -gt 0 ]; then
    echo "WARNING: $PLIST_COUNT remaining references in plist files:"
    grep -rn "Telegram" "$ROOT" --include="*.plist" 2>/dev/null | grep -vE "$EXCLUDE_PATTERN" | head -10
else
    echo "PASS: No remaining references in plist files"
fi

echo ""
echo "--- BUILD files ---"
BUILD_COUNT=$(grep -r "Telegram" "$ROOT" -l --include="BUILD" 2>/dev/null | wc -l || true)
if [ "$BUILD_COUNT" -gt 0 ]; then
    echo "INFO: $BUILD_COUNT BUILD files still reference 'Telegram' (some are expected for module names):"
    grep -rn "<string>Telegram</string>" "$ROOT" --include="BUILD" 2>/dev/null | head -10
else
    echo "PASS: No app-name references in BUILD files"
fi

echo ""
echo "--- Swift string literals ---"
SWIFT_COUNT=$(grep -rn '"[^"]*Telegram[^"]*"' "$ROOT" --include="*.swift" 2>/dev/null | grep -vE "$EXCLUDE_PATTERN" | wc -l || true)
if [ "$SWIFT_COUNT" -gt 0 ]; then
    echo "WARNING: $SWIFT_COUNT Swift string literals containing 'Telegram':"
    grep -rn '"[^"]*Telegram[^"]*"' "$ROOT" --include="*.swift" 2>/dev/null | grep -vE "$EXCLUDE_PATTERN" | head -20
else
    echo "PASS: No user-visible Swift string literals"
fi

echo ""
echo "--- Summary ---"
TOTAL=$((STRINGS_COUNT + PLIST_COUNT + SWIFT_COUNT))
if [ "$TOTAL" -eq 0 ]; then
    echo "ALL CLEAR: Rebrand appears complete."
else
    echo "ATTENTION: $TOTAL items may need review."
    echo "Some may be false positives (module names, comments). Review manually."
fi
