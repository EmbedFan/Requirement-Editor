#!/usr/bin/env python3
"""
Test the updated DATTR styling - smaller and more solid fonts
"""

import sys
import os
from pathlib import Path

# Add parent directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from libs.parse_req_md import ReadMDFile, ClassifyParts
from libs.gen_html_doc import GenerateHTML

def test_updated_dattr_styling():
    """Test the updated DATTR styling with smaller and more solid fonts."""
    print("🎨 Testing Updated DATTR Styling")
    print("=" * 50)
    
    # Test data paths
    test_data_dir = Path(__file__).parent / "data"
    test_input_md = test_data_dir / "test_input.md"
    test_output_html = test_data_dir / "test_dattr_updated_styling.html"
    
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
        html_content = GenerateHTML(classified_parts, "Updated DATTR Styling Test")
        if not html_content:
            print("❌ Failed to generate HTML")
            return False
        
        print(f"✅ Generated {len(html_content)} characters of HTML")
        
        # Save to file
        with open(test_output_html, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ Saved HTML to: {test_output_html}")
        
        # Check that updated DATTR styling is present
        styling_checks = [
            ("Smaller font size", "font-size: 0.85em"),
            ("More solid font weight", "font-weight: 900"),
            ("Reduced padding", "padding: 8px 12px"),
            ("Reduced margin", "margin: 10px 0"),
            ("Smaller border radius", "border-radius: 6px"),
            ("Subtle shadow", "box-shadow: 0 1px 3px")
        ]
        
        print("\n🔍 Checking updated DATTR styling:")
        all_found = True
        for check_name, check_text in styling_checks:
            if check_text in html_content:
                print(f"   ✅ {check_name}: {check_text}")
            else:
                print(f"   ❌ {check_name}: Missing - {check_text}")
                all_found = False
        
        if all_found:
            print("\n✅ All updated DATTR styling found!")
            print("🎯 DATTR now has:")
            print("   • Smaller font size (0.85em)")
            print("   • More solid font weight (900)")
            print("   • Compact padding and margins")
            print("   • Subtle styling for a professional look")
        else:
            print("\n⚠️  Some styling updates not found")
        
        return all_found
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_updated_dattr_styling()
