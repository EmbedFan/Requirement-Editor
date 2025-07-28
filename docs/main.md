# main.py Documentation

[← Back to Main README](../README.md) | [📚 Documentation Index](README.md) | [🔍 Parsing Module](parse_req_md.md) | [🎨 HTML Generation](gen_html_doc.md)

---

## Overview

The `main.py` module serves as the primary application orchestrator and command-line interface for the Requirement Editor, coordinating the complete workflow from markdown requirements parsing to interactive HTML document generation with advanced web features.

**Author:** Attila Gallai <attila@tux-net.hu>  
**Created:** 2025-07-09  
**Version:** 1.0.0  
**License:** MIT License

## Enhanced Architecture

### Application Orchestration
The module implements a sophisticated workflow management system that coordinates multiple specialized components:

```
Main Application Pipeline
├── Command Line Processing     # Argument parsing and validation
├── File Input Management      # UTF-8 markdown file reading
├── Document Parsing          # Element classification and hierarchy building
├── Console Reporting         # Detailed progress and debugging output
├── HTML Generation          # Template-based interactive document creation
└── File Output Management   # HTML writing with error handling
```

### Key Enhancements

#### **Comprehensive CLI Interface**
- **Help System**: Detailed usage information with examples and options
- **File Conversion**: Direct markdown-to-HTML conversion with path validation
- **Error Handling**: Graceful error recovery with informative messages
- **Exit Codes**: Proper system integration with shell scripting support

#### **Advanced Workflow Coordination**
- **Multi-stage Processing**: Coordinated pipeline with validation at each step
- **Progress Reporting**: Real-time feedback on processing status
- **Error Recovery**: Intelligent error handling with user guidance
- **Performance Optimization**: Efficient resource management and processing

#### **Enhanced Documentation**
- **Comprehensive Inline Documentation**: Detailed technical specifications
- **API Documentation**: Complete function and parameter references
- **Integration Examples**: Practical usage patterns and best practices
- **Error Scenarios**: Complete error handling documentation
│   ├── ClassifyParts()
│   └── _build_hierarchy()
├── libs.gen_html_doc (HTML Generation)
│   └── GenerateHTML()
└── SaveHTMLFile() (File Output)
```

## Document Structure Support

The application supports the following markdown document structures (parsed by `libs.parse_req_md`):

| Element Type | Pattern | Description |
|--------------|---------|-------------|
| **Titles** | Lines starting with '#' | Highest hierarchy level |
| **Subtitles** | Lines with `&nbsp;` indentation and `**bold**` formatting | Section headers |
| **Requirements** | Lines with `&nbsp;` + number + "Req:" pattern | Functional requirements |
| **Comments** | Lines with `&nbsp;` + number + "Comm:" pattern | Additional information (asterisks auto-removed) |
| **Unknown** | Any other content | Preserved with appropriate indentation |

## Indentation System

- **Rule**: Every 2 `&nbsp;` HTML entities = 1 indentation level
- **Hierarchy**: Parent-child relationships built using stack-based algorithm
- **Support**: Supports up to 10 indentation levels with CSS styling

## Configuration

```python
cfg_inputfile = "C:\\Munka\\Sandbox\\PromptEnginering\\Requirement Editor\\python\\test_input.md"
```

Modify this variable to change the input markdown file path.

## Usage

### Basic Usage
```bash
# Use default input file
python main.py

# Convert specific file (automatic .md extension)
python main.py -md2html requirements     # Finds requirements.md automatically
python main.py -md2html specs            # Finds specs.md automatically

# Direct file specification
python main.py -md2html requirements.md  # Use exact filename

# Interactive terminal editor
python main.py -ed                       # Start with new document
python main.py -ed requirements          # Load requirements.md automatically

