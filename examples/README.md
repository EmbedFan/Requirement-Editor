# Examples Directory

This directory contains demonstration scripts that show how to use various features of the Requirement Editor application.

## 📁 Demo Scripts

### 🎯 **demo_type_aliases.py**
**Purpose**: Demonstrates the type aliases functionality  
**Features**: Shows how to use short aliases (TIT, SUB, REQ, COM) instead of full type names  
**Usage**: `python examples/demo_type_aliases.py`

### ⌨️ **demo_terminal_editor.py**
**Purpose**: Introduction and overview of terminal editor functionality  
**Features**: Shows how to start the terminal editor and provides command overview  
**Usage**: `python examples/demo_terminal_editor.py`

### ✨ **demo_features.py**
**Purpose**: Demonstrates new features like DATTR timestamps and modification date updates  
**Features**: Shows automatic DATTR creation in new documents and timestamp management  
**Usage**: `python examples/demo_features.py`

### 🕒 **demo_dattr.py**
**Purpose**: Specifically demonstrates DATTR read-only timestamp functionality  
**Features**: Shows how DATTR items are protected from editing and automatic timestamp updates  
**Usage**: `python examples/demo_dattr.py`

## 🚀 Running Examples

All demo scripts can be run from the project root:

```bash
# Run individual demos
python examples/demo_type_aliases.py
python examples/demo_terminal_editor.py
python examples/demo_features.py
python examples/demo_dattr.py
```

## 📚 What You'll Learn

These examples demonstrate:

- **Type Aliases**: How to use short type names for faster editing
- **Terminal Editor**: Interactive command-line interface for document editing
- **DATTR Management**: Automatic timestamp handling and read-only protection
- **Document Creation**: How new documents are structured with metadata
- **Save Operations**: How saving updates modification timestamps
- **Feature Integration**: How all components work together

## 🎯 For Developers

These demo scripts serve as:
- **Usage Examples**: Real-world scenarios for using the editor features
- **Integration Examples**: How to use the terminal editor programmatically
- **Feature Verification**: Manual testing of implemented functionality
- **Documentation**: Live examples of feature behavior

## 📝 Notes

- All demo scripts include proper import path handling
- Examples create temporary files that can be safely deleted
- Scripts are designed to be run independently
- Each demo includes explanatory output showing what's happening
