# Test Directory

This directory contains all test files and test data for the Requirement Editor application.

## Structure

```
test/
├── test_runner.py              # Automated test discovery and execution
├── test_project_config.py      # Tests for project configuration module
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
Found 1 test file(s):
  - test_project_config.py

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