# Help information
python main.py -h                        # Show detailed help
```

### Automatic File Extension Handling
The system includes smart file loading that automatically tries adding `.md` extension:

- **No Extension**: `requirements` → automatically tries `requirements.md`
- **Wrong Extension**: `requirements.txt` → tries `requirements.md` if `.txt` doesn't exist
- **Exact Match**: `requirements.md` → uses file as specified
- **Error Handling**: Shows helpful messages when files cannot be found

This feature works for both `-md2html` and `-ed` commands, implemented via the `process_filename_for_loading()` function.

## Dependencies

- `libs.parse_req_md`: Markdown parsing and classification functionality
- `libs.gen_html_doc`: HTML generation and styling functionality

## Functions

### process_filename_for_loading(filename)
**Purpose:** Automatically tries adding `.md` extension if file not found

**Parameters:**
- `filename` (str): The original filename provided by user

**Returns:**
- `str`: Valid filename that exists
- `None`: If no valid file found

**Logic:**
1. First tries the filename exactly as provided
2. If no extension provided, tries adding `.md`
3. If different extension provided, tries replacing with `.md`
4. Returns `None` if no valid file found

**Console Output:**
- "Info: File found with .md extension: {filename}" when extension added
- "Info: Found .md version: {filename}" when extension replaced

### SaveHTMLFile(html_content, filename)
**Features:**
- UTF-8 encoding for international character support
- Graceful error handling with descriptive console messages
- Automatic file closure even if write operation fails

### main()

Main entry point orchestrating the complete conversion workflow.

**Workflow:**
1. **File Reading**: Uses `ReadMDFile()` from `libs.parse_req_md` to read the input markdown file
2. **Content Parsing**: Uses `ClassifyParts()` from `libs.parse_req_md` to parse and classify document elements
3. **Console Display**: Shows detailed classification results for verification and debugging
4. **HTML Generation**: Uses `GenerateHTML()` from `libs.gen_html_doc` to create interactive HTML
5. **File Output**: Uses `SaveHTMLFile()` to save the result (same name as input but with .html extension)

**Console Output:**
- File reading success/failure messages with character counts
- Detailed classification table showing:
  - Line numbers and element types
  - Indentation levels and ID numbers
  - Parent-child relationships
  - Description text (truncated for readability)
- HTML generation and file saving status messages

**Error Handling:**
- Gracefully handles file reading errors from the parsing module
- Continues processing even if some steps fail
- Provides informative error messages to user
- Exits gracefully if critical steps fail

**Configuration:**
- Input file path specified in global variable `cfg_inputfile`
- Output file automatically determined by replacing .md with .html
- HTML document title set to "Requirement Document for Requirement Editor"

## Workflow Details

### Step 1: Markdown File Reading
```python
md_content = ReadMDFile(cfg_inputfile)
```
- Delegates to `libs.parse_req_md.ReadMDFile()`
- Handles UTF-8 encoding and error cases
- Provides character count feedback

### Step 2: Content Classification
```python
classified_parts = ClassifyParts(md_content)
```
- Delegates to `libs.parse_req_md.ClassifyParts()`
- Parses markdown into structured elements
- Builds hierarchical relationships

### Step 3: Console Verification Display
```python
for part in classified_parts:
    # Display detailed classification information
```
- Shows line-by-line classification results
- Displays parent-child relationships
- Truncates descriptions for readability
- Provides verification before HTML generation

### Step 4: HTML Generation
```python
html_content = GenerateHTML(classified_parts, "Requirement Document for Requirement Editor")
```
- Delegates to `libs.gen_html_doc.GenerateHTML()`
- Creates interactive HTML with CSS and JavaScript
- Includes expand/collapse functionality and control buttons

### Step 5: File Output
```python
html_filename = cfg_inputfile.replace('.md', '.html')
SaveHTMLFile(html_content, html_filename)
```
- Automatically determines output filename
- Saves with UTF-8 encoding
- Provides success/failure feedback

## Integration Points

### Module Dependencies
The main module coordinates between specialized modules:

**Parsing Module (`libs.parse_req_md`)**:
- `ReadMDFile()`: File input handling
- `ClassifyParts()`: Content parsing and classification

**HTML Generation Module (`libs.gen_html_doc`)**:
- `GenerateHTML()`: HTML document creation with styling and interactivity

**Local Functions**:
- `SaveHTMLFile()`: File output handling
- `main()`: Workflow orchestration

### Data Flow
```
Input File → ReadMDFile() → ClassifyParts() → GenerateHTML() → SaveHTMLFile() → Output File
     ↓              ↓              ↓              ↓              ↓
  cfg_inputfile  md_content  classified_parts  html_content  html_filename
