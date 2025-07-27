#!/usr/bin/env python3
"""
Debug script for shopping_list_app.md loading issue.
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from libs.parse_req_md import ReadMDFile, ClassifyParts

def debug_shopping_list_app():
    """Debug the shopping list app loading issue."""
    print("🔍 Debugging shopping_list_app.md loading issue")
    print("=" * 60)
    
    file_path = "test/real_requirements/shopping_list_app.md"
    
    # Step 1: Read the raw file
    print("\n1. Reading raw file content:")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            raw_content = f.read()
        
        lines = raw_content.split('\n')
        print(f"   Total lines in file: {len(lines)}")
        print("   Raw content:")
        for i, line in enumerate(lines, 1):
            print(f"   {i:2d}: '{line}'")
        
    except Exception as e:
        print(f"   ❌ Error reading file: {e}")
        return
    
    # Step 2: Use the ReadMDFile function
    print("\n2. Using ReadMDFile function:")
    try:
        md_content = ReadMDFile(file_path)
        if md_content:
            md_lines = md_content.split('\n')
            print(f"   ReadMDFile returned {len(md_lines)} lines")
            print("   Processed content:")
            for i, line in enumerate(md_lines, 1):
                print(f"   {i:2d}: '{line}'")
        else:
            print("   ❌ ReadMDFile returned None or empty")
    except Exception as e:
        print(f"   ❌ Error in ReadMDFile: {e}")
        return
    
    # Step 3: Use ClassifyParts
    print("\n3. Using ClassifyParts function:")
    try:
        classified_parts = ClassifyParts(md_content)
        print(f"   ClassifyParts returned {len(classified_parts)} parts")
        
        for i, part in enumerate(classified_parts, 1):
            print(f"   {i:2d}: Type={part['type']:<10} Indent={part['indent']} Description='{part['description'][:50]}{'...' if len(part['description']) > 50 else ''}'")
            if 'id' in part:
                print(f"       ID='{part['id']}'")
                
    except Exception as e:
        print(f"   ❌ Error in ClassifyParts: {e}")
        return
    
    # Step 4: Test with terminal editor
    print("\n4. Testing with TerminalEditor:")
    try:
        from libs.terminal_editor import TerminalEditor
        from libs.md_edit import MarkdownEditor
        
        # Create markdown editor and load the file
        md_editor = MarkdownEditor(classified_parts)  # Pass the classified parts
        
        parts = md_editor.get_classified_parts()
        print(f"   MarkdownEditor has {len(parts)} parts")
        
        # Display like the terminal editor would
        for i, part in enumerate(parts, 1):
            indent_display = "  " * part['indent']
            type_display = f"[{part['type']}]"
            id_part = f" {part.get('id', '')}" if part.get('id') else ""
            desc = part['description']
            print(f"   {i:2d}│{indent_display}{type_display}{id_part} {desc}")
            
    except Exception as e:
        print(f"   ❌ Error testing with TerminalEditor: {e}")

if __name__ == "__main__":
    debug_shopping_list_app()
