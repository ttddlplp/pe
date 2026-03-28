#!/usr/bin/env python3
"""Patch Telegram/BUILD file for Gmall rebrand: app name, extensions, URL schemes."""

import os
import re
import sys

OLD_NAME = "Telegram"
NEW_NAME = "Gmall"
OLD_SCHEME = "tg"
NEW_SCHEME = "gmall"
OLD_BUNDLE_PREFIX = "ph.telegra"
NEW_BUNDLE_PREFIX = "com.gmall"


def patch_build_file(build_path: str) -> int:
    """Patch the main Telegram/BUILD file. Returns number of changes."""
    with open(build_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    changes = 0

    # 1. Replace app display name in AppNameInfoPlist
    # Pattern: <string>Telegram</string>
    content, n = re.subn(
        r'(<string>)Telegram(</string>)',
        rf'\g<1>{NEW_NAME}\g<2>',
        content
    )
    changes += n

    # 2. Replace CFBundleName entries for extensions
    # These appear as string values in plist fragments
    content, n = re.subn(
        r'(CFBundleName.*?<string>)Telegram([^<]*</string>)',
        rf'\g<1>{NEW_NAME}\2',
        content
    )
    changes += n

    # 3. Replace URL schemes: "tg" and "telegram"
    content, n = re.subn(
        r'(<string>)telegram(</string>)',
        rf'\g<1>{NEW_SCHEME}\g<2>',
        content
    )
    changes += n

    content, n = re.subn(
        r'(<string>)tg(</string>)',
        rf'\g<1>{NEW_SCHEME}\g<2>',
        content
    )
    changes += n

    # 4. Replace app_specific_url_scheme references
    content, n = re.subn(
        r'(app_specific_url_scheme.*?")telegram(")',
        rf'\g<1>{NEW_SCHEME}\2',
        content
    )
    changes += n

    if content != original:
        with open(build_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Patched BUILD file: {changes} changes")
    else:
        print("No changes needed in BUILD file")

    return changes


def patch_info_plist_strings(root: str) -> int:
    """Patch InfoPlist.strings files (permission descriptions)."""
    changes = 0
    for dirpath, _, filenames in os.walk(root):
        for fname in filenames:
            if fname == 'InfoPlist.strings':
                filepath = os.path.join(dirpath, fname)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                except (UnicodeDecodeError, FileNotFoundError):
                    continue

                if OLD_NAME not in content:
                    continue

                new_content = content.replace(OLD_NAME, NEW_NAME)
                if new_content != content:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    rel = os.path.relpath(filepath, root)
                    n = content.count(OLD_NAME)
                    print(f"  Patched {rel}: {n} replacements")
                    changes += n

    return changes


def patch_intent_vocabulary(root: str) -> int:
    """Patch AppIntentVocabulary.plist files."""
    changes = 0
    for dirpath, _, filenames in os.walk(root):
        for fname in filenames:
            if fname == 'AppIntentVocabulary.plist':
                filepath = os.path.join(dirpath, fname)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                except (UnicodeDecodeError, FileNotFoundError):
                    continue

                if OLD_NAME not in content:
                    continue

                new_content = content.replace(OLD_NAME, NEW_NAME)
                if new_content != content:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    rel = os.path.relpath(filepath, root)
                    print(f"  Patched {rel}")
                    changes += 1

    return changes


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <telegram-ios-root>")
        sys.exit(1)

    root = sys.argv[1]
    build_path = os.path.join(root, "Telegram", "BUILD")

    if not os.path.isfile(build_path):
        print(f"Error: BUILD file not found at {build_path}")
        print("Make sure you're pointing to the Telegram-iOS repo root")
        sys.exit(1)

    print("=== Patching Telegram/BUILD ===")
    patch_build_file(build_path)

    print("\n=== Patching InfoPlist.strings ===")
    patch_info_plist_strings(root)

    print("\n=== Patching AppIntentVocabulary ===")
    patch_intent_vocabulary(root)

    print("\nDone. Run verify_rebrand.sh to check for remaining references.")


if __name__ == "__main__":
    main()
