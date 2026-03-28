#!/usr/bin/env python3
"""Replace Telegram's default accent colors with Gmall brand colors in theme files."""

import os
import re
import sys

# Telegram's default accent blue: #0088FF (appears as 0x0088ff in Swift)
# Change this to your Gmall brand color
GMALL_ACCENT_COLOR = "0x6C5CE7"  # Purple — change to your preferred color

# Color mapping: old Telegram color -> new Gmall color
COLOR_MAP = {
    "0x0088ff": GMALL_ACCENT_COLOR,      # Primary accent
    "0x007ee5": GMALL_ACCENT_COLOR,      # Alternate accent blue
    "0x007aff": GMALL_ACCENT_COLOR,      # iOS-style blue accent
    "0x168acd": GMALL_ACCENT_COLOR,      # Navigation tint
}

# Files known to contain theme color definitions
THEME_FILES = [
    "submodules/TelegramPresentationData/Sources/DefaultDayPresentationTheme.swift",
    "submodules/TelegramPresentationData/Sources/DefaultDarkPresentationTheme.swift",
    "submodules/TelegramPresentationData/Sources/DefaultDarkTintedPresentationTheme.swift",
    "submodules/TelegramPresentationData/Sources/PresentationTheme.swift",
]


def replace_colors_in_file(filepath: str) -> int:
    """Replace color hex values in a Swift theme file. Returns change count."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"  Skipped (not found): {filepath}")
        return 0

    original = content
    changes = 0

    for old_color, new_color in COLOR_MAP.items():
        # Match case-insensitive hex colors in UIColor(rgb:) calls
        pattern = re.compile(re.escape(old_color), re.IGNORECASE)
        matches = pattern.findall(content)
        if matches:
            content = pattern.sub(new_color, content)
            changes += len(matches)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  Modified: {filepath} ({changes} color replacements)")
    else:
        print(f"  No matching colors: {filepath}")

    return changes


def scan_for_additional_theme_files(root: str) -> list[str]:
    """Find additional files that might contain theme colors."""
    extra = []
    for dirpath, _, filenames in os.walk(root):
        for fname in filenames:
            if fname.endswith('.swift') and 'theme' in fname.lower():
                filepath = os.path.join(dirpath, fname)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    for color in COLOR_MAP:
                        if color.lower() in content.lower():
                            extra.append(filepath)
                            break
                except (UnicodeDecodeError, FileNotFoundError):
                    pass
    return extra


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <telegram-ios-root>")
        print(f"\nCurrent Gmall accent color: {GMALL_ACCENT_COLOR}")
        print("Edit this script to change GMALL_ACCENT_COLOR before running.")
        sys.exit(1)

    root = sys.argv[1]
    if not os.path.isdir(root):
        print(f"Error: {root} is not a directory")
        sys.exit(1)

    print(f"Gmall accent color: {GMALL_ACCENT_COLOR}")
    print(f"Replacing Telegram colors: {list(COLOR_MAP.keys())}\n")

    total_changes = 0

    # Process known theme files
    print("=== Known theme files ===")
    for rel_path in THEME_FILES:
        filepath = os.path.join(root, rel_path)
        total_changes += replace_colors_in_file(filepath)

    # Scan for additional theme files
    print("\n=== Scanning for additional theme files ===")
    extra_files = scan_for_additional_theme_files(root)
    known_abs = {os.path.join(root, p) for p in THEME_FILES}
    for filepath in extra_files:
        if filepath not in known_abs:
            total_changes += replace_colors_in_file(filepath)

    print(f"\nDone: {total_changes} total color replacements")


if __name__ == "__main__":
    main()
