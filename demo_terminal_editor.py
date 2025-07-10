#!/usr/bin/env python3
"""
Demo script for the terminal editor functionality.

This script demonstrates how to use the terminal editor with
the -ed parameter and shows some basic commands.
"""

import os
import sys

print("🚀 Requirement Editor Terminal Interface Demo")
print("=" * 60)
print()

# Check if we have the test file
test_file = "test/data/test_input.md"
if os.path.exists(test_file):
    print(f"✅ Test file found: {test_file}")
    print()
    print("To start the terminal editor with this file, run:")
    print(f"  python main.py -ed {test_file}")
else:
    print(f"⚠️  Test file not found: {test_file}")
    print()
    print("To start the terminal editor with a new document, run:")
    print(f"  python main.py -ed")

print()
print("📚 Terminal Editor Commands Overview:")
print()
print("📁 File Operations:")
print("  new                    - Create new document")
print("  load <file>            - Load markdown file")
print("  save                   - Save current document")
print("  export <file>          - Export to HTML")
print()
print("✏️ Editing Commands:")
print("  add after 1 REQUIREMENT 'New requirement description'")
print("  add under 2 COMMENT 'This is a comment'")
print("  move 3 after 5")
print("  edit 4 'Updated description'")
print("  delete 6")
print()
print("🔍 Navigation:")
print("  list                   - Show document")
print("  find 'search text'     - Search descriptions")
print("  findid 1001            - Find by ID")
print("  goto 5                 - Show line info")
print()
print("❓ Help:")
print("  help                   - Show all commands")
print("  quit                   - Exit editor")
print()
print("💡 Ready to start? Run:")
print("    python main.py -ed")
