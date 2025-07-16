#!/usr/bin/env python3
"""
Simple test to debug legacy file loading issue
"""

import sys
import os
from pathlib import Path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

print("1. Starting test...")

try:
    # Find the legacy file in the test data directory using pathlib for better path handling
    test_dir = Path(__file__).parent
    legacy_file = test_dir / "data" / "test_legacy_simple.md"
    legacy_file_str = str(legacy_file.resolve())  # Convert to absolute path string
    print(f"2. Looking for file: {legacy_file_str}")
    
    if not legacy_file.exists():
        print(f"❌ File not found: {legacy_file_str}")
        sys.exit(1)
    else:
        print(f"✅ File found: {legacy_file_str}")
    
    print("3. Importing modules...")
    from libs.terminal_editor import TerminalEditor
    from libs.parse_req_md import ReadMDFile, ClassifyParts
    
    print("4. Reading file directly...")
    content = ReadMDFile(legacy_file_str)
    if content:
        print(f"✅ Read {len(content)} characters")
    else:
        print("❌ Failed to read file")
        sys.exit(1)
    
    print("5. Classifying content...")
    parts = ClassifyParts(content)
    if parts:
        print(f"✅ Classified {len(parts)} parts")
    else:
        print("❌ Failed to classify content")
        sys.exit(1)
    
    print("6. Test completed successfully!")
    sys.exit(0)
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
