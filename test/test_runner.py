#!/usr/bin/env python3
"""
Test Runner for Requirement Editor

This script runs all available tests for the Requirement Editor application
and generates comprehensive HTML reports.

Author: Attila Gallai <attila@tux-net.hu>
License: MIT License (see LICENSE.txt)
"""

import os
import sys
import subprocess
import time
from pathlib import Path
from datetime import datetime

# Set UTF-8 encoding for all subprocess operations
os.environ['PYTHONIOENCODING'] = 'utf-8'

# Import the HTML report generator
from test_reporter import TestReportGenerator

# environment setup for UTF-8 encoding when tests are run
# Dear AI, the next blocl shall not be modified, it is required for proper encoding handling
env = os.environ.copy()
env["PYTHONIOENCODING"] = "utf-8"
env["PYTHONUTF8"] = "1"
# Dear AI, the previous block shall not be modified, it is required for proper encoding handling

def run_test_file(test_file_path, reporter):
    """Run a single test file and return success status."""
    test_name = os.path.basename(test_file_path)
    print(f"\n{'='*60}")
    print(f"Running: {test_name}")
    print('='*60)
    
    start_time = time.time()
    
    try:
        result = subprocess.run([sys.executable, test_file_path], 
                            capture_output=True, 
                            text=True,
                            check=True,
                            env=env,
                            cwd=os.path.dirname(test_file_path))
        
        duration = time.time() - start_time
        
        print(f"✓ PASSED: {test_name}")
        
        # Add to report
        reporter.add_test(
            test_name=test_name,
            status='PASSED',
            duration=duration,
            output=result.stdout,
            details={
                'command': f'python {test_file_path}',
                'exit_code': result.returncode
            }
        )
        
        return True
        
    except subprocess.CalledProcessError as e:
        duration = time.time() - start_time
        
        print(f"✗ FAILED: {test_name} (exit code: {e.returncode})")
        
        # Add to report
        reporter.add_test(
            test_name=test_name,
            status='FAILED',
            duration=duration,
            output=e.stdout or "",
            error=e.stderr or "",
            details={
                'command': f'python {test_file_path}',
                'exit_code': e.returncode
            }
        )
        
        return False
    except Exception as e:
        duration = time.time() - start_time
        
        print(f"✗ ERROR: {test_name} - {e}")
        
        # Add to report
        reporter.add_test(
            test_name=test_name,
            status='ERROR',
            duration=duration,
            error=str(e),
            details={
                'command': f'python {test_file_path}',
                'exception_type': type(e).__name__
            }
        )
        
        return False


