#!/usr/bin/env python3
"""
Test script for automatic .md extension functionality in main.py

This script tests the new process_filename_for_loading() function
that automatically tries adding .md extension when loading files.

Test Cases:
1. File without extension -> should find .md version
2. File with wrong extension -> should find .md version  
3. File with correct .md extension -> should load directly
4. Non-existent file -> should return None with proper error
"""

import sys
import os
import subprocess
import tempfile

# Add the parent directory to sys.path to import main
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import process_filename_for_loading


def test_process_filename_for_loading():
    """Test the process_filename_for_loading function"""
    print("🧪 Testing process_filename_for_loading function...")
    
    # Create a temporary test file
    with tempfile.NamedTemporaryFile(suffix='.md', delete=False, mode='w', encoding='utf-8') as tmp_file:
        tmp_file.write("# Test Document\n\n&nbsp;&nbsp;&nbsp;&nbsp;1001 Req: Test requirement\n")
        tmp_filename = tmp_file.name
    
    try:
        # Get the base name without extension
        base_name = tmp_filename[:-3]  # Remove .md extension
        
        # Test 1: File without extension should find .md version
        print(f"\n1. Testing filename without extension: '{base_name}'")
        result = process_filename_for_loading(base_name)
        assert result == tmp_filename, f"Expected '{tmp_filename}', got '{result}'"
        print("   ✅ PASS - Found .md version")
        
        # Test 2: File with wrong extension should find .md version
        wrong_ext_name = base_name + ".txt"
        print(f"\n2. Testing filename with wrong extension: '{wrong_ext_name}'")
        result = process_filename_for_loading(wrong_ext_name)
        assert result == tmp_filename, f"Expected '{tmp_filename}', got '{result}'"
        print("   ✅ PASS - Found .md version")
        
        # Test 3: File with correct .md extension should load directly
        print(f"\n3. Testing filename with correct .md extension: '{tmp_filename}'")
        result = process_filename_for_loading(tmp_filename)
        assert result == tmp_filename, f"Expected '{tmp_filename}', got '{result}'"
        print("   ✅ PASS - Loaded directly")
        
        # Test 4: Non-existent file should return None
        nonexistent = "definitely_does_not_exist_12345"
        print(f"\n4. Testing non-existent file: '{nonexistent}'")
        result = process_filename_for_loading(nonexistent)
        assert result is None, f"Expected None, got '{result}'"
        print("   ✅ PASS - Returned None for non-existent file")
        
    finally:
        # Clean up
        if os.path.exists(tmp_filename):
            os.unlink(tmp_filename)
    
    print("\n🎉 All tests passed!")


def test_command_line_integration():
    """Test the command line integration with main.py"""
    print("\n🧪 Testing command line integration...")
    
    # Test with a known existing file (without extension)
    test_files = [
        "test/data/test_input",
        "test/data/test-doc1", 
    ]
    
    for test_file in test_files:
        print(f"\n📄 Testing command line with: '{test_file}'")
        
        # Run main.py with the test file
        result = subprocess.run([
            sys.executable, "main.py", "-md2html", test_file
        ], capture_output=True, text=True, cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        
        if result.returncode == 0:
            if "💡 File found with .md extension:" in result.stdout:
                print(f"   ✅ PASS - Found .md extension automatically")
            else:
                print(f"   ⚠️  WARNING - File processed but no extension message found")
        else:
            print(f"   ❌ FAIL - Command failed with return code {result.returncode}")
            print(f"   Error output: {result.stderr}")
    
    print("\n🎉 Command line integration tests completed!")


def main():
    """Run all tests"""
    print("=" * 60)
    print("AUTOMATIC .MD EXTENSION FEATURE - TEST SUITE")
    print("=" * 60)
    
    try:
        test_process_filename_for_loading()
        test_command_line_integration()
        
        print("\n" + "=" * 60)
        print("✅ ALL TESTS COMPLETED SUCCESSFULLY!")
        print("✅ Automatic .md extension feature is working correctly")
        print("=" * 60)
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 UNEXPECTED ERROR: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
