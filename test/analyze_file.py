#!/usr/bin/env python3
"""
Detailed file analysis for shopping_list_app.md
"""

def analyze_file():
    file_path = "test/real_requirements/shopping_list_app.md"
    
    print("🔍 Detailed File Analysis")
    print("=" * 50)
    
    # Read with different methods
    print("\n1. Reading with different line ending handling:")
    
    # Method 1: Default reading
    with open(file_path, 'r', encoding='utf-8') as f:
        content1 = f.read()
    
    lines1 = content1.split('\n')
    print(f"   Default read: {len(lines1)} lines")
    
    # Method 2: Read lines
    with open(file_path, 'r', encoding='utf-8') as f:
        lines2 = f.readlines()
    
    print(f"   readlines(): {len(lines2)} lines")
    
    # Method 3: Universal newlines
    with open(file_path, 'r', encoding='utf-8', newline=None) as f:
        content3 = f.read()
    
    lines3 = content3.split('\n')
    print(f"   Universal newlines: {len(lines3)} lines")
    
    print("\n2. Line by line analysis:")
    for i, line in enumerate(lines1, 1):
        is_empty = len(line.strip()) == 0
        status = " (EMPTY)" if is_empty else ""
        print(f"   {i:2d}: '{line}'{status}")
    
    print("\n3. Non-empty lines only:")
    non_empty_lines = [line for line in lines1 if line.strip()]
    for i, line in enumerate(non_empty_lines, 1):
        print(f"   {i:2d}: '{line}'")
    
    print(f"\nSummary: {len(non_empty_lines)} non-empty lines out of {len(lines1)} total lines")

if __name__ == "__main__":
    analyze_file()
