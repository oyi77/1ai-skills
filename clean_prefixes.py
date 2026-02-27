#!/usr/bin/env python3

import re
import sys


def clean_line_prefixes(file_path):
    """Remove corrupted LINE#ID prefixes from file"""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Pattern to match corrupted LINE#ID prefixes at start of lines
    # Matches patterns like "1#RQ|", "2#KM|", etc.
    pattern = r"^\d+#[A-Z]{2}\|"

    # Split into lines, clean each line, then rejoin
    lines = content.split("\n")
    cleaned_lines = []

    for line in lines:
        # Remove the corrupted prefix if it exists
        cleaned_line = re.sub(pattern, "", line)
        cleaned_lines.append(cleaned_line)

    # Join back and write
    cleaned_content = "\n".join(cleaned_lines)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(cleaned_content)

    return True


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python clean_prefixes.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    if clean_line_prefixes(file_path):
        print(f"Successfully cleaned {file_path}")
    else:
        print(f"Failed to clean {file_path}")
