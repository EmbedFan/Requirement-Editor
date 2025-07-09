#!/usr/bin/env python3
"""
Command Line Interface Test Suite for Requirement Editor

This test module validates the command-line interface functionality including:
- Help option (-2h) display and content
- Markdown to HTML conversion (-md2html <filepath>)
- Error handling for invalid arguments and missing files
- Default behavior when no arguments provided
- Command-line argument parsing and validation

Test Coverage:
- Help system functionality and content validation
- File conversion workflow from command line
- Error handling and user feedback
- HTML output generation and validation
- Integration with existing parsing and generation modules

Author: Attila Gallai <attila@tux-net.hu>
Created: 2025-07-09
License: MIT License (see LICENSE.txt)
"""

import os
import sys
import subprocess
import tempfile

# Add the parent directory to the path to import the modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestCommandLineInterface:
    """Test class for command-line interface functionality."""
    
    def __init__(self):
        self.test_results = []
        self.main_py_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'main.py')
        self.test_data_dir = os.path.join(os.path.dirname(__file__), 'data')
        self.test_input_file = os.path.join(self.test_data_dir, 'test_input.md')
    
    def run_test(self, test_name, test_func):
        """Run a single test and record the result."""
        try:
            test_func()
            self.test_results.append(f"✓ PASS: {test_name}")
            print(f"✓ PASS: {test_name}")
            return True
        except Exception as e:
            self.test_results.append(f"✗ FAIL: {test_name} - {str(e)}")
            print(f"✗ FAIL: {test_name} - {str(e)}")
            return False
    
    def test_cli_help_option(self):
        """Test the -h help option functionality."""
        # Test 1: Help option returns success code
        result = subprocess.run([sys.executable, self.main_py_path, "-h"], 
                              capture_output=True, text=True)
        
        assert result.returncode == 0, f"Help option should return success code, got {result.returncode}"
        
        # Test 2: Help output contains required sections
        help_content = result.stdout
        assert help_content, "Help output should not be empty"
        
        required_sections = [
            'REQUIREMENT EDITOR',
            'USAGE:',
            'COMMAND LINE OPTIONS:',
            'EXAMPLES:',
            '-h',
            '-md2html'
        ]
        
        for section in required_sections:
            assert section in help_content, f"Help output missing required section: {section}"
        
        # Test 3: Help output has reasonable length
        assert len(help_content) > 500, "Help output seems too short to be comprehensive"
        
        # Test 4: Help contains usage examples
        assert 'python main.py' in help_content, "Help should contain usage examples"
        assert 'example.md' in help_content or 'test_input.md' in help_content, "Help should contain file examples"
    
    def test_cli_md2html_conversion(self):
        """Test the -md2html conversion functionality."""
        # Ensure test input file exists
        assert os.path.exists(self.test_input_file), f"Test input file not found: {self.test_input_file}"
        
        # Test 1: Successful conversion
        result = subprocess.run([sys.executable, self.main_py_path, "-md2html", self.test_input_file], 
                              capture_output=True, text=True)
        
        assert result.returncode == 0, f"Conversion should succeed, got exit code {result.returncode}"
        
        # Test 2: Output contains expected success messages
        output = result.stdout
        assert 'Successfully read' in output, "Output should indicate successful file reading"
        assert 'HTML file saved successfully' in output, "Output should indicate successful HTML generation"
        
        # Test 3: HTML file is created
        expected_html_file = self.test_input_file.replace('.md', '.html')
        assert os.path.exists(expected_html_file), f"HTML file should be created: {expected_html_file}"
        
        # Test 4: HTML file has valid content
        with open(expected_html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        assert len(html_content) > 1000, "HTML file should contain substantial content"
        assert '<!DOCTYPE html>' in html_content, "HTML should have proper DOCTYPE"
        assert '<html lang="en">' in html_content, "HTML should have proper language attribute"
        assert '<style>' in html_content, "HTML should contain embedded CSS"
        assert '<script>' in html_content, "HTML should contain JavaScript for interactivity"
        assert 'Test Document Title' in html_content or 'System Requirements' in html_content or 'Requirement document for Requirement Editor' in html_content, "HTML should contain actual content"
        
        # Test 5: Output shows processing details
        assert 'Classified' in output and 'parts:' in output, "Output should show classification details"
        assert 'Line' in output and 'Type:' in output, "Output should show detailed part information"
    
    def test_cli_error_handling(self):
        """Test error handling for invalid arguments and missing files."""
        # Test 1: Invalid command line option
        result = subprocess.run([sys.executable, self.main_py_path, "-invalid"], 
                              capture_output=True, text=True)
        
        assert result.returncode != 0, "Invalid arguments should return non-zero exit code"
        
        output = result.stdout
        assert 'Invalid command line' in output or 'Unknown option' in output, "Should indicate invalid arguments"
        assert 'Valid usage:' in output or 'USAGE:' in output, "Should show usage information"
        
        # Test 2: Missing file for conversion
        nonexistent_file = "nonexistent_file_12345.md"
        assert not os.path.exists(nonexistent_file), "Test file should not exist"
        
        result = subprocess.run([sys.executable, self.main_py_path, "-md2html", nonexistent_file], 
                              capture_output=True, text=True)
        
        assert result.returncode != 0, "Missing file should return non-zero exit code"
        
        output = result.stdout
        assert 'Input file not found' in output or 'Failed to read' in output, "Should indicate file not found"
        
        # Test 3: md2html without file argument
        result = subprocess.run([sys.executable, self.main_py_path, "-md2html"], 
                              capture_output=True, text=True)
        
        assert result.returncode != 0, "md2html without file should return non-zero exit code"
        
        output = result.stdout
        assert 'requires a file path' in output or 'Missing file path' in output, "Should indicate missing file path"
    
    def test_cli_default_behavior(self):
        """Test default behavior when no command line arguments are provided."""
        # Test 1: Default execution uses built-in configuration
        result = subprocess.run([sys.executable, self.main_py_path], 
                              capture_output=True, text=True)
        
        # Default behavior should work if the configured input file exists
        # The success depends on the cfg_inputfile setting in main.py
        output = result.stdout
        
        # Should either succeed with default file or show helpful error
        if result.returncode == 0:
            assert 'Successfully read' in output, "Default execution should process a file"
            assert 'HTML file saved' in output, "Default execution should generate HTML"
        else:
            # If default file doesn't exist, should show helpful message
            assert 'Failed to read' in output or 'not found' in output, "Should indicate file issue"
        
        # Test 2: Default behavior produces some output
        assert len(output) > 0, "Default execution should produce some output"
    
    def test_cli_integration_with_core_modules(self):
        """Test that CLI properly integrates with core parsing and generation modules."""
        # Use the existing test_input.md file instead of creating a temporary file
        test_file = self.test_input_file
        
        # Test conversion
        result = subprocess.run([sys.executable, self.main_py_path, "-md2html", test_file], 
                              capture_output=True, text=True)
        
        assert result.returncode == 0, "Conversion should succeed"
        
        # Check if HTML file was created
        html_file = test_file.replace('.md', '.html')
        assert os.path.exists(html_file), "HTML file should be generated"
        
        # Verify HTML content structure
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Should contain properly classified elements based on actual test_input.md content
        assert 'class="title' in html_content, "Should contain title elements"
        assert 'class="subtitle' in html_content, "Should contain subtitle elements"
        assert 'class="requirement' in html_content, "Should contain requirement elements"
        assert 'class="comment' in html_content, "Should contain comment elements"
        assert '1001 Req:' in html_content, "Should preserve requirement IDs"
        assert '1030 Comm:' in html_content, "Should process comment IDs"
        
        # Should contain interactive elements
        assert 'toggleCollapse' in html_content, "Should contain interactive JavaScript"
        assert 'controls' in html_content, "Should contain control buttons"
    
    def run_all_tests(self):
        """Run all command-line interface tests."""
        print("=" * 80)
        print("COMMAND LINE INTERFACE TEST SUITE")
        print("=" * 80)
        
        tests = [
            ("CLI Help Option Functionality", self.test_cli_help_option),
            ("CLI Markdown to HTML Conversion", self.test_cli_md2html_conversion),
            ("CLI Error Handling", self.test_cli_error_handling),
            ("CLI Default Behavior", self.test_cli_default_behavior),
            ("CLI Integration with Core Modules", self.test_cli_integration_with_core_modules)
        ]
        
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            print(f"\nRunning: {test_name}")
            print("-" * 60)
            if self.run_test(test_name, test_func):
                passed += 1
        
        print("\n" + "=" * 80)
        print("COMMAND LINE INTERFACE TEST RESULTS")
        print("=" * 80)
        
        for result in self.test_results:
            print(result)
        
        print(f"\nSummary: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 ALL COMMAND LINE INTERFACE TESTS PASSED!")
            return True
        else:
            print(f"❌ {total - passed} tests failed")
            return False


def main():
    """Main test runner for command-line interface tests."""
    test_suite = TestCommandLineInterface()
    
    try:
        success = test_suite.run_all_tests()
        
        # Return appropriate exit code
        if success:
            print("\n✅ All command-line interface tests completed successfully!")
            sys.exit(0)
        else:
            print("\n❌ Some command-line interface tests failed!")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n💥 Test suite crashed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
