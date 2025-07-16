#!/usr/bin/env python3
"""
Ultra minimal test to isolate the exact hanging point
"""

import sys
import os
from pathlib import Path

print("1. Starting minimal test...")

try:
    # Add libs to path
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
    
    # Find the legacy file
    test_dir = Path(__file__).parent
    legacy_file = test_dir / "data" / "test_legacy_simple.md"
    
    print(f"2. File path: {legacy_file}")
    print(f"3. File exists: {legacy_file.exists()}")
    
    # Try basic file reading first
    with open(legacy_file, 'r', encoding='utf-8') as f:
        content = f.read()
    print(f"4. Read {len(content)} characters using basic file I/O")
    
    print("5. Now trying to import ReadMDFile...")
    from libs.parse_req_md import ReadMDFile
    print("6. ReadMDFile imported successfully")
    
    print("7. Calling ReadMDFile...")
    # This is where it might hang
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
