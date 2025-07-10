#!/usr/bin/env python3
"""
Test Suite for Stylesheet Configuration Functionality

This test module validates the stylesheet configuration system including:
- Hardcoded default stylesheet template functionality
- Project configuration stylesheet management
- HTML generation with custom and default stylesheets
- Graceful fallback behavior when custom stylesheets are unavailable

Test Coverage:
- _get_default_style_template() function validation
- ProjectConfig style_template_path management
- GenerateHTML() with stylesheet configuration
- Error handling and fallback mechanisms
- Integration between project config and HTML generation

Author: Attila Gallai <attila@tux-net.hu>
Created: 2025-07-09
License: MIT License (see LICENSE.txt)
"""

import os
import sys
import tempfile
import json
from pathlib import Path

# Add the parent directory to the path to import the modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from libs.gen_html_doc import GenerateHTML, _get_default_style_template, _load_stylesheet_template
from libs.project import ProjectConfig
from libs.parse_req_md import ClassifyParts


class TestStylesheetConfiguration:
    """Test class for stylesheet configuration functionality."""
    
    def __init__(self):
        self.test_results = []
        self.temp_dir = tempfile.mkdtemp()
        self.sample_classified_parts = self._create_sample_classified_parts()
    
    def _create_sample_classified_parts(self):
        """Create sample classified parts for testing HTML generation."""
        return [
            {
                'line_number': 1,
                'type': 'TITLE',
                'indent': 0,
                'id': None,
                'description': 'Test Document Title',
                'parent': None,
                'children': [2, 3],
                'children_refs': []
            },
            {
                'line_number': 2,
                'type': 'SUBTITLE',
                'indent': 1,
                'id': None,
                'description': 'Test Subtitle',
                'parent': 1,
                'children': [],
                'children_refs': []
            },
            {
                'line_number': 3,
                'type': 'REQUIREMENT',
                'indent': 1,
                'id': 1001,
                'description': 'Test requirement description',
                'parent': 1,
                'children': [],
                'children_refs': []
            },
            {
                'line_number': 4,
                'type': 'DATTR',
                'indent': 1,
                'id': 1002,
                'description': 'Created at: <CRAT><br>Modified at: <MODAT>',
                'parent': 1,
                'children': [],
                'children_refs': []
            }
        ]
    
    def _build_hierarchy(self, classified_parts):
        """Build parent-child references for testing."""
        # Create lookup dictionary
        parts_dict = {part['line_number']: part for part in classified_parts}
        
        # Build children_refs
        for part in classified_parts:
            part['children_refs'] = [parts_dict[child_id] for child_id in part['children'] if child_id in parts_dict]
        
        return classified_parts
    
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
    
    def test_hardcoded_default_stylesheet(self):
        """Test that _get_default_style_template() provides a complete CSS template."""
        # Test 1: Function returns non-empty string
        css_template = _get_default_style_template()
        assert css_template, "Default stylesheet template should not be empty"
        assert isinstance(css_template, str), "Default stylesheet template should be a string"
        
        # Test 2: Template contains required CSS classes
        required_classes = [
            '.title', '.subtitle', '.requirement', '.comment', '.dattr', '.unknown',
            '.indent-0', '.indent-1', '.indent-2', '.indent-3', '.indent-4',
            '.line-number', '.collapsible', '.collapsible-content', '.controls'
        ]
        
        for css_class in required_classes:
            assert css_class in css_template, f"Default template missing required class: {css_class}"
        
        # Test 3: Template contains essential styling elements
        essential_elements = [
            'body {', 'font-family:', 'background-color:', 'color:',
            '@media print', 'margin:', 'padding:'
        ]
        
        for element in essential_elements:
            assert element in css_template, f"Default template missing essential element: {element}"
        
        # Test 4: Template has reasonable length (should be comprehensive)
        assert len(css_template) > 3000, "Default stylesheet template seems too short to be comprehensive"
        
        # Test 5: Template contains proper CSS syntax
        assert css_template.count('{') == css_template.count('}'), "CSS template has unmatched braces"
        assert '/*' in css_template and '*/' in css_template, "CSS template should contain comments"
    
    def test_project_config_stylesheet_management(self):
        """Test ProjectConfig class stylesheet management functionality."""
        config_path = os.path.join(self.temp_dir, 'test_config.json')
        
        # Test 1: New project has default None stylesheet path
        config = ProjectConfig(config_path)
        config.create_new_project('test.md')
        
        assert config.get_style_template_path() is None, "New project should have None stylesheet path"
        
        # Test 2: Set custom stylesheet path
        custom_path = 'custom_style.css'
        config.set_style_template_path(custom_path)
        
        assert config.get_style_template_path() == custom_path, "Custom stylesheet path should be set correctly"
        
        # Test 3: Save and reload project maintains stylesheet path
        config.save_project()
        
        config2 = ProjectConfig(config_path)
        config2.load_project()
        
        assert config2.get_style_template_path() == custom_path, "Loaded config should maintain custom stylesheet path"
        
        # Test 4: Set stylesheet path to None
        config2.set_style_template_path(None)
        assert config2.get_style_template_path() is None, "Should be able to set stylesheet path to None"
        
        # Test 5: Configuration includes stylesheet path in JSON
        config2.set_style_template_path('another_style.css')
        config2.save_project()
        
        with open(config_path, 'r') as f:
            config_data = json.load(f)
        
        assert 'style_template_path' in config_data, "Configuration JSON should include style_template_path"
        assert config_data['style_template_path'] == 'another_style.css', "JSON should contain correct stylesheet path"
        
        # Test 6: Load older config without stylesheet path (backward compatibility)
        old_config_data = {
            "input_md_file_path": "test.md",
            "project_creation_date": "2025-07-09 14:40",
            "project_last_modification_date": "2025-07-09 14:40",
            "application_version": "1.0.0"
        }
        
        old_config_path = os.path.join(self.temp_dir, 'old_config.json')
        with open(old_config_path, 'w') as f:
            json.dump(old_config_data, f)
        
        old_config = ProjectConfig(old_config_path)
        old_config.load_project()
        
        assert old_config.get_style_template_path() is None, "Old config should default to None stylesheet path"
    
    def test_html_generation_with_stylesheets(self):
        """Test GenerateHTML() function with both default and custom stylesheets."""
        classified_parts = self._build_hierarchy(self.sample_classified_parts)
        
        # Test 1: HTML generation with default stylesheet (no config)
        html_default = GenerateHTML(classified_parts, "Test Document")
        
        assert html_default, "HTML generation should produce output"
        assert '<!DOCTYPE html>' in html_default, "HTML should have proper DOCTYPE"
        assert '<style>' in html_default, "HTML should contain embedded CSS"
        assert 'font-family: Arial, sans-serif' in html_default, "HTML should contain default CSS"
        assert 'Test Document Title' in html_default, "HTML should contain content"
        
        # Test 2: HTML generation with project config (None stylesheet)
        config = ProjectConfig(os.path.join(self.temp_dir, 'test_html_config.json'))
        config.create_new_project('test.md')
        
        html_config_none = GenerateHTML(classified_parts, "Test Document", config)
        
        assert html_config_none, "HTML generation with config should produce output"
        assert html_config_none == html_default, "HTML with None stylesheet should match default"
        
        # Test 3: HTML generation with custom stylesheet path (file doesn't exist - should fallback)
        config.set_style_template_path('nonexistent_style.css')
        
        html_fallback = GenerateHTML(classified_parts, "Test Document", config)
        
        assert html_fallback, "HTML generation with missing custom stylesheet should produce output"
        assert 'font-family: Arial, sans-serif' in html_fallback, "Should fallback to default stylesheet"
        
        # Test 4: HTML generation with valid custom stylesheet
        custom_css = """
        body { font-family: 'Times New Roman', serif; background-color: #fff; }
        .title { color: #800000; font-size: 2.5em; }
        .requirement { background-color: #f0f8ff; border-left: 5px solid #4169e1; }
        .comment { background-color: #fff8dc; border-left: 5px solid #ffa500; }
        .dattr { background-color: #e6f3ff; border-left: 5px solid #007acc; }
        .subtitle { background-color: #f5f5dc; border-left: 5px solid #4b0082; }
        .unknown { background-color: #f5f5f5; border-left: 5px solid #808080; }
        .controls { margin-bottom: 30px; text-align: center; }
        .indent-0 { margin-left: 0px; }
        .indent-1 { margin-left: 40px; }
        .line-number { color: #800000; font-size: 0.9em; }
        .collapsible { position: relative; cursor: pointer; }
        .collapsible-content { overflow: hidden; }
        .collapsible-content.collapsed { max-height: 0; }
        .collapsible-content.expanded { max-height: 1000px; }
        @media print { .controls { display: none !important; } }
        """
        
        custom_stylesheet_path = os.path.join(self.temp_dir, 'custom_style.css')
        with open(custom_stylesheet_path, 'w') as f:
            f.write(custom_css)
        
        config.set_style_template_path(custom_stylesheet_path)
        
        html_custom = GenerateHTML(classified_parts, "Test Document", config)
        
        assert html_custom, "HTML generation with custom stylesheet should produce output"
        assert 'Times New Roman' in html_custom, "HTML should contain custom CSS"
        assert '#800000' in html_custom, "HTML should contain custom colors"
        assert 'font-family: Arial, sans-serif' not in html_custom, "HTML should not contain default CSS"
        
        # Test 5: HTML structure validation
        for html_content in [html_default, html_config_none, html_fallback, html_custom]:
            assert '<html lang="en">' in html_content, "HTML should have proper language attribute"
            assert '<meta charset="UTF-8">' in html_content, "HTML should have proper charset"
            assert '<title>Test Document</title>' in html_content, "HTML should have proper title"
            assert '<div class="container">' in html_content, "HTML should have container div"
            assert '<script>' in html_content, "HTML should contain JavaScript"
            assert 'toggleCollapse' in html_content, "HTML should contain interactive functions"
    
    def test_graceful_fallback_behavior(self):
        """Test graceful fallback when custom stylesheets are not found."""
        # Test 1: _load_stylesheet_template with None path
        css_none = _load_stylesheet_template(None)
        default_css = _get_default_style_template()
        
        assert css_none == default_css, "None path should return default template"
        
        # Test 2: _load_stylesheet_template with empty string
        css_empty = _load_stylesheet_template("")
        assert css_empty == default_css, "Empty string should return default template"
        
        # Test 3: _load_stylesheet_template with nonexistent file
        css_missing = _load_stylesheet_template('nonexistent_file.css')
        assert css_missing == default_css, "Missing file should return default template"
        
        # Test 4: _load_stylesheet_template with invalid path
        css_invalid = _load_stylesheet_template('/invalid/path/style.css')
        assert css_invalid == default_css, "Invalid path should return default template"
        
        # Test 5: _load_stylesheet_template with directory instead of file
        css_dir = _load_stylesheet_template(self.temp_dir)
        assert css_dir == default_css, "Directory path should return default template"
        
        # Test 6: _load_stylesheet_template with valid file
        valid_css = "body { color: red; }"
        valid_path = os.path.join(self.temp_dir, 'valid.css')
        with open(valid_path, 'w') as f:
            f.write(valid_css)
        
        css_valid = _load_stylesheet_template(valid_path)
        assert css_valid == valid_css, "Valid file should return file content"
        assert css_valid != default_css, "Valid file should not return default template"
        
        # Test 7: Integration test - fallback in HTML generation
        classified_parts = self._build_hierarchy(self.sample_classified_parts)
        config = ProjectConfig(os.path.join(self.temp_dir, 'fallback_config.json'))
        config.create_new_project('test.md')
        
        # Set various invalid paths and ensure fallback works
        invalid_paths = [
            'nonexistent.css',
            '/invalid/path/style.css',
            '',
            None,
            self.temp_dir  # directory instead of file
        ]
        
        for invalid_path in invalid_paths:
            config.set_style_template_path(invalid_path)
            html_output = GenerateHTML(classified_parts, "Test Document", config)
            
            assert html_output, f"HTML generation should work with invalid path: {invalid_path}"
            assert 'font-family: Arial, sans-serif' in html_output, f"Should fallback to default CSS for: {invalid_path}"
    
    def run_all_tests(self):
        """Run all stylesheet configuration tests."""
        print("=" * 80)
        print("STYLESHEET CONFIGURATION TEST SUITE")
        print("=" * 80)
        
        tests = [
            ("Hardcoded Default Stylesheet Template", self.test_hardcoded_default_stylesheet),
            ("Project Configuration Stylesheet Management", self.test_project_config_stylesheet_management),
            ("HTML Generation with Stylesheets", self.test_html_generation_with_stylesheets),
            ("Graceful Fallback Behavior", self.test_graceful_fallback_behavior)
        ]
        
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            print(f"\nRunning: {test_name}")
            print("-" * 60)
            if self.run_test(test_name, test_func):
                passed += 1
        
        print("\n" + "=" * 80)
        print("STYLESHEET CONFIGURATION TEST RESULTS")
        print("=" * 80)
        
        for result in self.test_results:
            print(result)
        
        print(f"\nSummary: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 ALL STYLESHEET CONFIGURATION TESTS PASSED!")
            return True
        else:
            print(f"❌ {total - passed} tests failed")
            return False
    
    def cleanup(self):
        """Clean up temporary files."""
        import shutil
        try:
            shutil.rmtree(self.temp_dir)
        except:
            pass


def main():
    """Main test runner for stylesheet configuration tests."""
    test_suite = TestStylesheetConfiguration()
    
    try:
        success = test_suite.run_all_tests()
        
        # Return appropriate exit code
        if success:
            print("\n✅ All stylesheet configuration tests completed successfully!")
            sys.exit(0)
        else:
            print("\n❌ Some stylesheet configuration tests failed!")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n💥 Test suite crashed: {e}")
        sys.exit(1)
    finally:
        test_suite.cleanup()


if __name__ == "__main__":
    main()