```

## Console Output Example

```
Successfully read 1247 characters from C:\...\test_input.md

Classified 15 parts:
----------------------------------------------------------------------------------------------------
Line  1: Type: TITLE        | Indent: 0 | ID:  N/A | Parent: None | Children: [2, 5]
         Description: System Requirements...

Line  2: Type: SUBTITLE     | Indent: 1 | ID:  N/A | Parent: 1 | Children: [3, 4]
         Description: User Interface...

Line  3: Type: REQUIREMENT  | Indent: 2 | ID:    1 | Parent: 2 | Children: None
         Description: The system shall provide a login screen...

HTML file saved successfully: C:\...\test_input.html
```

## Output Features

The generated HTML includes:

- **Color-coded Element Types**:
  - Green: Requirements
  - Yellow: Comments
  - Blue: Subtitles
  - Dark blue: Titles

- **Interactive Features**:
  - Click-to-expand/collapse for all elements except titles
  - "Expand All" and "Collapse All" buttons
  - Line number toggle for reference/clean view switching
  - "Print to PDF" button for document export

- **Print Optimization**:
  - All control buttons hidden during printing
  - Background colors preserved in PDF output
  - Clean, professional printed appearance

## Example Usage

### Basic Application Run
```bash
# Run the complete conversion process
python main.py
```

### Programmatic Integration
```python
# Example of using the application components programmatically
from libs.parse_req_md import ReadMDFile, ClassifyParts
from libs.gen_html_doc import GenerateHTML
from main import SaveHTMLFile

# Read and process a markdown file
content = ReadMDFile("my_requirements.md")
if content:
    parts = ClassifyParts(content)
    html = GenerateHTML(parts, "My Requirements Document")
    
    # Save to file
    if SaveHTMLFile(html, "my_requirements.html"):
        print("Conversion completed successfully")
```

### Custom Configuration
```python
# Modify the input file configuration
import main
main.cfg_inputfile = "path/to/your/requirements.md"
main.main()  # Run with custom configuration
```

## Error Handling

The module implements comprehensive error handling by coordinating error responses from its dependencies:

### File Reading Errors (from libs.parse_req_md)
- **File Not Found**: Clear error message if input file doesn't exist
- **Permission Errors**: Graceful handling of file access issues
- **Encoding Issues**: UTF-8 encoding prevents character encoding problems

### Processing Errors
- **Empty Content**: Graceful handling when markdown file is empty
- **Malformed Input**: Continues processing with unknown classification for irregular content
- **Memory Issues**: Efficient processing delegation to specialized modules

### Output Errors (local handling)
- **Write Permissions**: Clear error messages for output file creation issues
- **Disk Space**: Proper error reporting for storage problems
- **Path Issues**: Handles invalid output path scenarios

## Performance Characteristics

### Workflow Efficiency
- **Minimal Overhead**: Main module adds negligible processing time
- **Memory Efficient**: No unnecessary data duplication between modules
- **Streaming Design**: Processes data through the pipeline efficiently

### Scalability
- **Large Documents**: Delegates heavy processing to optimized specialized modules
- **File Size Handling**: No artificial limits imposed by the orchestration layer
- **Resource Management**: Proper cleanup and resource handling throughout workflow

## Configuration Options

### Current Configuration
```python
cfg_inputfile = "C:\\Munka\\Sandbox\\PromptEnginering\\Requirement Editor\\python\\test_input.md"
```

### Future Configuration Enhancements
Potential configuration options for future versions:
- Output directory specification
- HTML template selection
- Custom CSS styling options
- Batch processing for multiple files
- Command-line argument support

## Module Relationships

### Dependency Graph
```
main.py
├── libs/parse_req_md.py
│   └── re (built-in)
└── libs/gen_html_doc.py
    └── (self-contained)
