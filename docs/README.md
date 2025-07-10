# Requirement Editor Documentation

[← Back to Main README](../README.md) | [🔧 Main Module](main.md) | [🔍 Parsing Module](parse_req_md.md) | [🎨 HTML Generation](gen_html_doc.md) | [📁 Project Config](project.md) | [⌨️ Terminal Editor](TERMINAL_EDITOR.md)

---

## Project Overview

The Requirement Editor is a sophisticated Python-based tool for converting markdown-formatted technical requirement documents into professional, interactive HTML documents with modern web features. The system implements a complete document processing pipeline with intelligent parsing, hierarchical structure building, and advanced HTML generation capabilities.

**Author:** Attila Gallai <attila@tux-net.hu>  
**Created:** 2025-07-09  
**Version:** 1.0.0  
**License:** MIT License

## Enhanced Documentation Structure

This documentation reflects the comprehensive inline documentation updates implemented across all core modules. Each module now includes detailed technical specifications, architectural overviews, and integration guidelines.

### Documentation Features
- **Comprehensive Technical Specifications**: Detailed algorithm and implementation documentation
- **API Documentation**: Complete function and class references with examples
- **Integration Guidelines**: Best practices for module integration and extension
- **Performance Analysis**: Optimization techniques and performance considerations
- **Error Handling**: Comprehensive error scenarios and recovery strategies

## Updated Project Structure

```
python/
├── main.py                    # Enhanced CLI interface with terminal editor support
├── demo_terminal_editor.py    # Demo script showcasing terminal editor usage
├── libs/
│   ├── parse_req_md.py       # Advanced parsing engine with sophisticated algorithms
│   ├── gen_html_doc.py       # Professional HTML generation with interactive features
│   ├── project.py            # Comprehensive configuration management system
│   ├── md_edit.py            # In-memory markdown editor for requirement documents
│   └── terminal_editor.py    # Interactive terminal-based editor for document editing
├── test/
│   ├── test_runner.py        # Automated test runner with HTML reporting
│   ├── test_cli.py           # Complete CLI interface testing suite
│   ├── test_project_config.py # Project configuration validation tests
│   ├── test_comprehensive.py # End-to-end integration testing
│   ├── test_simple.py        # Core functionality unit tests
│   ├── test_md_edit_line_based.py # Comprehensive md_edit.py testing suite
│   ├── test_md_edit_integration.py # Integration tests for md_edit.py
│   └── test_stylesheet_config.py # Stylesheet configuration testing
│   ├── data/
│   │   ├── test_input.md     # Sample requirement document for testing
│   │   └── test_input.html   # Generated HTML output (created by tests)
│   ├── results/              # Generated test reports directory
│   │   └── test_result_*.html # Timestamped HTML test reports
│   └── README.md             # Test directory documentation
├── docs/
│   ├── README.md             # This file - project overview
│   ├── main.md               # main.py documentation
│   ├── parse_req_md.md       # parse_req_md.py documentation
│   ├── gen_html_doc.md       # gen_html_doc.py documentation
│   ├── project.md            # project.py documentation
│   └── TERMINAL_EDITOR.md    # Terminal editor documentation and usage guide
└── LICENSE                   # MIT License file
```

## Quick Start

1. **Installation**: No external dependencies required - uses Python standard library only
2. **Configuration**: Edit `cfg_inputfile` in `main.py` to point to your markdown file
3. **Execution**: 
   - Standard processing: `python main.py`
   - Interactive terminal editor: `python main.py -ed`
4. **Output**: HTML file generated with same name as input but `.html` extension
5. **Testing**: Run `python test/test_runner.py` to execute all tests
6. **Demo**: Run `python demo_terminal_editor.py` to see terminal editor capabilities

## Testing

The project includes comprehensive testing capabilities:

### Running Tests
```bash
# Run all tests with the test runner
python test/test_runner.py

# Run individual test files
python test/test_project_config.py
```

### Test Structure
- **Unit Tests**: Individual module functionality testing
- **Integration Tests**: Full workflow validation  
- **Test Data**: Sample files in `test/data/` directory
- **Automated Runner**: Discovers and executes all tests

## System Architecture

### Modular Design
The application follows a clean modular architecture with separation of concerns:

```
main.py (Orchestrator)
├── libs/parse_req_md.py (Parsing Engine)
│   ├── ReadMDFile() - File input handling
│   ├── ClassifyParts() - Content parsing and classification
│   └── _build_hierarchy() - Hierarchy building
├── libs/gen_html_doc.py (HTML Generator)
│   └── GenerateHTML() - Interactive HTML creation
├── libs/project.py (Configuration Manager)
│   ├── ProjectConfig class - Project metadata management
│   ├── create_project_config() - New project creation
│   └── load_project_config() - Existing project loading
├── libs/md_edit.py (In-Memory Editor)
│   ├── MarkdownEditor class - Line number-based editing
│   ├── add_item_*() - Content insertion methods
│   ├── move_item_*() - Content movement methods
│   └── delete_item() - Content removal
├── libs/terminal_editor.py (Interactive Editor)
│   ├── TerminalEditor class - Command-line interface
│   ├── run() - Main editing loop
│   └── Command processing - File operations and navigation
└── SaveHTMLFile() - File output handling
```

