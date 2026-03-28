#!/usr/bin/env python3
"""Scan Swift source files for hardcoded 'Telegram' strings and generate a report."""

import os
import re
import sys

OLD_NAME = "Telegram"

# Patterns that are expected/acceptable (not user-visible or technical references)
ACCEPTABLE_PATTERNS = [
    r'telegram\.org',
    r'telegram\.me',
    r't\.me',
    r'core\.telegram\.org',
    r'TelegramCore',
    r'TelegramUI',
    r'TelegramApi',
    r'TelegramPresentationData',
    r'TelegramCallsUI',
    r'TelegramVoip',
    r'TelegramStringFormatting',
    r'TelegramBaseController',
    r'TelegramNotices',
    r'TelegramAudio',
    r'TelegramMediaResources',
    r'TelegramUniversalVideoContent',
    r'TelegramAnimatedStickerNode',
    r'import\s+Telegram',
    r'@testable\s+import',
    r'MTProto',
    r'//.*Telegram',       # Comments
    r'\/\*.*Telegram',     # Block comments
    r'#if.*Telegram',      # Preprocessor
]

# These are likely user-visible and need fixing
HIGH_PRIORITY_PATTERNS = [
    r'"[^"]*Telegram[^"]*"',           # String literals containing "Telegram"
    r'NSLocalizedString.*Telegram',     # Localized strings
    r'text\s*=\s*"[^"]*Telegram',      # UI text assignment
    r'title\s*=\s*"[^"]*Telegram',     # Title assignment
    r'message\s*=\s*"[^"]*Telegram',   # Message assignment
]


def is_acceptable(line: str) -> bool:
    """Check if this line's Telegram reference is an acceptable module/technical name."""
    for pattern in ACCEPTABLE_PATTERNS:
        if re.search(pattern, line):
            return True
    return False


def is_high_priority(line: str) -> bool:
    """Check if this line likely contains a user-visible Telegram reference."""
    for pattern in HIGH_PRIORITY_PATTERNS:
        if re.search(pattern, line):
            return True
    return False


def scan_file(filepath: str) -> list[dict]:
    """Scan a Swift file for Telegram references. Returns list of findings."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except (UnicodeDecodeError, FileNotFoundError):
        return []

    findings = []
    for i, line in enumerate(lines, 1):
        if OLD_NAME in line:
            if is_acceptable(line):
                continue
            findings.append({
                'line': i,
                'content': line.rstrip(),
                'priority': 'HIGH' if is_high_priority(line) else 'LOW',
            })

    return findings


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <telegram-ios-root>")
        sys.exit(1)

    root = sys.argv[1]
    if not os.path.isdir(root):
        print(f"Error: {root} is not a directory")
        sys.exit(1)

    # Find all Swift files
    swift_files = []
    for dirpath, _, filenames in os.walk(root):
        for fname in filenames:
            if fname.endswith('.swift'):
                swift_files.append(os.path.join(dirpath, fname))

    print(f"Scanning {len(swift_files)} Swift files for hardcoded 'Telegram' references...\n")

    high_priority = []
    low_priority = []

    for filepath in sorted(swift_files):
        findings = scan_file(filepath)
        for f in findings:
            f['file'] = os.path.relpath(filepath, root)
            if f['priority'] == 'HIGH':
                high_priority.append(f)
            else:
                low_priority.append(f)

    # Report
    print(f"{'='*60}")
    print(f"HIGH PRIORITY — Likely user-visible strings ({len(high_priority)} found)")
    print(f"{'='*60}")
    for f in high_priority:
        print(f"\n  {f['file']}:{f['line']}")
        print(f"    {f['content']}")

    print(f"\n{'='*60}")
    print(f"LOW PRIORITY — May be internal/code references ({len(low_priority)} found)")
    print(f"{'='*60}")
    for f in low_priority[:50]:  # Show first 50
        print(f"\n  {f['file']}:{f['line']}")
        print(f"    {f['content']}")

    if len(low_priority) > 50:
        print(f"\n  ... and {len(low_priority) - 50} more low-priority items")

    # Write full report to file
    report_path = os.path.join(root, "gmall_rebrand_report.txt")
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(f"Gmall Rebrand Report\n")
        f.write(f"{'='*60}\n\n")
        f.write(f"HIGH PRIORITY: {len(high_priority)}\n")
        f.write(f"LOW PRIORITY: {len(low_priority)}\n\n")

        f.write(f"HIGH PRIORITY ITEMS\n{'-'*40}\n")
        for item in high_priority:
            f.write(f"{item['file']}:{item['line']}\n")
            f.write(f"  {item['content']}\n\n")

        f.write(f"\nLOW PRIORITY ITEMS\n{'-'*40}\n")
        for item in low_priority:
            f.write(f"{item['file']}:{item['line']}\n")
            f.write(f"  {item['content']}\n\n")

    print(f"\n\nFull report written to: {report_path}")
    print(f"\nSummary: {len(high_priority)} high-priority, {len(low_priority)} low-priority references")


if __name__ == "__main__":
    main()
