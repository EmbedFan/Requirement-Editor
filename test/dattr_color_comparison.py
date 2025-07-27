#!/usr/bin/env python3
"""
Visual comparison of DATTR color schemes
"""

import sys
import os
from pathlib import Path

def show_dattr_color_comparison():
    """Show the color scheme change for DATTR styling."""
    print("🎨 DATTR Color Scheme Comparison")
    print("=" * 60)
    
    print("🟢 PREVIOUS (Green Theme):")
    print("""
.dattr {
    background-color: #e8f5e8;     ← Light green background
    border: 2px solid #28a745;     ← Green border
    border-left: 6px solid #28a745; ← Green left border
    color: #155724;                 ← Dark green text
    box-shadow: 0 1px 3px rgba(40, 167, 69, 0.15); ← Green shadow
}
""")

    print("🟡 CURRENT (Orange & Yellow Theme):")
    print("""
.dattr {
    background-color: #fffef5;     ← Very light yellow background
    border: 2px solid #ff8c00;     ← Orange border (DarkOrange)
    border-left: 6px solid #ff8c00; ← Orange left border
    color: #cc6600;                 ← Orange-brown text
    box-shadow: 0 1px 3px rgba(255, 140, 0, 0.15); ← Orange shadow
}
""")

    print("🎯 COLOR SPECIFICATIONS:")
    print("✅ Background: #fffef5 (Very Light Yellow)")
    print("   - Nearly white with a subtle warm yellow tint")
    print("   - Hex breakdown: R=255, G=254, B=245")
    print()
    print("✅ Border: #ff8c00 (DarkOrange)")
    print("   - Pure orange color for strong visibility")
    print("   - Hex breakdown: R=255, G=140, B=0")
    print()
    print("✅ Text: #cc6600 (Orange-Brown)")
    print("   - Darker orange for better readability")
    print("   - Hex breakdown: R=204, G=102, B=0")
    print()
    print("✅ Shadow: rgba(255, 140, 0, 0.15)")
    print("   - Subtle orange shadow with 15% opacity")
    
    print("\n🎨 VISUAL IMPACT:")
    print("• Warm, friendly appearance with yellow/orange scheme")
    print("• High contrast orange borders for clear definition") 
    print("• Professional yet approachable color combination")
    print("• Excellent visibility and readability")
    print("• Consistent with warning/attention color psychology")
    
    print("\n✨ DATTR now has a bright, warm yellow background with orange frame! ✨")

def create_color_swatch_html():
    """Create an HTML file showing the color swatches."""
    html_content = """<!DOCTYPE html>
<html>
<head>
    <title>DATTR Color Swatches</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 20px; }
        .swatch { 
            display: inline-block; 
            width: 100px; 
            height: 100px; 
            margin: 10px; 
            border: 2px solid #333;
            text-align: center;
            line-height: 100px;
            font-weight: bold;
        }
        .bg-light-yellow { background-color: #fffef5; }
        .bg-orange { background-color: #ff8c00; }
        .text-orange-brown { color: #cc6600; }
        .dattr-demo {
            background-color: #fffef5;
            border: 2px solid #ff8c00;
            border-left: 6px solid #ff8c00;
            padding: 8px 12px;
            margin: 10px 0;
            border-radius: 6px;
            font-family: 'Courier New', monospace;
            color: #cc6600;
            font-weight: 900;
            font-size: 0.85em;
            box-shadow: 0 1px 3px rgba(255, 140, 0, 0.15);
            max-width: 600px;
        }
    </style>
</head>
<body>
    <h1>🎨 DATTR Color Scheme</h1>
    
    <h2>Color Swatches:</h2>
    <div class="swatch bg-light-yellow">#fffef5<br>Light Yellow</div>
    <div class="swatch bg-orange" style="color: white;">#ff8c00<br>Orange</div>
    <div class="swatch text-orange-brown" style="background: white;">#cc6600<br>Orange-Brown</div>
    
    <h2>DATTR Preview:</h2>
    <div class="dattr-demo">
        <span style="color: #999;">[2]</span><span style="font-weight: bold;">1031 Dattr:</span> Created at: 2025-07-27 Modified at: 2025-07-27
    </div>
    
    <p><strong>Perfect!</strong> The DATTR field now features a very light yellow background with orange borders.</p>
</body>
</html>"""
    
    output_file = Path(__file__).parent / "data" / "dattr_color_swatches.html"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"\n📄 Color swatch HTML created: {output_file}")
    return output_file

if __name__ == "__main__":
    show_dattr_color_comparison()
    swatch_file = create_color_swatch_html()
    print(f"💡 Open {swatch_file} in a browser to see the color preview!")
