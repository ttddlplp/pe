# Gmall Brand Guidelines

## Color Palette

### Primary Colors
| Name | Hex | RGB | Usage |
|------|-----|-----|-------|
| Gmall Purple | `#6C5CE7` | 108, 92, 231 | Primary accent, buttons, links, nav bar tint |
| Gmall Dark | `#2D3436` | 45, 52, 54 | Text, dark backgrounds |
| Gmall Light | `#DFE6E9` | 223, 230, 233 | Light backgrounds, separators |
| White | `#FFFFFF` | 255, 255, 255 | Backgrounds, text on dark |

### Status Colors
| Name | Hex | Usage |
|------|-----|-------|
| Online Green | `#00B894` | Online status indicator |
| Error Red | `#FF3B30` | Destructive actions, errors |
| Warning Orange | `#FDCB6E` | Warnings |

### Message Bubbles
| Element | Light Mode | Dark Mode |
|---------|-----------|-----------|
| Outgoing bubble | `#6C5CE7` | `#5B4CC4` |
| Incoming bubble | `#F0F0F0` | `#2D2D2D` |
| Outgoing text | `#FFFFFF` | `#FFFFFF` |
| Incoming text | `#000000` | `#FFFFFF` |

> **Note:** Edit `scripts/rebrand_colors.py` and update `GMALL_ACCENT_COLOR` to match the chosen primary color before running. The default is set to `0x6C5CE7`.

## App Icon

### Requirements
The following icon sizes are needed for iOS (all in PNG format):

| Size (px) | Usage |
|-----------|-------|
| 40x40 | iPhone Notification @2x |
| 60x60 | iPhone Notification @3x |
| 58x58 | iPhone Settings @2x |
| 87x87 | iPhone Settings @3x |
| 80x80 | iPhone Spotlight @2x |
| 120x120 | iPhone Spotlight @3x / App @2x |
| 180x180 | iPhone App @3x |
| 152x152 | iPad App @2x |
| 167x167 | iPad Pro App @2x |
| 1024x1024 | App Store |

### Icon Variants
Telegram supports 12+ alternate icons. For V1, create at minimum:
- **Default icon** — Gmall branding on purple background
- **Dark icon** — Gmall branding on dark background

Place icon PNGs in `assets/app_icons/` matching the sizes above.

## Typography

Use system fonts (San Francisco on iOS) — no custom fonts needed for V1.

## Naming

- App name: **Gmall**
- Never use "Telegram" in user-visible text
- Acceptable: "Built on the Telegram API" (in about/legal screens only)
