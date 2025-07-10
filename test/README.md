# Test Directory

This directory contains all test files and test data for the Requirement Editor application.

## Structure

```
test/
├── test_runner.py              # Automated test discovery and execution
├── test_comprehensive.py       # Comprehensive integration tests
├── test_project_config.py      # Tests for project configuration module
├── test_simple.py              # Simple unit tests for basic functionality
├── test_stylesheet_config.py   # Tests for stylesheet configuration system
├── test_reporter.py            # HTML test report generator
├── test_md_edit_line_based.py  # Comprehensive tests for md_edit.py module
├── test_md_edit_integration.py # Integration tests for md_edit.py with real data
├── results/                    # Test execution results and reports
└── data/
    ├── test_input.md           # Sample markdown requirement document
    └── test_input.html         # Generated HTML output (created by tests)
```

## Running Tests

### Run All Tests
```bash
# From project root directory
python test/test_runner.py
```

This will:
- Discover all test files (`test_*.py`)
- Run each test file individually
- Run integration tests with the main application
- Provide a comprehensive test summary

### Run Individual Tests
```bash
# From project root directory
python test/test_project_config.py
```

### Expected Output
When all tests pass, you should see:
```
Requirement Editor Test Runner
============================================================
Found 4 test file(s):
  - test_comprehensive.py
  - test_project_config.py  
  - test_simple.py
  - test_stylesheet_config.py

============================================================
Running: test_project_config.py
============================================================
Testing Project Configuration Working Directory Enforcement
============================================================

Test 1: Basic project creation with default naming
✓ SUCCESS: Config file created at: [working_directory]/[filename]_config.json

Test 2: Project creation with custom name
✓ SUCCESS: Config file created at: [working_directory]/custom_test_config.json

Test 3: Custom filename with path components (security test)
✓ SUCCESS: Config file safely created at: [working_directory]/malicious_config.json
✓ SUCCESS: Path traversal attack prevented

Test 4: Filename without .json extension
✓ SUCCESS: Config file created with .json extension: [working_directory]/no_extension.json

============================================================
Test completed!
✓ PASSED: test_project_config.py

============================================================
Running Integration Test - Main Application
============================================================
Running main.py with test input: [test_directory]/data/test_input.md
✓ PASSED: Main application executed successfully
✓ PASSED: HTML output generated

============================================================
FINAL RESULTS
============================================================
✓ ALL TESTS AND INTEGRATION CHECKS PASSED!
```

## Test Data

### test_input.md
Sample markdown file containing various requirement document elements:
- Document titles
- Subtitles with indentation
- Requirements with ID numbers
- Comments with formatting

This file is used to test the parsing and HTML generation functionality.

### test_input.html
Generated HTML output from processing `test_input.md`. This file is created during testing and demonstrates the expected output format.

## Test Coverage

### Unit Tests
- **Project Configuration**: Tests working directory enforcement, file naming, security features
- **Path Security**: Validates prevention of directory traversal attacks
- **File Operations**: Tests creation, loading, and saving of configuration files

### Integration Tests
- **Main Application Workflow**: End-to-end test of markdown parsing and HTML generation
- **File I/O**: Tests reading input files and writing output files
- **Module Integration**: Validates interaction between parsing, generation, and configuration modules

## Test Modules

### test_stylesheet_config.py
Comprehensive test suite for the stylesheet configuration system:
- **Hardcoded Default Stylesheet**: Validates `_get_default_style_template()` function
- **Project Configuration**: Tests `ProjectConfig` stylesheet path management
- **HTML Generation**: Verifies HTML generation with custom and default stylesheets  
- **Graceful Fallback**: Tests fallback behavior when custom stylesheets are unavailable
- **Integration Testing**: End-to-end validation of stylesheet configuration workflow

This test module includes:
- CSS template validation (structure, required classes, syntax)
- Project configuration persistence and loading
- Custom stylesheet loading and error handling
- HTML output validation with different stylesheet configurations
- Backward compatibility testing for older project configurations

### test_comprehensive.py
Integration tests covering the complete application workflow from markdown parsing to HTML generation.

### test_simple.py
Basic unit tests for core functionality including parsing and classification.

### test_project_config.py
Tests for the project configuration management system including security features and file operations.

## MD Edit Module Tests

The `md_edit.py` module has dedicated test suites with comprehensive coverage:

### Core Functionality Tests
```bash
# Test the line number-based editing API
cd test
python test_md_edit_line_based.py
```

