#!/usr/bin/env python3
"""
Test the new DATTR styling - light yellow background with orange borders
"""

import sys
import os
from pathlib import Path

# Add parent directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from libs.parse_req_md import ReadMDFile, ClassifyParts
from libs.gen_html_doc import GenerateHTML

def test_orange_yellow_dattr_styling():
    """Test the new DATTR styling with light yellow background and orange borders."""
    print("🟡 Testing Orange & Yellow DATTR Styling")
    print("=" * 50)
    
    # Test data paths
    test_data_dir = Path(__file__).parent / "data"
    test_input_md = test_data_dir / "test_input.md"
    test_output_html = test_data_dir / "test_dattr_orange_yellow.html"
    
    print(f"Reading markdown file: {test_input_md}")
    
    try:
        # Read and process markdown
        md_content = ReadMDFile(str(test_input_md))
        if not md_content:
            print("❌ Failed to read markdown file")
            return False
        
        print(f"✅ Read {len(md_content)} characters")
        
        # Classify content
        classified_parts = ClassifyParts(md_content)
        if not classified_parts:
            print("❌ Failed to classify content")
            return False
        
        print(f"✅ Classified {len(classified_parts)} parts")
        
        # Find DATTR elements
        dattr_elements = [part for part in classified_parts if part['type'] == 'DATTR']
        print(f"🏷️  Found {len(dattr_elements)} DATTR elements")
        
        # Generate HTML
        html_content = GenerateHTML(classified_parts, "Orange & Yellow DATTR Styling Test")
        if not html_content:
            print("❌ Failed to generate HTML")
            return False
        
        print(f"✅ Generated {len(html_content)} characters of HTML")
        
        # Save to file
        with open(test_output_html, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ Saved HTML to: {test_output_html}")
        
        # Check that new DATTR styling is present
        styling_checks = [
            ("Light yellow background", "background-color: #fffef5"),
            ("Orange border", "border: 2px solid #ff8c00"),
            ("Orange left border", "border-left: 6px solid #ff8c00"),
            ("Orange text color", "color: #cc6600"),
            ("Orange shadow", "rgba(255, 140, 0, 0.15)"),
            ("Print: Light yellow bg", "background-color: #fffef5 !important"),
            ("Print: Orange border", "border: 2px solid #ff8c00 !important")
        ]
        
        print("\n🔍 Checking orange & yellow DATTR styling:")
        all_found = True
        for check_name, check_text in styling_checks:
            if check_text in html_content:
                print(f"   ✅ {check_name}: Found")
            else:
                print(f"   ❌ {check_name}: Missing - {check_text}")
                all_found = False
        
        if all_found:
            print("\n✅ All orange & yellow DATTR styling found!")
            print("🎨 DATTR now features:")
            print("   🟡 Very light yellow background (#fffef5)")
            print("   🟠 Orange border frame (#ff8c00)")
            print("   🟠 Orange text color (#cc6600)")
            print("   🖨️  Print-optimized colors")
        else:
            print("\n⚠️  Some styling updates not found")
        
        return all_found
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_orange_yellow_dattr_styling()