### Data Flow
```
Input File → Read → Parse & Classify → Build Hierarchy → Generate HTML → Save Output
     ↓         ↓          ↓                ↓              ↓           ↓
test_input.md → ReadMDFile() → ClassifyParts() → _build_hierarchy() → GenerateHTML() → SaveHTMLFile()
```

### Module Responsibilities

| Module | Primary Responsibility | Key Functions |
|--------|----------------------|---------------|
| `main.py` | Workflow orchestration, console interface, terminal editor integration | `main()`, `SaveHTMLFile()` |
| `libs/parse_req_md.py` | Markdown parsing, content classification | `ReadMDFile()`, `ClassifyParts()`, `_build_hierarchy()` |
| `libs/gen_html_doc.py` | HTML generation, styling, interactivity | `GenerateHTML()` |
| `libs/md_edit.py` | In-memory document editing, line number-based operations | `MarkdownEditor class`, `add_item_*()`, `move_item_*()` |
| `libs/terminal_editor.py` | Interactive terminal-based editing interface | `TerminalEditor class`, `run()`, command processing |

## Features

### Document Processing
- **Multi-format Support**: Handles titles, subtitles, requirements, comments
- **Hierarchy Building**: Automatic parent-child relationships based on indentation
- **ID Management**: Preserves requirement and comment ID numbers
- **Comment Processing**: Automatic removal of asterisk formatting

### HTML Output
- **Interactive Elements**: Expand/collapse functionality for sections
- **Professional Styling**: Color-coded element types with modern CSS
- **Control Interface**: Buttons for expand all, collapse all, line number toggle, print
- **Print Optimization**: Clean PDF output with preserved colors and hidden controls

### Technical Features
- **Self-contained**: Generated HTML has no external dependencies
- **Responsive Design**: Works on various screen sizes
- **Security**: XSS protection through HTML escaping
- **Performance**: Efficient O(n) algorithms for large documents

### Editing Capabilities
- **In-Memory Editing**: Advanced markdown document manipulation using `md_edit.py`
- **Line Number-Based Operations**: Precise positioning and referencing system
- **Terminal Interface**: Interactive command-line editor accessible via `main.py -ed`
- **Hierarchical Operations**: Move, add, delete items while maintaining document structure
- **Real-time Updates**: Immediate reflection of changes in document structure
- **Command Set**: Comprehensive editing commands for all document operations

## Supported Markdown Syntax

### Document Structure
The system recognizes specific markdown patterns for different element types:

#### Titles
```markdown
# Document Title
```
- Creates highest-level headers
- Always at indent level 0
- Not collapsible in HTML output

#### Subtitles
```markdown
&nbsp;&nbsp;**Section Title**
```
- Uses `&nbsp;` entities for indentation
- Bold formatting with `**text**`
- Collapsible in HTML output

#### Requirements
```markdown
&nbsp;&nbsp;&nbsp;&nbsp;1001 Req: The system shall do something.
```
- Format: `{indentation}{number} Req: {description}`
- Number becomes the requirement ID
- Green styling in HTML output

#### Comments
```markdown
&nbsp;&nbsp;&nbsp;&nbsp;1002 Comm: *Additional information about the requirement.*
```
- Format: `{indentation}{number} Comm: *{description}*`
- Asterisks automatically removed from description
- Yellow styling in HTML output

### Indentation Rules
- **2 `&nbsp;` entities = 1 indentation level**
- **Maximum 10 levels supported**
- **Determines parent-child relationships**

## Example Document

Here's a sample markdown document showing the supported syntax:

```markdown
# Project Requirements

&nbsp;&nbsp;1000 Comm: *This is a project overview comment.*

&nbsp;&nbsp;**Database Requirements**
&nbsp;&nbsp;&nbsp;&nbsp;1001 Req: The system shall use a database for storage.
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1002 Comm: *SQLite is recommended for simplicity.*
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1003 Req: Data shall be stored in UTF-8 format.

&nbsp;&nbsp;**User Interface Requirements**
&nbsp;&nbsp;&nbsp;&nbsp;1010 Req: The UI shall be responsive and modern.
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1011 Req: All buttons shall have hover effects.
```

This generates a hierarchical HTML structure with:
- Title at top level
- Two main sections (Database and UI Requirements)
- Requirements under each section
- Comments providing additional context

## Configuration Options

### File Paths
```python
# In main.py
cfg_inputfile = "path/to/your/requirements.md"
```

### HTML Customization
The HTML generation can be customized by modifying the CSS in `libs/gen_html_doc.py`:

```css
/* Element colors */
.requirement { background-color: #e8f5e8; }  /* Light green */
.comment { background-color: #fff3cd; }      /* Light yellow */
.subtitle { background-color: #ecf0f1; }     /* Light gray */

/* Indentation levels */
.indent-1 { margin-left: 30px; }
.indent-2 { margin-left: 60px; }
/* ... up to indent-10 */
```

## Output HTML Features

