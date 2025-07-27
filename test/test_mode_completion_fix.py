#!/usr/bin/env python3
"""
Quick test to verify mode completion fix
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from libs.terminal_editor import TabCompleter

def test_mode_fix():
    """Test that mode completion only returns valid modes."""
    completer = TabCompleter()
    
    print("🔧 Testing Mode Completion Fix")
    print("=" * 40)
    
    # Test all mode completions
    all_modes = completer._complete_mode("")
    print(f"All available modes: {all_modes}")
    
    # Verify only valid modes are included
    valid_modes = ['compact', 'full']
    invalid_modes = ['detailed']
    
    print(f"✅ Expected valid modes: {valid_modes}")
    print(f"❌ Invalid modes that should NOT appear: {invalid_modes}")
    
    # Check results
    all_correct = True
    for mode in all_modes:
        if mode in valid_modes:
            print(f"✅ '{mode}' - VALID")
        elif mode in invalid_modes:
            print(f"❌ '{mode}' - INVALID (should not appear!)")
            all_correct = False
        else:
            print(f"⚠️  '{mode}' - UNKNOWN mode")
            all_correct = False
    
    # Check that all valid modes are present
    for mode in valid_modes:
        if mode not in all_modes:
            print(f"❌ Missing valid mode: '{mode}'")
            all_correct = False
    
    print("\n" + "=" * 40)
    if all_correct:
        print("✅ Mode completion fix SUCCESSFUL!")
        print("   Only valid modes (compact, full) are available for tab completion.")
    else:
        print("❌ Mode completion fix FAILED!")
        print("   Invalid or missing modes detected.")
    
    return all_correct

if __name__ == "__main__":
    test_mode_fix()
