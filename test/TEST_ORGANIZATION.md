# Test Organization - Updated Structure

## 📁 Test Directory Structure

All test files have been moved to the `test/` directory for better organization:

```
test/
├── README.md                    # Test documentation
├── test_comprehensive.py        # Full system integration test
├── test_save_issue.py          # New document structure tests
├── test_type_command.py         # Type command alias tests
├── test_type_aliases.py         # Type alias functionality tests
├── test_saveas_final.py         # Saveas functionality tests
├── test_saveas_integration.py   # Saveas integration tests
├── test_cancellation_fix.py     # Save cancellation behavior tests
├── test_md_edit_*.py           # Markdown editor tests
├── test_project_config.py       # Project configuration tests
├── test_display_mode.py         # Display mode tests
├── data/                        # Test data files
├── results/                     # Test results
└── ...                         # Other test files
```

## 🔧 Import Path Standard

All test files now use the standard import pattern:

```python
import sys
import os
# Add parent directory to path to access libs
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from libs.terminal_editor import TerminalEditor
from libs.md_edit import MarkdownEditor
# ... other imports
```

## 🏃 Running Tests

### From Project Root:
```bash
# Run specific test
python test/test_comprehensive.py

# Run all tests
python -m pytest test/
```

### From Test Directory:
```bash
cd test
python test_comprehensive.py
python test_save_issue.py
```

## ✅ Migration Completed

- ✅ All `test_*.py` files moved from root to `test/` directory
- ✅ Import paths updated for new directory structure
- ✅ All tests verified to work in new location
- ✅ Comprehensive test suite passes
- ✅ No regression in functionality

## 📝 Guidelines for New Tests

**All new test files should:**

1. **Be created in the `test/` directory**
2. **Follow naming convention: `test_*.py`**
3. **Use the standard import pattern shown above**
4. **Include proper documentation and comments**
5. **Be included in the comprehensive test suite where appropriate**

Example new test file template:

```python
#!/usr/bin/env python3
"""
Test description here.
"""

import sys
import os
# Add parent directory to path to access libs
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from libs.terminal_editor import TerminalEditor

def test_my_feature():
    """Test description."""
    # Test implementation
    pass

if __name__ == "__main__":
    # Test execution
    pass
```
