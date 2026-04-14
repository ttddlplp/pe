#!/bin/bash
# Build the app via Bazel, install on the booted simulator, and launch.
# Use this instead of Cmd+R in Xcode (Xcode 26 + rules_xcodeproj is broken).

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TG_ROOT="$REPO_ROOT/telegram-ios"
BAZEL="$TG_ROOT/build-input/bazel-8.4.2-darwin-arm64"
BUNDLE_ID="com.spinora.gmall.app"
EXTRACT_DIR="/tmp/telegram_extracted"

EXTENSION_IDS=(
    "$BUNDLE_ID"
    "$BUNDLE_ID.Widget"
    "$BUNDLE_ID.Share"
    "$BUNDLE_ID.NotificationService"
    "$BUNDLE_ID.NotificationContent"
    "$BUNDLE_ID.BroadcastUpload"
    "$BUNDLE_ID.SiriIntents"
    "$BUNDLE_ID.watchkitapp"
)

echo "==> Building via Bazel..."
cd "$TG_ROOT"
"$BAZEL" build //Telegram:Telegram \
    -c dbg \
    --ios_multi_cpus=sim_arm64 \
    --//Telegram:disableProvisioningProfiles

echo "==> Extracting IPA..."
rm -rf "$EXTRACT_DIR"
mkdir -p "$EXTRACT_DIR"
cd "$EXTRACT_DIR"
unzip -q "$TG_ROOT/bazel-bin/Telegram/Telegram.ipa"

echo "==> Uninstalling old app + extensions from booted simulator..."
for id in "${EXTENSION_IDS[@]}"; do
    xcrun simctl uninstall booted "$id" 2>/dev/null || true
done

echo "==> Installing..."
xcrun simctl install booted "$EXTRACT_DIR/Payload/Telegram.app"

echo "==> Launching..."
xcrun simctl launch booted "$BUNDLE_ID"

echo "==> Done."