```

### Import Structure
```python
# Direct imports from specialized modules
from libs.parse_req_md import ReadMDFile, ClassifyParts
from libs.gen_html_doc import GenerateHTML

# Local function definitions
def SaveHTMLFile(html_content, filename): ...
def main(): ...
```

## Testing Strategy

### Integration Testing
The main module is ideal for integration testing:

```python
def test_complete_workflow():
    # Test the entire conversion process
    import main
    
    # Set test input
    main.cfg_inputfile = "test_requirements.md"
    
    # Run conversion
    main.main()
    
    # Verify output file exists and contains expected content
    assert os.path.exists("test_requirements.html")
```

### Unit Testing Components
```python
def test_save_html_file():
    # Test file saving functionality
    content = "<html><body>Test</body></html>"
    result = SaveHTMLFile(content, "test_output.html")
    assert result == True

def test_save_html_file_error():
    # Test error handling in file saving
    result = SaveHTMLFile("content", "/invalid/path/file.html")
    assert result == False
```

## Deployment Considerations

### File Structure Requirements
```
project/
├── main.py
├── libs/
│   ├── parse_req_md.py
│   └── gen_html_doc.py
└── requirements.md (input file)
```

### Environment Requirements
- **Python Version**: Compatible with Python 3.6+
- **File Permissions**: Read access to input files, write access to output directory
- **Encoding Support**: UTF-8 encoding support in the environment

### Distribution Package
For packaging the application:
```python
# setup.py considerations
install_requires=[
    # No external dependencies required
]

entry_points={
    'console_scripts': [
        'req-converter=main:main',
    ],
}
```

## Limitations and Design Decisions

### Current Limitations
- **Single File Processing**: Processes one markdown file at a time
- **Fixed Output Format**: HTML output format only
- **Console-Based Interface**: No GUI or web interface
- **Static Configuration**: Input file path must be modified in code

### Design Decisions
- **Modular Architecture**: Separation of concerns between parsing, generation, and orchestration
- **Console Output**: Detailed progress reporting for transparency and debugging
- **Error Tolerance**: Continues processing even with non-critical errors
- **UTF-8 Standard**: Consistent encoding throughout the workflow

## Future Enhancements

### Potential Improvements
- **Command-Line Interface**: Accept input file as command-line argument
- **Batch Processing**: Process multiple markdown files in one run
- **Configuration File**: External configuration for customization
- **Multiple Output Formats**: Support for PDF, Word, etc.
- **Real-Time Processing**: Watch file changes and auto-regenerate HTML
- **GUI Interface**: Desktop application with file browser and preview
- **Web Interface**: Browser-based conversion tool
- **Template System**: Customizable HTML templates
- **Plugin Architecture**: Extensible processing pipeline
- **Database Integration**: Store and manage requirement documents
- **Version Control**: Track changes in requirement documents
- **Collaborative Features**: Multi-user editing and commenting
- **Export Integration**: Direct integration with requirement management tools

### Architecture Evolution
- **Service-Oriented**: Convert to web service architecture
- **Microservices**: Separate parsing and generation into independent services
- **API Development**: RESTful API for programmatic access
- **Containerization**: Docker support for easy deployment
- **Cloud Integration**: Support for cloud storage and processing

## Conclusion

The `main.py` module serves as an effective orchestrator for the requirement document conversion process. Its clean separation of concerns, comprehensive error handling, and detailed user feedback make it a robust foundation for the application. The modular design facilitates future enhancements and makes the codebase maintainable and extensible.

---

[← Back to Main README](../README.md) | [📚 Documentation Index](README.md) | [🔍 Parsing Module](parse_req_md.md) | [🎨 HTML Generation](gen_html_doc.md)

**Last Updated:** 2025-07-09 14:40
