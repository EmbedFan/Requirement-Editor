#!/usr/bin/env python3
"""
Test the improved file reading with encoding handling.
"""

import os
import sys

# Add libs to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'libs'))

from parse_req_md import ReadMDFile

def test_encoding_fix():
    """Test the encoding fix for ReadMDFile."""
    
    print("🧪 Testing Improved File Reading with Encoding Handling")
    print("=" * 60)
    
    test_file = "test/data/new-2.md"
    
    print(f"📄 Testing file: {test_file}")
    
    # Test the improved ReadMDFile function
    content = ReadMDFile(test_file)
    
    if content:
        print(f"✅ SUCCESS: File read successfully!")
        print(f"📝 Content length: {len(content)} characters")
        print(f"📋 Content preview: {repr(content[:100])}")
        
        # Count lines
        lines = content.split('\n')
        print(f"📄 Number of lines: {len(lines)}")
        
        # Show first few lines
        print(f"📋 First few lines:")
        for i, line in enumerate(lines[:5], 1):
            print(f"   {i}: {repr(line)}")
            
    else:
        print(f"❌ FAILED: Could not read file")
    
    print("=" * 60)

if __name__ == "__main__":
    test_encoding_fix()
