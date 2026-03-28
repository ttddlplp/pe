# Gmall — Setup Guide

## Prerequisites

### Hardware/Software
- **Mac** running macOS (check `versions.json` in Telegram-iOS repo for exact version)
- **Xcode** (exact version from `versions.json` — mismatched versions will fail)
- **Python 3** (for the Bazel build orchestrator)
- **Git** with submodule support
- **~20GB free disk space** (source + submodules + build artifacts)
- **iPhone** connected via USB (for sideloading)

### Credentials
1. **Telegram API credentials** — Register at https://my.telegram.org
   - Log in with your phone number
   - Go to "API development tools"
   - Create app: title "Gmall", platform "iOS"
   - Save your `api_id` (number) and `api_hash` (string)

2. **Apple ID** — Free account is sufficient for sideloading
   - Sign into Xcode > Settings > Accounts
   - No paid Developer Program needed (app expires every 7 days)

## Step 1: Set Up the Fork

Run the automated setup script from the Gmall repo root:

```bash
./scripts/setup_fork.sh
```

This will:
- Clone `TelegramMessenger/Telegram-iOS` into `telegram-ios/`
- Initialize all 229 submodules
- Set up the upstream remote for future syncs

If you prefer manual setup:

```bash
git clone --recursive -j8 https://github.com/TelegramMessenger/Telegram-iOS.git telegram-ios
cd telegram-ios
git remote rename origin upstream
```

## Step 2: Configure Credentials

```bash
cp config/gmall_configuration.json telegram-ios/config/gmall_configuration.json
```

Edit `telegram-ios/config/gmall_configuration.json` and fill in:
- `api_id` — from my.telegram.org
- `api_hash` — from my.telegram.org
- `team_id` — your Apple Team ID (visible in Xcode > Settings > Accounts > click your team)

## Step 3: Run Rebrand Scripts

From the Gmall repo root:

```bash
cd telegram-ios

# Patch the BUILD file (app name, extensions, URL schemes)
python3 ../scripts/rebrand_build.py .

# Replace "Telegram" in all localization files
python3 ../scripts/rebrand_strings.py .

# Update accent colors to Gmall brand
python3 ../scripts/rebrand_colors.py .

# Scan Swift code for remaining hardcoded refs (generates report)
python3 ../scripts/rebrand_swift.py .

# Verify no "Telegram" remains in user-facing text
../scripts/verify_rebrand.sh .
```

## Step 4: Generate Xcode Project

```bash
python3 build-system/Make/Make.py \
    --configurationPath config/gmall_configuration.json \
    generateProject \
    --xcodeManagedCodesigning
```

This generates an `.xcodeproj` file. Bazel is downloaded automatically on first run.

## Step 5: Build and Deploy

1. Open the generated `.xcodeproj` in Xcode
2. Select your connected iPhone as the build target
3. If prompted about signing, select your free Apple ID team
4. Press **Cmd+R** to build and run
5. On first launch, go to iPhone Settings > General > VPN & Device Management > trust your developer certificate

## Troubleshooting

### "Untrusted Developer" on iPhone
Settings > General > VPN & Device Management > tap your Apple ID > Trust

### Build fails with version mismatch
Check `telegram-ios/versions.json` for required Xcode and macOS versions. The build system enforces exact version matching.

### App expires after 7 days
This is normal with free Apple ID signing. Re-deploy from Xcode to renew. A paid Developer account ($99/year) removes this limit.

### Submodule init fails
```bash
git submodule update --init --recursive -j8
```
If specific submodules fail, try them individually without `-j8`.

## Syncing with Upstream Telegram

To pull in new Telegram updates:

```bash
cd telegram-ios
git fetch upstream
git merge upstream/master
# Resolve any conflicts with rebrand changes
# Re-run rebrand scripts if new files were added
python3 ../scripts/rebrand_strings.py .
../scripts/verify_rebrand.sh .
```
