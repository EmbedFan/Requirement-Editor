#!/usr/bin/env python3
"""
Final validation of orange & yellow DATTR styling
"""

import sys
import os
from pathlib import Path

def validate_orange_yellow_dattr():
    """Validate the complete orange & yellow DATTR implementation."""
    print("🔍 Final Validation: Orange & Yellow DATTR")
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
    
    # Comprehensive validation checks
    validation_checks = [
        # Screen CSS
        ("Light yellow background", "#fffef5", "screen"),
        ("Orange border", "#ff8c00", "screen"),
        ("Orange text color", "#cc6600", "screen"),
        ("Orange shadow", "rgba(255, 140, 0, 0.15)", "screen"),
        
        # Print CSS
        ("Print: Light yellow bg", "background-color: #fffef5 !important", "print"),
        ("Print: Orange border", "border: 2px solid #ff8c00 !important", "print"),
        ("Print: Orange left border", "border-left: 6px solid #ff8c00 !important", "print"),
        
        # Font styling maintained
        ("Small font size", "font-size: 0.85em", "font"),
        ("Bold font weight", "font-weight: 900", "font"),
        ("Monospace font", "'Courier New', monospace", "font"),
        
        # Layout maintained
        ("Compact padding", "padding: 8px 12px", "layout"),
        ("Tight margins", "margin: 10px 0", "layout"),
        ("Sharp corners", "border-radius: 6px", "layout"),
        
        # DATTR element present
        ("DATTR element", "1031 Dattr:", "content"),
        ("DATTR CSS class", 'class="dattr', "content")
    ]
    
    print("\n🔍 Comprehensive validation:")
    all_passed = True
    categories = {}
    
    for check_name, check_text, category in validation_checks:
        found = check_text in html_content
        if category not in categories:
            categories[category] = []
        
        if found:
            categories[category].append(f"✅ {check_name}")
        else:
            categories[category].append(f"❌ {check_name}")
            all_passed = False
    
    # Display results by category
    for category, results in categories.items():
        print(f"\n📂 {category.upper()}:")
        for result in results:
            print(f"   {result}")
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 COMPLETE SUCCESS!")
        print("✅ Orange & Yellow DATTR styling fully implemented!")
        print()
        print("🎨 Summary of changes:")
        print("   🟡 Background: Very light yellow (#fffef5)")
        print("   🟠 Border: Orange frame (#ff8c00)")
        print("   🟠 Text: Orange-brown color (#cc6600)")
        print("   📝 Font: Small (0.85em) and extra bold (900)")
        print("   📐 Layout: Compact padding and margins")
        print("   🖨️  Print: Optimized for PDF output")
        print()
        print("🎯 The DATTR field now perfectly matches your requirements:")
        print("   • Very light yellow background")
        print("   • Orange border frame")
        print("   • Maintained compact, solid appearance")
    else:
        print("❌ Some validation checks failed")
    
    return all_passed

if __name__ == "__main__":
    validate_orange_yellow_dattr()
