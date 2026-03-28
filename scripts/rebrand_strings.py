#!/usr/bin/env python3
"""Replace 'Telegram' with 'Gmall' in all .strings localization files."""

import os
import re
import sys

OLD_NAME = "Telegram"
NEW_NAME = "Gmall"

# Patterns where "Telegram" should NOT be replaced (keep original)
PRESERVE_PATTERNS = [
    r'telegram\.org',
    r'telegram\.me',
    r't\.me',
    r'core\.telegram\.org',
    r'telegram\.dog',
    r'MTProto',
]

# Compound brand terms that need specific replacement
COMPOUND_REPLACEMENTS = [
    ("Telegram Premium", f"{NEW_NAME} Premium"),
    ("Telegram Passport", f"{NEW_NAME} Passport"),
    ("Telegram Stars", f"{NEW_NAME} Stars"),
    ("Telegram Business", f"{NEW_NAME} Business"),
    ("Telegram for iOS", f"{NEW_NAME} for iOS"),
    ("Telegram Messenger", NEW_NAME),
    ("Telegram Support", f"{NEW_NAME} Support"),
    ("Telegram FAQ", f"{NEW_NAME} FAQ"),
    ("Telegram Tips", f"{NEW_NAME} Tips"),
]


def should_preserve(line: str, match_start: int, match_end: int) -> bool:
    """Check if this Telegram occurrence should be kept as-is."""
    context = line[max(0, match_start - 20):match_end + 20]
    for pattern in PRESERVE_PATTERNS:
        if re.search(pattern, context, re.IGNORECASE):
            return True
    return False


def rebrand_strings_file(filepath: str) -> tuple[int, int]:
    """Process a single .strings file. Returns (replacements_made, preserved)."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except (UnicodeDecodeError, FileNotFoundError):
        return 0, 0

    if OLD_NAME not in content:
        return 0, 0

    original = content
    replacements = 0
    preserved = 0

    # .strings format: "key" = "value";
    # Only replace in values, not keys
    def replace_in_value(match):
        nonlocal replacements, preserved
        key = match.group(1)
        value = match.group(2)

        new_value = value
        # Apply compound replacements first (more specific)
        for old, new in COMPOUND_REPLACEMENTS:
            if old in new_value:
                new_value = new_value.replace(old, new)

        # Then do generic replacement for remaining instances
        remaining_positions = [m.start() for m in re.finditer(re.escape(OLD_NAME), new_value)]
        if remaining_positions:
            result = []
            last_end = 0
            for m in re.finditer(re.escape(OLD_NAME), new_value):
                if should_preserve(new_value, m.start(), m.end()):
                    result.append(new_value[last_end:m.end()])
                    preserved += 1
                else:
                    result.append(new_value[last_end:m.start()] + NEW_NAME)
                    replacements += 1
                last_end = m.end()
            result.append(new_value[last_end:])
            new_value = ''.join(result)

        if new_value != value:
            replacements += 1
        return f'"{key}" = "{new_value}";'

    content = re.sub(
        r'"([^"]*?)"\s*=\s*"([^"]*?)";',
        replace_in_value,
        content
    )

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

    return replacements, preserved


def find_strings_files(root_dir: str) -> list[str]:
    """Find all .strings files recursively."""
    results = []
    for dirpath, _, filenames in os.walk(root_dir):
        for fname in filenames:
            if fname.endswith('.strings'):
                results.append(os.path.join(dirpath, fname))
    return results


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <telegram-ios-root>")
        sys.exit(1)

    root = sys.argv[1]
    if not os.path.isdir(root):
        print(f"Error: {root} is not a directory")
        sys.exit(1)

    files = find_strings_files(root)
    print(f"Found {len(files)} .strings files")

    total_replaced = 0
    total_preserved = 0
    modified_files = 0

    for filepath in sorted(files):
        replaced, preserved = rebrand_strings_file(filepath)
        if replaced > 0:
            rel = os.path.relpath(filepath, root)
            print(f"  Modified: {rel} ({replaced} replacements, {preserved} preserved)")
            modified_files += 1
        total_replaced += replaced
        total_preserved += preserved

    print(f"\nDone: {total_replaced} replacements in {modified_files} files, {total_preserved} preserved")


if __name__ == "__main__":
    main()