### Integration Tests
```bash
# Test with real requirement document data
cd test  
python test_md_edit_integration.py
```

### md_edit.py Implementation Details

The `md_edit.py` module uses a **line number-based** system for positioning and referencing elements within requirement documents. All operations work with line numbers that are automatically updated after insertions, deletions, and movements.

### Available md_edit Test Files

#### 1. test_md_edit_line_based.py ✅ CURRENT
**Status**: Active - Tests the current line number-based implementation

**Comprehensive Test Coverage**:
- ✅ Basic functionality (line number system, lookups)
- ✅ Editing operations (add before/after/under, move operations)
- ✅ Hierarchical operations (parent-child relationships)
- ✅ Deletion operations (with and without children)
- ✅ Type changes (requirement ↔ comment conversions)
- ✅ Search operations (by description, case sensitivity, special characters)
- ✅ Edge cases and error handling (invalid inputs, boundary conditions)
- ✅ Advanced hierarchical operations (deep nesting, complex moves)
- ✅ Bulk operations (multiple items, performance testing)
- ✅ Data integrity verification (consistency checks, ID uniqueness)
- ✅ Undo-like scenarios (change reversal, state management)

**Test Results**: 11/11 tests passed ✅

#### 2. test_md_edit_integration.py ✅ CURRENT
**Status**: Active - Integration tests with real data using line numbers

**Description**: Tests the line number-based API with real test data from `test/data/test_input.md`.

**Coverage**:
- ✅ Real document parsing and editing
- ✅ Complex editing operations on actual requirement documents
- ✅ Data integrity verification
- ✅ Performance with larger documents

**Test Results**: 2/2 tests passed ✅

### md_edit.py API Summary

**Core Editing Operations**:
- `add_item_before(line_number, type, description, item_id=None)`
- `add_item_after(line_number, type, description, item_id=None)`
- `add_item_under(line_number, type, description, item_id=None)`
- `move_item_before(source_line, target_line)`
- `move_item_after(source_line, target_line)`
- `move_item_under(source_line, target_line)`

**Content Operations**:
- `get_content(line_number)`
- `update_content(line_number, new_description)`
- `delete_item(line_number, delete_children=True)`
- `change_item_type(line_number, new_type, new_item_id=None)`

**Search & Navigation**:
- `find_by_item_id(item_id, item_type=None)` → returns line number
- `find_by_description(pattern, case_sensitive=False)` → returns line numbers
- `get_children(line_number)` → returns child line numbers
- `get_parent(line_number)` → returns parent line number

**Information**:
- `get_item_info(line_number)` → returns complete item dict
- `list_all_items()` → returns summary of all items
- `get_classified_parts()` → returns full structure

### Enhanced Test Coverage Statistics

The md_edit line-based test suite includes comprehensive coverage with:
- **11 test suites** covering all aspects of functionality
- **Over 50 individual test assertions**
- **Performance testing** with larger documents
- **Error handling and boundary condition** testing
- **Deep hierarchy testing** (5+ indent levels)
- **Bulk operations testing** (5+ items at once)
- **Data integrity verification** after complex operations

### Development History

1. **Original Implementation**: Line number-based system
2. **Refactor Attempt**: Object ID-based system (completed and tested)
3. **Reversion**: Back to line number-based system (current)

The object ID-based implementation was fully functional and tested, but was reverted as requested. All current tests focus on the line number-based approach.

## Adding New Tests

To add new test files:

1. Create a new file starting with `test_` (e.g., `test_new_feature.py`)
2. Place it in the `test/` directory
3. Follow the existing test structure and patterns
4. The test runner will automatically discover and execute the new test

Example test file structure:
```python
#!/usr/bin/env python3
"""
Test Description

Author: Attila Gallai <attila@tux-net.hu>
License: MIT License (see LICENSE.txt)
"""

import os
import sys

# Add parent directory to Python path to access libs
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from libs.module_name import function_to_test

def test_function_name():
    """Test description."""
    # Test implementation
    pass

if __name__ == "__main__":
    test_function_name()
    print("All tests completed!")
```

## Test Data Management

- Test input files should be placed in `test/data/`
- Generated output files during testing are also stored in `test/data/`
- Test files should be small and focused on specific functionality
- Clean up temporary files created during testing

---

*Test documentation for Requirement Editor v1.0.0*  
*Last updated: 2025-01-09 18:00*