### Interactive Elements
- **Click to Toggle**: Click any element (except titles) to expand/collapse
- **Visual Feedback**: Arrow indicators show expand/collapse state
- **Smooth Animation**: CSS transitions provide professional feel

### Control Buttons
- **Expand All**: Opens all collapsible sections
- **Collapse All**: Closes all collapsible sections  
- **Toggle Line Numbers**: Show/hide line references
- **Print to PDF**: Opens browser print dialog

### Print Features
- **Hidden Controls**: Buttons automatically hidden during printing
- **Color Preservation**: Background colors maintained in PDF
- **Clean Layout**: Optimized spacing for professional documents
- **Cross-browser**: Works with Chrome, Firefox, Safari, Edge

## Error Handling

The system includes comprehensive error handling:

### File Operations
- **Missing Files**: Clear error messages for non-existent input files
- **Permission Issues**: Graceful handling of read/write permissions
- **Encoding Problems**: UTF-8 support prevents character issues

### Data Processing
- **Malformed Input**: Robust parsing handles irregular markdown
- **Empty Documents**: Safe handling of empty or whitespace-only files
- **Invalid Patterns**: Unknown content preserved as UNKNOWN type

### HTML Generation
- **XSS Prevention**: All content properly escaped
- **Browser Compatibility**: Graceful degradation for older browsers
- **Memory Management**: Efficient processing for large documents

## Performance Characteristics

### Scalability
- **Linear Complexity**: O(n) processing for n input lines
- **Memory Efficient**: Processes line-by-line without full loading
- **Fast Rendering**: Generated HTML optimized for browser performance

### Benchmarks
Typical performance on modern hardware:
- **Small Documents** (< 100 requirements): < 1 second
- **Medium Documents** (100-1000 requirements): 1-5 seconds
- **Large Documents** (1000+ requirements): 5-30 seconds

### Limitations
- **Maximum Depth**: 10 indentation levels (CSS limitation)
- **Memory Usage**: Full document hierarchy kept in memory
- **Browser Limits**: Very large HTML may impact browser performance

## Development Guidelines

### Code Style
- **PEP 8 Compliance**: Python code follows standard conventions
- **Documentation**: Comprehensive docstrings for all functions
- **Error Handling**: Graceful degradation and informative messages
- **Security**: Input validation and XSS prevention

### Testing Approach
- **Unit Tests**: Individual function testing
- **Integration Tests**: Full workflow validation
- **Manual Testing**: Real-world document processing
- **Performance Tests**: Large document handling

### Contribution Guidelines
- Follow existing code style and patterns
- Add comprehensive documentation for new features
- Include error handling and validation
- Test with various document sizes and formats

## Troubleshooting

### Common Issues

#### File Not Found
- **Error**: `FileNotFoundError: [Errno 2] No such file or directory`
- **Solution**: Verify `cfg_inputfile` path in `main.py`
- **Check**: File permissions and accessibility

#### Empty Output
- **Cause**: No recognized content patterns in input
- **Solution**: Verify markdown follows supported syntax
- **Debug**: Check console output for classification results

#### HTML Not Interactive
- **Cause**: JavaScript disabled or browser restrictions
- **Solution**: Enable JavaScript in browser settings
- **Alternative**: Static view still provides document structure

#### Print Colors Not Showing
- **Cause**: Browser print settings
- **Solution**: Enable "Background graphics" in print options
- **Alternative**: Use "Print to PDF" for better color preservation

### Debug Information

The system provides detailed console output:
```
Successfully read 2847 characters from test_input.md

Classified 15 parts:
----------------------------------------------------------------------------------------------------
Line  1: Type: TITLE        | Indent: 0 | ID:  N/A | Parent: None | Children: [2, 3]
         Description: Requirement document for Requirement Editor...

Line  2: Type: COMMENT      | Indent: 1 | ID: 1030 | Parent: 1 | Children: None
         Description: This project is for providing application to writing requirement documents...
```

This output helps identify parsing issues and verify document structure.

## Future Development

### Planned Features
- **Database Integration**: SQLite storage for requirement persistence
- **Version Control**: Git integration for requirement versioning
- **Collaborative Editing**: Multi-user editing capabilities
- **Advanced Export**: Word, PDF direct export options
- **Template System**: Customizable HTML templates

### Enhancement Ideas
- **Real-time Preview**: Live HTML update during editing
- **Requirement Validation**: Automated quality checks
- **Traceability Matrix**: Requirement relationship tracking
- **Test Integration**: Link requirements to test cases
- **Reporting**: Advanced analytics and metrics

### Architecture Improvements
- **Plugin System**: Extensible functionality framework
- **API Development**: RESTful service for remote access
- **Cloud Integration**: Online storage and collaboration
- **Mobile Support**: Responsive design improvements

---

[← Back to Main README](../README.md) | [🔧 Main Module](main.md) | [🔍 Parsing Module](parse_req_md.md) | [🎨 HTML Generation](gen_html_doc.md) | [📁 Project Config](project.md) | [⌨️ Terminal Editor](TERMINAL_EDITOR.md)

*Documentation generated for Requirement Editor v1.0.0*  
*Last updated: 2025-07-10 (Terminal Editor Integration)*
