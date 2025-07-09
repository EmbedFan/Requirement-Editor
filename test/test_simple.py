#!/usr/bin/env python3
"""
Simple Test Suite for Demonstration

This script contains basic tests that will pass to demonstrate 
the HTML report generation functionality.

Author: Attila Gallai <attila@tux-net.hu>
License: MIT License (see LICENSE.txt)
"""

import os
import sys
import time

# Add parent directory to Python path to access libs
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from libs.project import create_project_config


def test_basic_functionality():
    """Test basic functionality that should always pass."""
    
    print("Running Basic Functionality Tests")
    print("=" * 50)
    
    # Test 1: Simple math
    print("\nTest 1: Basic Math Operations")
    assert 2 + 2 == 4, "Basic addition failed"
    assert 5 * 3 == 15, "Basic multiplication failed"
    print("✓ Math operations working correctly")
    
    # Test 2: String operations
    print("\nTest 2: String Operations")
    test_string = "Hello, World!"
    assert len(test_string) == 13, "String length incorrect"
    assert test_string.upper() == "HELLO, WORLD!", "String upper() failed"
    print("✓ String operations working correctly")
    
    # Test 3: List operations
    print("\nTest 3: List Operations")
    test_list = [1, 2, 3, 4, 5]
    assert len(test_list) == 5, "List length incorrect"
    assert sum(test_list) == 15, "List sum incorrect"
    print("✓ List operations working correctly")
    
    print("\n" + "=" * 50)
    print("All basic functionality tests PASSED!")


def test_file_operations():
    """Test file system operations."""
    
    print("\nRunning File Operations Tests")
    print("=" * 50)
    
    # Test 1: Check if current directory exists
    print("\nTest 1: Directory Operations")
    current_dir = os.getcwd()
    assert os.path.exists(current_dir), "Current directory doesn't exist"
    assert os.path.isdir(current_dir), "Current directory is not a directory"
    print(f"✓ Current directory exists: {current_dir}")
    
    # Test 2: Check parent directory structure
    print("\nTest 2: Parent Directory Structure")
    parent_dir = os.path.dirname(__file__)
    assert os.path.exists(parent_dir), "Parent directory doesn't exist"
    print(f"✓ Parent directory exists: {parent_dir}")
    
    print("\n" + "=" * 50)
    print("All file operation tests PASSED!")


def test_module_imports():
    """Test that required modules can be imported."""
    
    print("\nRunning Module Import Tests")
    print("=" * 50)
    
    # Test 1: Standard library imports
    print("\nTest 1: Standard Library Imports")
    try:
        import json
        import datetime
        import pathlib
        print("✓ Standard library modules imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import standard library: {e}")
        raise
    
    # Test 2: Project module imports
    print("\nTest 2: Project Module Imports")
    try:
        from libs import parse_req_md
        from libs import gen_html_doc
        from libs import project
        print("✓ Project modules imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import project modules: {e}")
        raise
        
    print("\n" + "=" * 50)
    print("All module import tests PASSED!")


def test_performance_metrics():
    """Test performance and timing."""
    
    print("\nRunning Performance Tests")
    print("=" * 50)
    
    # Test 1: Simple loop performance
    print("\nTest 1: Loop Performance")
    start_time = time.time()
    
    result = 0
    for i in range(100000):
        result += i
    
    end_time = time.time()
    duration = end_time - start_time
    
    expected_result = sum(range(100000))
    assert result == expected_result, f"Loop calculation incorrect: {result} != {expected_result}"
    assert duration < 1.0, f"Loop took too long: {duration}s"
    
    print(f"✓ Loop completed in {duration:.4f} seconds")
    print(f"✓ Result: {result:,}")
    
    print("\n" + "=" * 50)
    print("All performance tests PASSED!")


if __name__ == "__main__":
    print("🧪 Starting Simple Test Suite")
    print("=" * 70)
    
    try:
        # Run all test functions
        test_basic_functionality()
        test_file_operations()
        test_module_imports()
        test_performance_metrics()
        
        print("\n" + "=" * 70)
        print("🎉 ALL TESTS COMPLETED SUCCESSFULLY!")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        print("=" * 70)
        sys.exit(1)
