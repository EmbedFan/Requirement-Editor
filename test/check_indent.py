#!/usr/bin/env python3
"""
Simple indentation check for shopping_list_app.md
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from libs.parse_req_md import ReadMDFile, ClassifyParts

def check_indentation():
    file_path = "test/real_requirements/shopping_list_app.md"
    
    print("Indentation Analysis")
    print("===================")
    
    try:
        md_content = ReadMDFile(file_path)
        classified_parts = ClassifyParts(md_content)
        
        print(f"Found {len(classified_parts)} parts:")
        print()
        
        for i, part in enumerate(classified_parts, 1):
            indent_str = "  " * part['indent']
            type_str = part['type'] or 'UNKNOWN'
            id_str = str(part.get('id', 'None'))
            desc = part['description'][:60] + "..." if len(part['description']) > 60 else part['description']
            
            print(f"{i:2d}. Indent:{part['indent']} Type:{type_str:<10} ID:{id_str:<4} Desc:'{desc}'")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_indentation()
