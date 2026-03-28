# Gmall — Rebrand Manifest

Complete list of every file/area in Telegram-iOS that must be modified for the Gmall rebrand.

## Layer 1: App Identity (Blocks building/shipping)

| File | Change |
|------|--------|
| `build-system/gmall_configuration.json` | Bundle ID → `com.gmall.app`, own API creds, URL scheme → `gmall` |
| `Telegram/BUILD` | `AppNameInfoPlist`: "Telegram" → "Gmall" |
| `Telegram/BUILD` | Extension `CFBundleName` entries (Share, NotificationContent, Widget, BroadcastUpload, Watch) |
| `Telegram/BUILD` | `CFBundleURLSchemes`: `telegram`/`tg` → `gmall` |
| `Telegram/Telegram-iOS/Info.plist` | URL type handler references |
| `Telegram/Telegram-iOS/en.lproj/InfoPlist.strings` | Permission descriptions ("Telegram needs access to...") |
| `Telegram/Telegram-iOS/en.lproj/AppIntentVocabulary.plist` | Siri intent references |

## Layer 2: App Icon & Launch Screen

| File | Change |
|------|--------|
| `Telegram/Telegram-iOS/AppIcons.xcassets/` | Replace all icon sets (12+ variants) |
| `Telegram/BUILD` → `DefaultIcon` | Point to Gmall default icon |
| `Telegram/Telegram-iOS/Base.lproj/LaunchScreen.xib` | Update with Gmall branding |

Icon variants to replace:
- BlueIcon (default), BlackIcon, BlackClassicIcon, BlackFilledIcon
- BlueClassicIcon, BlueFilledIcon, WhiteFilledIcon
- New1, New2, Premium, PremiumBlack, PremiumTurbo

Required sizes (in points): 20, 29, 40, 58, 60, 76, 80, 87, 120, 152, 167, 180, 1024

## Layer 3: Color Theme

| File | Change |
|------|--------|
| `submodules/TelegramPresentationData/Sources/DefaultDayPresentationTheme.swift` | `defaultDayAccentColor` (`0x0088ff` → Gmall brand color) |
| `submodules/TelegramPresentationData/Sources/DefaultDayPresentationTheme.swift` | All hardcoded color values (nav bar, bubbles, links, buttons) |
| Dark theme equivalent file | Same treatment for dark mode |

Key Telegram colors to replace:
- `0x0088ff` — Primary accent (blue)
- `0xff3b30` — Destructive actions (red) — keep or customize
- `0x00c900` — Online status (green) — keep or customize

## Layer 4: Localized Strings (Largest change by volume)

| File | Change |
|------|--------|
| `Telegram/Telegram-iOS/en.lproj/Localizable.strings` | Replace "Telegram" → "Gmall" in all string values |
| All `*.lproj/Localizable.strings` across languages | Same replacement for every locale |
| Various Swift files in `submodules/` | Hardcoded "Telegram" strings in code |

Edge cases requiring manual review:
- "Telegram Premium" → "Gmall Premium"
- "Telegram Passport" → "Gmall Passport"
- URLs containing "telegram.org" — keep as-is (they point to Telegram's servers)
- Protocol references ("Telegram API", "MTProto") — keep as-is (technical terms)

## Layer 5: UI Screens with Brand References

| File/Area | Change |
|-----------|--------|
| `submodules/SettingsUI/` | About screen: "Telegram for iOS" → "Gmall for iOS" |
| `submodules/TelegramUI/Sources/` | Intro/onboarding: "Welcome to Telegram" |
| `Telegram/NotificationService/` | Push notification templates |
| `Telegram/Watch/` | WatchOS companion references |
| `Telegram/Share/` | "Share via Telegram" → "Share via Gmall" |

## Layer 6: Deep Internal References (Lower priority)

| File/Area | Change |
|-----------|--------|
| Entitlements files | Keychain access groups (currently `ph.telegra.Telegraph` based) |
| Various entitlements | App group identifiers for data sharing between app/extensions |
| Various Swift sources | `UserDefaults` suite names |
| `submodules/TelegramUI/Sources/` | Deep link handling — keep `tg://` and `t.me` for compatibility, add `gmall://` |
| Data container | Shared group container name `telegram-data` |

## Automation Coverage

| Script | Handles |
|--------|---------|
| `scripts/rebrand_build.py` | Layer 1 (BUILD file changes) |
| `scripts/rebrand_strings.py` | Layer 4 (all .strings files) |
| `scripts/rebrand_colors.py` | Layer 3 (theme colors) |
| `scripts/rebrand_swift.py` | Layers 5-6 (scan + report, manual fixes) |
| `scripts/verify_rebrand.sh` | All layers (post-rebrand verification) |
| Manual | Layer 2 (icon assets — require design work) |