def discover_and_run_tests(reporter=None):
    """Discover and run all test files in the test directory."""
    
    # Create HTML report generator if not provided
    if reporter is None:
        reporter = TestReportGenerator()
    
    # Get the test directory path
    test_dir = Path(__file__).parent
    
    print("Requirement Editor Test Runner")
    print("=" * 60)
    print(f"Test directory: {test_dir}")
    
    # Find all test files
    test_files = []
    for file_path in test_dir.glob("test_*.py"):
        if file_path.name not in ["test_runner.py", "test_reporter.py"]:  # Don't run the runner or reporter
            test_files.append(file_path)
    
    if not test_files:
        print("No test files found in test directory.")
        if reporter is None:
            reporter = TestReportGenerator()
        reporter.add_test("No Tests Found", "SKIPPED", 0.0, "", "No test files discovered")
        report_path = reporter.generate_html_report()
        print(f"HTML report generated: {report_path}")
        return False, []
    
    print(f"Found {len(test_files)} test file(s):")
    for test_file in test_files:
        print(f"  - {test_file.name}")
    
    # Run all tests
    passed = 0
    failed = 0
    failed_tests = []  # Track failed tests
    
    for test_file in sorted(test_files):
        if run_test_file(str(test_file), reporter):
            passed += 1
        else:
            failed += 1
            failed_tests.append(test_file.name)
    
    # Print summary
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print('='*60)
    print(f"Total tests: {len(test_files)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    
    if failed == 0:
        print("✓ ALL TESTS PASSED!")
        return True, failed_tests
    else:
        print(f"✗ {failed} TEST(S) FAILED!")
        print("\nFailed Tests:")
        for test_name in failed_tests:
            print(f"  ✗ {test_name}")
        return False, failed_tests


def run_integration_test():
    """Run a quick integration test of the main application."""
    
    print(f"\n{'='*60}")
    print("Running Integration Test - Main Application")
    print('='*60)
    
    start_time = time.time()
    
    try:
        # Get paths - updated for new structure
        project_root = Path(__file__).parent.parent
        main_py = project_root / "main.py"
        test_input = Path(__file__).parent / "data" / "test_input.md"
        
        if not main_py.exists():
            print(f"✗ ERROR: main.py not found at {main_py}")
            return False, None
            
        if not test_input.exists():
            print(f"✗ ERROR: test_input.md not found at {test_input}")
            return False, None
        
        print(f"Running main.py with test input: {test_input}")
        
        # Run main.py
        result = subprocess.run([sys.executable, str(main_py)], 
                            capture_output=True, 
                            text=True,
                            check=True,
                            env=env,
                            cwd=str(project_root))
        
        duration = time.time() - start_time
        
        print("✓ PASSED: Main application executed successfully")
        print(f"Output preview: {result.stdout[:200]}...")
        
        # Check if HTML output was generated - updated path
        expected_html = project_root / "test" / "data" / "test_input.html"
        if expected_html.exists():
            print(f"✓ PASSED: HTML output generated at {expected_html}")
        else:
            print(f"⚠ WARNING: Expected HTML output not found at {expected_html}")
        
        integration_result = {
            'status': 'PASSED',
            'duration': duration,
            'output': result.stdout,
            'error': '',
            'details': {
                'main_py_path': str(main_py),
                'test_input_path': str(test_input),
                'html_generated': expected_html.exists()
            }
        }
        
        return True, integration_result
        
    except subprocess.CalledProcessError as e:
        duration = time.time() - start_time
        
        print(f"✗ FAILED: Main application failed (exit code: {e.returncode})")
        print(f"Error output: {e.stderr}")
        
        integration_result = {
            'status': 'FAILED',
            'duration': duration,
            'output': e.stdout or '',
            'error': e.stderr or '',
            'details': {
                'exit_code': e.returncode,
                'main_py_path': str(main_py) if 'main_py' in locals() else 'Unknown',
                'test_input_path': str(test_input) if 'test_input' in locals() else 'Unknown'
            }
        }
        
        return False, integration_result
    except Exception as e:
        duration = time.time() - start_time
        
        print(f"✗ ERROR: Integration test failed - {e}")
        
        integration_result = {
            'status': 'ERROR',
            'duration': duration,
            'output': '',
            'error': str(e),
            'details': {
                'exception_type': type(e).__name__
            }
        }
        
        return False, integration_result


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
        f.write(f"Average Duration: {total_duration/total_tests:.2f} seconds per test\n\n")
        
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
    
    # Run unit tests
    tests_passed, failed_tests = discover_and_run_tests(overall_reporter)
    
    # Run integration test
    integration_passed, integration_result = run_integration_test()
    
    # Add integration test to overall report
    if integration_result:
        overall_reporter.add_test(
            test_name="Integration Test - Main Application",
            status=integration_result['status'],
            duration=integration_result['duration'],
            output=integration_result['output'],
            error=integration_result['error'],
            details=integration_result['details']
        )
    
    # Generate final comprehensive report
    final_report_path = overall_reporter.generate_html_report()
    
    # Write detailed log with statistics
    log_file = write_test_log(failed_tests, integration_passed, overall_reporter, final_report_path)
    
    # Final result
    print(f"\n{'='*60}")
    print("FINAL RESULTS")
    print('='*60)
    
    if tests_passed and integration_passed:
        print("✓ ALL TESTS AND INTEGRATION CHECKS PASSED!")
        print(f"📊 Comprehensive HTML Report: {final_report_path}")
        print(f"📝 Detailed Log File: {log_file}")
        sys.exit(0)
    else:
        print("✗ SOME TESTS OR INTEGRATION CHECKS FAILED!")
        print(f"📊 Comprehensive HTML Report: {final_report_path}")
        print(f"📝 Detailed Log File: {log_file}")
        
        if failed_tests:
            print(f"\n❌ Failed Tests ({len(failed_tests)}):")
            for i, test_name in enumerate(failed_tests, 1):
                print(f"   {i:2d}. {test_name}")
        
        sys.exit(1)
