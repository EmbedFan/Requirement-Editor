#!/usr/bin/env python3
"""
Minimal test to find where the hang occurs
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

print("1. Starting test...")

try:
    # Find the legacy file in the test data directory
    legacy_file = os.path.join(os.path.dirname(__file__), "data", "test_legacy_simple.md")
    print(f"2. Looking for file: {legacy_file}")
    
    if not os.path.exists(legacy_file):
        print(f"❌ File not found: {legacy_file}")
        sys.exit(1)
    else:
        print(f"✅ File found: {legacy_file}")
    
    print("3. Testing file reading...")
    with open(legacy_file, 'r', encoding='utf-8') as f:
        content = f.read()
    print(f"✅ Read {len(content)} characters directly")
    
    print("4. Test completed successfully!")
    sys.exit(0)
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
