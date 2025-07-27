#!/usr/bin/env python3
"""
Test script for enhanced tab completion functionality
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from libs.terminal_editor import TabCompleter

def test_command_completion():
    """Test command completion functionality."""
    completer = TabCompleter()
    
    print("🧪 Testing Enhanced Tab Completion")
    print("=" * 50)
    
    # Test command completion
    print("\n1. Testing command completion:")
    test_cases = [
        ("", "empty string"),
        ("l", "commands starting with 'l'"),
        ("sa", "commands starting with 'sa'"),
        ("ex", "commands starting with 'ex'"),
        ("h", "commands starting with 'h'"),
        ("qu", "commands starting with 'qu'"),
    ]
    
    for text, description in test_cases:
        matches = completer._complete_command(text)
        print(f"  '{text}' ({description}): {matches}")
    
    # Test mode completion
    print("\n2. Testing mode completion:")
    mode_tests = [
        ("", "all modes"),
        ("c", "modes starting with 'c'"),
        ("f", "modes starting with 'f'"),
    ]
    
    for text, description in mode_tests:
        matches = completer._complete_mode(text)
        print(f"  '{text}' ({description}): {matches}")
    
    # Test item type completion
    print("\n3. Testing item type completion:")
    type_tests = [
        ("", "all types"),
        ("r", "types starting with 'r'"),
        ("c", "types starting with 'c'"),
        ("t", "types starting with 't'"),
    ]
    
    for text, description in type_tests:
        matches = completer._complete_item_type(text)
        print(f"  '{text}' ({description}): {matches}")
    
    # Test add command completion
    print("\n4. Testing add command argument completion:")
    add_tests = [
        (["add"], "position arguments"),
        (["add", "before"], "position arguments starting with 'before'"),
        (["add", "after", "1"], "type arguments"),
        (["add", "under", "2", "r"], "types starting with 'r'"),
    ]
    
    for words, description in add_tests:
        text = words[-1] if len(words) > 1 else ""
        matches = completer._complete_add_args(text, words)
        print(f"  {words} ({description}): {matches}")
    
    print("\n✅ Tab completion tests completed!")

if __name__ == "__main__":
    test_command_completion()
