#!/bin/bash
# Build the app via Bazel, install on a physical iOS device, and launch.
# Requires provisioning profiles to exist for com.spinora.gmall.app and extensions
# (generated via Xcode with the device connected — see NOTES below).

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TG_ROOT="$REPO_ROOT/telegram-ios"
BAZEL="$TG_ROOT/build-input/bazel-8.4.2-darwin-arm64"
BUNDLE_ID="com.spinora.gmall.app"
EXTRACT_DIR="/tmp/telegram_device_extracted"

# Optionally override with: DEVICE_ID=<UDID> ./scripts/run_device.sh
DEVICE_ID="${DEVICE_ID:-}"

if [ -z "$DEVICE_ID" ]; then
    # Auto-pick the first available paired device
    DEVICE_ID=$(xcrun devicectl list devices 2>/dev/null | \
        awk '/available \(paired\)/ {print $3; exit}')
    if [ -z "$DEVICE_ID" ]; then
        echo "ERROR: no paired device found. Connect your iPhone via USB."
        echo "       Or set DEVICE_ID=<UDID> manually."
        echo ""
        echo "Available devices:"
        xcrun devicectl list devices
        exit 1
    fi
fi

echo "==> Using device: $DEVICE_ID"

echo "==> Building via Bazel for device (arm64)..."
cd "$TG_ROOT"
"$BAZEL" build //Telegram:Telegram \
    -c dbg \
    --ios_multi_cpus=arm64 \
    --watchos_cpus=arm64_32 \
    --//Telegram:disableExtensions

echo "==> Extracting IPA..."
rm -rf "$EXTRACT_DIR"
mkdir -p "$EXTRACT_DIR"
cd "$EXTRACT_DIR"
unzip -q "$TG_ROOT/bazel-bin/Telegram/Telegram.ipa"

echo "==> Installing on device..."
xcrun devicectl device install app \
    --device "$DEVICE_ID" \
    "$EXTRACT_DIR/Payload/Telegram.app"

echo "==> Launching..."
xcrun devicectl device process launch \
    --device "$DEVICE_ID" \
    --terminate-existing \
    "$BUNDLE_ID"

echo "==> Done."
echo ""
echo "NOTE: With a free Apple ID, the app expires in 7 days."
echo "      Re-run this script to redeploy."
