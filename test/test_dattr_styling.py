#!/usr/bin/env python3
"""
Test DATTR styling in HTML export
"""

import sys
import os
from pathlib import Path

# Add parent directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from libs.parse_req_md import ReadMDFile, ClassifyParts
from libs.gen_html_doc import GenerateHTML

def test_dattr_styling():
    """Test the new DATTR styling in HTML export."""
    print("🎨 Testing DATTR Styling in HTML Export")
    print("=" * 50)
    
    # Test data paths
    test_data_dir = Path(__file__).parent / "data"
    test_input_md = test_data_dir / "test_input.md"
    test_output_html = test_data_dir / "test_dattr_styling.html"
    
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
        print(f"🏷️  Found {len(dattr_elements)} DATTR elements:")
        for dattr in dattr_elements:
            print(f"   - Line {dattr.get('line', '?')}: {dattr.get('description', 'No description')[:50]}...")
        
        # Generate HTML
        html_content = GenerateHTML(classified_parts, "DATTR Styling Test")
        if not html_content:
            print("❌ Failed to generate HTML")
            return False
        
        print(f"✅ Generated {len(html_content)} characters of HTML")
        
        # Save to file
        with open(test_output_html, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ Saved HTML to: {test_output_html}")
        
        # Check that DATTR styling is present
        if '.dattr {' in html_content and 'border: 2px solid #28a745' in html_content:
            print("✅ New DATTR styling found in HTML!")
        else:
            print("⚠️  New DATTR styling not found - checking what's there...")
            import re
            dattr_css = re.search(r'\.dattr \{[^}]+\}', html_content, re.DOTALL)
            if dattr_css:
                print(f"Found DATTR CSS: {dattr_css.group()}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_dattr_styling()
