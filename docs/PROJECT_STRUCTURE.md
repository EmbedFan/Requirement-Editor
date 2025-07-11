# Project Structure Guidelines

**Established:** July 11, 2025  
**Status:** MANDATORY for all future development

## 🏗️ Official Directory Structure

This document defines the mandatory file organization structure for the Requirement Editor project. **All contributors must follow these guidelines.**

```
python/
├── main.py                    # Main application entry point
├── README.md                  # Project overview and quick start
├── LICENSE                    # Project license
├── .gitignore                 # Git ignore rules
├── .vscode/                   # VS Code workspace settings
├── .venv/                     # Python virtual environment
│
├── libs/                      # 🔧 CORE APPLICATION MODULES
│   ├── md_edit.py            # Markdown editing functionality
│   ├── terminal_editor.py    # Terminal-based editor
│   ├── project.py            # Project configuration management
│   ├── gen_html_doc.py       # HTML generation
│   ├── parse_req_md.py       # Markdown parsing
│   └── __pycache__/          # Python cache files
│
├── docs/                      # 📖 DOCUMENTATION
│   ├── README.md             # Documentation index
│   ├── main.md               # Main module documentation
│   ├── project.md            # Project configuration docs
│   ├── TERMINAL_EDITOR.md    # Terminal editor user guide
│   ├── parse_req_md.md       # Parsing module docs
│   └── gen_html_doc.md       # HTML generation docs
│
├── examples/                  # 📚 DEMONSTRATION SCRIPTS
│   ├── README.md             # Examples overview and usage
│   ├── demo_type_aliases.py  # Type aliases demonstration
│   ├── demo_terminal_editor.py # Terminal editor introduction
│   ├── demo_features.py      # New features demonstration
│   └── demo_dattr.py         # DATTR functionality demo
│
└── test/                     # 🧪 TESTING ECOSYSTEM
    ├── README.md             # Test directory overview
    ├── TEST_ORGANIZATION.md  # Test organization guidelines
    ├── test_comprehensive.py # Main integration tests
    ├── test_*.py             # All other test scripts
    ├── data/                 # Test input files and data
    ├── results/              # Test execution results
    └── *.md                  # Test-related documentation
```

## 📋 File Placement Rules

### 🔧 **Module Files → `libs/`**
**What goes here:**
- All `.py` files containing core application logic
- Reusable modules and classes
- Application utilities and helpers
- Library code that other modules import

**Examples:**
- `md_edit.py` - Markdown editing functionality
- `terminal_editor.py` - Terminal interface
- `project.py` - Configuration management
- `parse_req_md.py` - Document parsing

**Naming convention:** Descriptive names reflecting functionality

### 📖 **Documentation → `docs/`**
**What goes here:**
- User guides and tutorials
- API documentation
- Feature specifications
- Architecture documentation
- Non-test related markdown files

**Examples:**
- `TERMINAL_EDITOR.md` - User guide for terminal editor
- `project.md` - Configuration system documentation
- `main.md` - Main application documentation

**Naming convention:** `FEATURE_NAME.md` or `module_name.md`

### 📚 **Examples → `examples/`**
**What goes here:**
- Demonstration scripts showing feature usage
- Tutorial code examples
- Sample implementations
- Usage pattern demonstrations

**Examples:**
- `demo_type_aliases.py` - How to use type aliases
- `demo_terminal_editor.py` - Terminal editor walkthrough
- `demo_features.py` - New features showcase

**Naming convention:** `demo_*.py` for scripts, descriptive names for docs

### 🧪 **Tests → `test/`**
**What goes here:**
- All test scripts and test code
- Test-related documentation
- Test data files and fixtures
- Test execution results and reports
- Testing utilities and helpers

**Examples:**
- `test_comprehensive.py` - Integration tests
- `test_md_edit.py` - Module-specific tests
- `TEST_ORGANIZATION.md` - Testing guidelines
- `data/test_input.md` - Test data files

**Naming convention:** `test_*.py` for scripts, `TEST_*.md` or `*_TEST.md` for docs

### 🏠 **Root Directory**
**What goes here:** ONLY essential project files
- `main.py` - Application entry point
- `README.md` - Project overview
- `LICENSE` - License file
- Configuration files (`.gitignore`, etc.)
- Environment directories (`.venv/`, `.vscode/`)

**What does NOT go here:**
- ❌ Module files (use `libs/`)
- ❌ Documentation files (use `docs/`)  
- ❌ Test files (use `test/`)
- ❌ Demo scripts (use `examples/`)

## ⚠️ Enforcement Rules

### 🚫 **NEVER PUT IN ROOT:**
- Python modules (`.py` files except `main.py`)
- Documentation files (`.md` files except `README.md`)
- Test files or test data
- Demo scripts or examples
- Generated files or temporary files

### ✅ **ALWAYS ORGANIZE BY PURPOSE:**
- **Functionality** → `libs/`
- **Documentation** → `docs/`
- **Examples** → `examples/`
- **Testing** → `test/`

### 📝 **FILE NAMING CONVENTIONS:**
- **Test files:** `test_*.py`, `TEST_*.md`
- **Demo files:** `demo_*.py`
- **Module files:** `descriptive_name.py`
- **Documentation:** `FEATURE_NAME.md` or `module_name.md`

## 🎯 Benefits of This Structure

### 🧹 **Clean Organization**
- Easy to find any type of file
- Clear separation of concerns
- Professional project appearance
- Reduced cognitive overhead

### 🔍 **Better Navigation**
- Logical grouping of related files
- Predictable file locations
- IDE-friendly structure
- Version control friendly

### 🛠️ **Easier Maintenance**
- Related files grouped together
- Clear dependency relationships
- Simplified testing and documentation
- Better collaboration support

## 🚀 Migration History

- **July 9, 2025:** Initial test file migration
- **July 11, 2025:** Complete organization overhaul
  - Moved all test-related files to `test/`
  - Created `examples/` for demo scripts
  - Established mandatory structure guidelines

## ⚖️ Compliance

**This structure is MANDATORY for all future development.**

When adding new files:
1. ✅ Identify the file's primary purpose
2. ✅ Place it in the appropriate directory
3. ✅ Follow naming conventions
4. ✅ Update documentation if needed
5. ✅ Verify the root directory stays clean

**Violations of this structure will require immediate correction.**
