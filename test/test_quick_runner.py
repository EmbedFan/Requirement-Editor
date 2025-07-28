#!/usr/bin/env python3
"""
Quick Test Runner - Limited Version

Runs only a few simple tests to verify the enhanced logging functionality.
"""

import os
import sys
import subprocess
import time
from pathlib import Path
from datetime import datetime

# Set UTF-8 encoding for all subprocess operations
os.environ['PYTHONIOENCODING'] = 'utf-8'
os.environ['PYTHONUTF8'] = '1'

# Import the HTML report generator
from test_reporter import TestReportGenerator


def discover_and_run_limited_tests(reporter):
    """Run only a small subset of tests for quick verification."""
    
    test_dir = Path(__file__).parent
    
    # Limited list of simple tests
    test_files = [
        "test_simple.py",
        "test_simple_aliases.py", 
        "test_id_fix.py"
    ]
    
    failed_tests = []
    
    print(f"Quick Test Runner - Limited Edition")
    print("=" * 60)
    print(f"Test directory: {test_dir}")
    print(f"Running {len(test_files)} selected tests:")
    for test_file in test_files:
        print(f"  - {test_file}")
    print("=" * 60)
    
    for test_file in test_files:
        test_path = test_dir / test_file
        
        if not test_path.exists():
            print(f"⚠ SKIPPED: {test_file} (not found)")
            continue
            
        print(f"Running: {test_file}")
        print("=" * 60)
        
        start_time = time.time()
        
        # Set up UTF-8 environment
        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'utf-8'
        env['PYTHONUTF8'] = '1'
        
        try:
            # Run the test
            result = subprocess.run(
                [sys.executable, str(test_path)],
                capture_output=True,
                text=True,
                cwd=test_path.parent,
                timeout=30,
                env=env,
                encoding='utf-8'
            )
            
            duration = time.time() - start_time
            
            if result.returncode == 0:
                print(f"✓ PASSED: {test_file}")
                reporter.add_test(
                    test_name=test_file,
                    status="PASSED",
                    duration=duration,
                    output=result.stdout,
                    error="",
                    details={}
                )
            else:
                print(f"✗ FAILED: {test_file} (exit code: {result.returncode})")
                failed_tests.append(test_file)
                reporter.add_test(
                    test_name=test_file,
                    status="FAILED", 
                    duration=duration,
                    output=result.stdout,
                    error=result.stderr,
                    details={"exit_code": result.returncode}
                )
                
        except subprocess.TimeoutExpired:
            duration = time.time() - start_time
            print(f"⏰ TIMEOUT: {test_file}")
            failed_tests.append(test_file)
            reporter.add_test(
                test_name=test_file,
                status="ERROR",
                duration=duration,
                output="",
                error="Test timeout after 30 seconds",
                details={"timeout": 30}
            )
            
        except Exception as e:
            duration = time.time() - start_time
            print(f"❌ ERROR: {test_file} - {e}")
            failed_tests.append(test_file)
            reporter.add_test(
                test_name=test_file,
                status="ERROR",
                duration=duration,
                output="",
                error=str(e),
                details={"exception": type(e).__name__}
            )
    
    print("=" * 60)
    
    # Summary
    total_tests = len(test_files)
    passed_tests = total_tests - len(failed_tests)
    
    print(f"📊 Quick Test Summary:")
    print(f"   Total: {total_tests}")
    print(f"   Passed: {passed_tests}")
    print(f"   Failed: {len(failed_tests)}")
    
    if failed_tests:
        print(f"\n❌ Failed Tests ({len(failed_tests)}):")
        for i, test_name in enumerate(failed_tests, 1):
            print(f"   {i:2d}. {test_name}")
    
    success = len(failed_tests) == 0
    return success, failed_tests


def write_test_log(failed_tests, integration_passed, overall_reporter, final_report_path):
    """Write detailed test statistics to log file."""
    
    # Create results directory if it doesn't exist
    results_dir = Path(__file__).parent / "results"
    results_dir.mkdir(exist_ok=True)
    
    log_file = results_dir / "log.txt"
    
    # Get current timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Collect statistics from the reporter
    total_tests = len(overall_reporter.test_results)
    passed_tests = sum(1 for test in overall_reporter.test_results if test.status == 'PASSED')
    failed_test_count = sum(1 for test in overall_reporter.test_results if test.status == 'FAILED')
    error_test_count = sum(1 for test in overall_reporter.test_results if test.status == 'ERROR')
    
    # Calculate total duration
    total_duration = sum(test.duration for test in overall_reporter.test_results)
    
    # Write log
    with open(log_file, 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("REQUIREMENT EDITOR TEST RUNNER LOG\n")
        f.write("="*80 + "\n")
        f.write(f"Timestamp: {timestamp}\n")
        f.write(f"Version: 1.1.0\n")
        f.write(f"HTML Report: {final_report_path}\n\n")
        
        f.write("TEST STATISTICS\n")
        f.write("-"*40 + "\n")
        f.write(f"Total Tests Run: {total_tests}\n")
        f.write(f"Passed: {passed_tests}\n")
        f.write(f"Failed: {failed_test_count}\n")
        f.write(f"Errors: {error_test_count}\n")
        f.write(f"Integration Test: {'PASSED' if integration_passed else 'FAILED'}\n")
        f.write(f"Total Duration: {total_duration:.2f} seconds\n")
        if total_tests > 0:
            f.write(f"Average Duration: {total_duration/total_tests:.2f} seconds per test\n\n")
        else:
            f.write("Average Duration: N/A\n\n")
        
        if failed_tests:
            f.write("FAILED TESTS\n")
            f.write("-"*40 + "\n")
            for i, test_name in enumerate(failed_tests, 1):
                f.write(f"{i:2d}. {test_name}\n")
            f.write("\n")
        
        f.write("DETAILED TEST RESULTS\n")
        f.write("-"*40 + "\n")
        for test in overall_reporter.test_results:
            f.write(f"Test: {test.test_name}\n")
            f.write(f"Status: {test.status}\n")
            f.write(f"Duration: {test.duration:.2f}s\n")
            if test.status != 'PASSED':
                if test.error:
                    f.write(f"Error: {test.error[:200]}...\n")
                if test.details:
                    f.write(f"Details: {test.details}\n")
            f.write("-" * 20 + "\n")
        
        f.write("\nLOG END\n")
        f.write("="*80 + "\n")
    
    print(f"📝 Detailed log written to: {log_file}")
    return log_file


if __name__ == "__main__":
    
    # Create overall report generator
    overall_reporter = TestReportGenerator()
    
    # Run limited set of unit tests
    tests_passed, failed_tests = discover_and_run_limited_tests(overall_reporter)
    
    # Generate final comprehensive report
    final_report_path = overall_reporter.generate_html_report()
    
    # Write detailed log with statistics
    log_file = write_test_log(failed_tests, True, overall_reporter, final_report_path)
    
    # Final result
    print(f"\n{'='*60}")
    print("FINAL RESULTS")
    print('='*60)
    
    if tests_passed:
        print("✓ ALL QUICK TESTS PASSED!")
        print(f"📊 HTML Report: {final_report_path}")
        print(f"📝 Detailed Log File: {log_file}")
        sys.exit(0)
    else:
        print("✗ SOME QUICK TESTS FAILED!")
        print(f"📊 HTML Report: {final_report_path}")
        print(f"📝 Detailed Log File: {log_file}")
        
        if failed_tests:
            print(f"\n❌ Failed Tests ({len(failed_tests)}):")
            for i, test_name in enumerate(failed_tests, 1):
                print(f"   {i:2d}. {test_name}")
        
        sys.exit(1)
