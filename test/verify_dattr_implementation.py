#!/usr/bin/env python3
"""
Verify DATTR field appears as green bordered block before first comment
"""

import sys
import os
from pathlib import Path

# Add parent directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def verify_dattr_implementation():
    """Verify that DATTR field is properly implemented with green border."""
    print("🔍 Verifying DATTR Implementation")
    print("=" * 50)
    
    # Check the generated HTML file
    test_html_file = Path(__file__).parent / "data" / "test_input.html"
    
    if not test_html_file.exists():
        print("❌ Test HTML file not found")
        return False
    
    print(f"✅ Found test HTML file: {test_html_file}")
    
    # Read the HTML content
    with open(test_html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Check 1: DATTR CSS styling with green border
    checks = [
        ("Green border styling", "border: 2px solid #28a745"),
        ("Green background", "background-color: #e8f5e8"),
        ("Green border left", "border-left: 6px solid #28a745"),
        ("Box shadow", "box-shadow: 0 2px 4px rgba(40, 167, 69, 0.1)"),
        ("DATTR content", "1031 Dattr:"),
        ("DATTR element", '<div class="dattr indent-1'),
        ("Comment after DATTR", "1030 Comm:")
    ]
    
    print("\n🎨 Checking DATTR styling...")
    all_passed = True
    
    for check_name, check_text in checks:
        if check_text in html_content:
            print(f"   ✅ {check_name}: Found")
        else:
            print(f"   ❌ {check_name}: Missing")
            all_passed = False
    
    # Check 2: DATTR appears before first comment
    print("\n📍 Checking DATTR positioning...")
    
    dattr_pos = html_content.find('1031 Dattr:')
    comment_pos = html_content.find('1030 Comm:')
    
    if dattr_pos != -1 and comment_pos != -1:
        if dattr_pos < comment_pos:
            print("   ✅ DATTR appears before first comment")
        else:
            print("   ❌ DATTR does not appear before first comment")
            all_passed = False
    else:
        print("   ❌ Could not find DATTR or comment positions")
        all_passed = False
    
    # Check 3: Print media styling
    print("\n🖨️  Checking print media styling...")
    print_media_checks = [
        "background-color: #e8f5e8 !important",
        "border: 2px solid #28a745 !important", 
        "border-left: 6px solid #28a745 !important"
    ]
    
    for check in print_media_checks:
        if check in html_content:
            print(f"   ✅ Print media: {check[:40]}...")
        else:
            print(f"   ❌ Print media missing: {check[:40]}...")
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 SUCCESS: DATTR field is properly implemented!")
        print("   ✅ Green bordered block styling")
        print("   ✅ Positioned before first comment")  
        print("   ✅ Print-optimized styling")
        print("\n💡 The DATTR field now appears as a prominent green bordered")
        print("   block containing document metadata (creation/modification dates)")
    else:
        print("❌ IMPLEMENTATION INCOMPLETE: Some checks failed")
    
    return all_passed

if __name__ == "__main__":
    verify_dattr_implementation()
