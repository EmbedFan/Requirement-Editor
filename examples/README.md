# Examples Directory

This directory contains demonstration scripts that show how to use various features of the Requirement Editor application.

## 📁 Demo Scripts

### 🎯 **demo_type_aliases.py**
**Purpose**: Demonstrates the type aliases functionality  
**Features**: Shows how to use short aliases (TIT, SUB, REQ, COM) instead of full type names  
**Usage**: `python examples/demo_type_aliases.py`

### ⌨️ **demo_terminal_editor.py**
**Purpose**: Introduction and overview of terminal editor functionality with latest features  
**Features**: Shows how to start the terminal editor and provides complete command overview including DATTR, export, and tab completion  
**Usage**: `python examples/demo_terminal_editor.py`

### ✨ **demo_features.py**
**Purpose**: Demonstrates new features like DATTR timestamps, modification date updates, and smart export  
**Features**: Shows automatic DATTR creation in new documents, timestamp management, and export functionality  
**Usage**: `python examples/demo_features.py`

### 🕒 **demo_dattr.py**
**Purpose**: Specifically demonstrates DATTR read-only timestamp functionality and visual styling  
**Features**: Shows how DATTR items are protected from editing, automatic timestamp updates, and orange/yellow styling  
**Usage**: `python examples/demo_dattr.py`

### 📝 **demo_witheditor.py**
**Purpose**: Demonstrates the new witheditor command for external text editor integration  
**Features**: Shows how to edit item descriptions using system text editor (Notepad/nano) for longer content  
**Usage**: `python examples/demo_witheditor.py`

## 🚀 Running Examples

All demo scripts can be run from the project root:

```bash
# Run individual demos
python examples/demo_type_aliases.py
python examples/demo_terminal_editor.py
python examples/demo_features.py
python examples/demo_dattr.py
python examples/demo_witheditor.py
```

## 📚 What You'll Learn

These examples demonstrate:

- **Type Aliases**: How to use short type names (TIT, SUB, REQ, COM) for faster editing
- **Terminal Editor**: Interactive command-line interface for document editing with tab completion
- **DATTR Management**: Automatic timestamp handling, read-only protection, and visual styling
- **Document Creation**: How new documents are structured with metadata and default content
- **Save Operations**: How saving updates modification timestamps automatically
- **Smart Export**: Automatic filename derivation and flexible HTML export options
- **Visual Styling**: Orange/yellow DATTR styling with compact fonts for professional appearance
- **External Editor Integration**: How to use witheditor command for longer text editing with system text editor
- **Cross-Platform Support**: Windows (Notepad) and Unix-like systems (nano/$EDITOR) integration

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
