#!/usr/bin/env python3
"""
Test the three originally failing tests
"""

import os
import subprocess
import sys
from pathlib import Path

# Set UTF-8 encoding for all subprocess operations
os.environ['PYTHONIOENCODING'] = 'utf-8'
os.environ['PYTHONUTF8'] = '1'

def test_fixed_tests():
    """Test the three originally failing tests that we just fixed."""
    
    test_dir = Path(__file__).parent
    
    failed_tests = [
        "test_line_numbers.py",
        "test_witheditor.py", 
        "test_witheditor_integration.py"
    ]
    
    print("🧪 Testing Previously Failed Tests")
    print("=" * 50)
    
    results = {}
    
    for test_file in failed_tests:
        test_path = test_dir / test_file
        print(f"\nRunning: {test_file}")
        print("-" * 30)
        
        # Set up UTF-8 environment
        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'utf-8'
        env['PYTHONUTF8'] = '1'
        
        try:
            result = subprocess.run(
                [sys.executable, str(test_path)],
                capture_output=True,
                text=True,
                cwd=test_path.parent,
                timeout=30,
                env=env,
                encoding='utf-8'
            )
            
            if result.returncode == 0:
                print(f"✅ PASSED: {test_file}")
                results[test_file] = "PASSED"
            else:
                print(f"❌ FAILED: {test_file} (exit code: {result.returncode})")
                print("STDERR:", result.stderr[-200:])  # Last 200 chars
                results[test_file] = "FAILED"
                
        except subprocess.TimeoutExpired:
            print(f"⏰ TIMEOUT: {test_file}")
            results[test_file] = "TIMEOUT"
        except Exception as e:
            print(f"💥 ERROR: {test_file} - {e}")
            results[test_file] = "ERROR"
    
    print("\n" + "=" * 50)
    print("SUMMARY")
    print("=" * 50)
    
    passed = 0
    for test_file, status in results.items():
        status_icon = "✅" if status == "PASSED" else "❌"
        print(f"{status_icon} {test_file}: {status}")
        if status == "PASSED":
            passed += 1
    
    print(f"\nResult: {passed}/{len(failed_tests)} tests passed")
    
    if passed == len(failed_tests):
        print("🎉 All previously failing tests are now working!")
        return True
    else:
        print("⚠️  Some tests still need attention")
        return False


if __name__ == "__main__":
    success = test_fixed_tests()
    sys.exit(0 if success else 1)
