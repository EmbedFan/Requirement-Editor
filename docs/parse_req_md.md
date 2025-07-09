# parse_req_md.py Documentation

[← Back to Main README](../README.md) | [📚 Documentation Index](README.md) | [🔧 Main Module](main.md) | [🎨 HTML Generation](gen_html_doc.md)

---

## Overview

The `parse_req_md.py` module provides comprehensive functionality for parsing and classifying markdown-formatted requirement documents into structured hierarchical elements. This module is the core parsing engine that handles document structure analysis and hierarchy building.

**Author:** Attila Gallai <attila@tux-net.hu>  
**Created:** 2025  
**Last Updated:** 2025-07-09 14:40  
**Module Location:** `libs/parse_req_md.py`

## Key Features

- **Document Element Classification**: Identifies titles, subtitles, requirements, and comments
- **Hierarchical Structure Building**: Creates parent-child relationships based on indentation
- **Indentation Processing**: Handles HTML `&nbsp;` entities for precise indentation control
- **Comment Processing**: Automatically removes asterisk formatting from comments
- **Line Number Traceability**: Maintains references to original source line numbers
- **Robust Error Handling**: Graceful handling of file I/O operations and malformed input

## Document Structure Support

| Element Type | Pattern | Description | Indent Calculation |
|--------------|---------|-------------|-------------------|
| **TITLE** | Lines starting with '#' | Highest hierarchy level | Always indent = 0 |
| **SUBTITLE** | `&nbsp;` + `**text**` | Section headers | Based on `&nbsp;` count |
| **REQUIREMENT** | `&nbsp;` + number + "Req:" | Functional requirements | Based on `&nbsp;` count |
| **COMMENT** | `&nbsp;` + number + "Comm:" | Additional information | Based on `&nbsp;` count |
| **UNKNOWN** | Any other content | Preserved content | Based on `&nbsp;` count |

## Indentation System

- **Base Rule**: Every 2 `&nbsp;` HTML entities = 1 indentation level
- **Calculation**: `indent_level = nbsp_count // 2`
- **Hierarchy Building**: Uses stack-based algorithm for efficient parent-child relationships
- **Support Range**: Theoretically unlimited levels (CSS supports up to 10 for styling)

## Functions

### ReadMDFile(filename)

Reads a markdown file and returns its contents as a string with comprehensive error handling.

**Signature:**
```python
def ReadMDFile(filename: str) -> str | None
```

**Parameters:**
- `filename` (str): Path to the markdown file to read (absolute or relative path)

**Returns:**
- `str`: Complete file contents if successful
- `None`: If file cannot be read due to errors

**Features:**
- **UTF-8 Encoding**: Supports international characters commonly found in technical documentation
- **Error Handling**: Catches `FileNotFoundError` and `IOError` exceptions
- **User-Friendly Messages**: Prints descriptive error messages to console
- **No Exceptions**: Returns None instead of raising exceptions for easier integration

**Example Usage:**
```python
from libs.parse_req_md import ReadMDFile

content = ReadMDFile("requirements.md")
if content:
    print(f"Read {len(content)} characters")
else:
    print("Failed to read file")
```

### ClassifyParts(mdContent)

Main parsing function that analyzes markdown content and classifies document elements into structured hierarchy.

**Signature:**
```python
def ClassifyParts(mdContent: str) -> list[dict]
```

**Parameters:**
- `mdContent` (str): Complete markdown content as a string to analyze

**Returns:**
- `list`: List of dictionaries representing classified document elements
- `[]`: Empty list if input is None or empty

**Classification Process:**

1. **Line-by-Line Analysis**: Processes each line individually
2. **Empty Line Skipping**: Automatically skips blank lines
3. **Title Detection**: Identifies lines starting with '#'
4. **Indentation Counting**: Counts leading `&nbsp;` entities
5. **Pattern Matching**: Uses regex to identify requirements and comments
6. **Subtitle Recognition**: Detects `**bold**` formatted text
7. **Hierarchy Building**: Calls `_build_hierarchy()` to establish relationships

**Output Dictionary Structure:**
```python
{
    'line_number': int,        # Original line number (1-based)
    'original_line': str,      # Complete unmodified line text
    'type': str,              # 'TITLE', 'SUBTITLE', 'REQUIREMENT', 'COMMENT', 'UNKNOWN'
    'indent': int,            # Indentation level (0, 1, 2, etc.)
    'id': int|None,           # Requirement/Comment ID number if applicable
    'description': str,       # Processed description text
    'parent': int|None,       # Line number of parent element (None for root)
    'children': list,         # List of line numbers of direct children
    'parent_ref': dict|None,  # Direct reference to parent element object
    'children_refs': list     # List of direct references to child objects
}
```

**Classification Rules:**

- **TITLE Detection**: `line.strip().startswith('#')`
  - Removes '#' and strips whitespace for description
  - Always sets indent = 0

- **Requirement/Comment Detection**: 
  - Regex pattern: `r'^(\d+)\s+(Req|Comm):\s*(.+)$'`
  - Extracts ID number and description
  - For comments: removes surrounding '*' characters

- **Subtitle Detection**:
  - Regex pattern: `r'^\*\*(.+)\*\*$'`
  - Extracts text between double asterisks

- **Unknown Classification**:
  - Applied to any line that doesn't match other patterns
  - Preserves original text as description

**Example Input:**
```markdown
# System Requirements
&nbsp;&nbsp;**User Interface**
&nbsp;&nbsp;&nbsp;&nbsp;1 Req: The system shall provide a login screen
&nbsp;&nbsp;&nbsp;&nbsp;2 Comm: *Consider using OAuth for authentication*
&nbsp;&nbsp;**Database**
&nbsp;&nbsp;&nbsp;&nbsp;3 Req: The system shall store user data securely
```

**Example Output Structure:**
```
TITLE: "System Requirements" (indent=0, no parent)
├── SUBTITLE: "User Interface" (indent=1, parent=line_1)
│   ├── REQUIREMENT: "The system shall provide a login screen" (indent=2, id=1)
│   └── COMMENT: "Consider using OAuth for authentication" (indent=2, id=2)
└── SUBTITLE: "Database" (indent=1, parent=line_1)
    └── REQUIREMENT: "The system shall store user data securely" (indent=2, id=3)
```

### _build_hierarchy(parts)

Internal helper function that builds parent-child relationships between document elements using a stack-based algorithm.

**Signature:**
```python
def _build_hierarchy(parts: list[dict]) -> None
```

**Parameters:**
- `parts` (list): List of classified part dictionaries to process

**Returns:**
- `None`: Modifies the parts list in-place

**Algorithm Details:**

1. **Stack Initialization**: Creates empty stack for potential parents
2. **Element Processing**: Iterates through each classified element
3. **Stack Cleanup**: Removes parents at same or deeper indentation levels
4. **Parent Assignment**: Sets parent if stack contains elements
5. **Relationship Establishment**: Updates both parent and child references
6. **Stack Update**: Adds current element as potential parent

**Stack-Based Approach Benefits:**
- **Efficiency**: O(n) time complexity for entire hierarchy
- **Memory Efficient**: O(d) space complexity where d = maximum depth
- **Correct Nesting**: Handles irregular indentation patterns
- **Robust**: Works with skipped indentation levels

**Relationship Types Established:**
- `parent`: Line number of parent element
- `children`: List of line numbers of direct children
- `parent_ref`: Direct object reference to parent (for fast traversal)
- `children_refs`: List of direct object references to children

**Example Stack Operations:**
```
Input: [Title(0), Subtitle(1), Req(2), Req(2), Subtitle(1)]

Step 1: Title(0) - Stack: [Title(0)]
Step 2: Subtitle(1) - Stack: [Title(0), Subtitle(1)]
        Parent: Title(0) → Children: [Subtitle(1)]
Step 3: Req(2) - Stack: [Title(0), Subtitle(1), Req(2)]
        Parent: Subtitle(1) → Children: [Req(2)]
Step 4: Req(2) - Stack: [Title(0), Subtitle(1), Req(2)]
        Parent: Subtitle(1) → Children: [Req(2), Req(2)]
Step 5: Subtitle(1) - Stack pops Req(2), Stack: [Title(0), Subtitle(1)]
        Parent: Title(0) → Children: [Subtitle(1), Subtitle(1)]
```

## Usage Examples

### Basic Parsing
```python
from libs.parse_req_md import ReadMDFile, ClassifyParts

# Read and parse a markdown file
content = ReadMDFile("requirements.md")
if content:
    parts = ClassifyParts(content)
    
    # Display results
    for part in parts:
        print(f"Line {part['line_number']}: {part['type']} - {part['description']}")
```

### Hierarchy Traversal
```python
# Find all root elements (no parent)
root_elements = [part for part in parts if part['parent'] is None]

# Recursively print hierarchy
def print_hierarchy(element, depth=0):
    indent = "  " * depth
    print(f"{indent}{element['type']}: {element['description']}")
    
    for child in element['children_refs']:
        print_hierarchy(child, depth + 1)

for root in root_elements:
    print_hierarchy(root)
```

### Filtering by Type
```python
# Extract all requirements
requirements = [part for part in parts if part['type'] == 'REQUIREMENT']

# Extract all comments
comments = [part for part in parts if part['type'] == 'COMMENT']

# Count elements by type
type_counts = {}
for part in parts:
    type_counts[part['type']] = type_counts.get(part['type'], 0) + 1
```

## Error Handling

The module implements comprehensive error handling:

### File Reading Errors
- **FileNotFoundError**: Clear message when input file doesn't exist
- **IOError**: Graceful handling of permission issues, disk errors, etc.
- **Encoding Issues**: UTF-8 encoding prevents most character problems

### Input Validation
- **None Input**: Returns empty list for None or empty content
- **Malformed Lines**: Unknown classification preserves content
- **Missing Patterns**: Robust regex matching handles edge cases

### Memory Management
- **Large Files**: Efficient line-by-line processing
- **Deep Hierarchies**: Stack-based algorithm prevents recursion limits
- **Object References**: Circular references avoided through careful design

## Performance Characteristics

### Time Complexity
- **Line Processing**: O(n) where n = number of lines
- **Hierarchy Building**: O(n) stack-based algorithm
- **Overall**: O(n) linear scaling with input size

### Space Complexity
- **Element Storage**: O(n) for all classified elements
- **Hierarchy Stack**: O(d) where d = maximum indentation depth
- **References**: O(n) for parent/child relationships

### Scalability
- **Large Documents**: Handles thousands of requirements efficiently
- **Deep Nesting**: Supports arbitrarily deep hierarchies
- **Memory Efficient**: No unnecessary data duplication

## Integration Notes

### Module Dependencies
- **re**: Built-in Python regex module for pattern matching
- **No External Dependencies**: Self-contained parsing functionality

### Import Usage
```python
# Individual function imports
from libs.parse_req_md import ReadMDFile, ClassifyParts

# Full module import
import libs.parse_req_md as parser
content = parser.ReadMDFile("file.md")
parts = parser.ClassifyParts(content)
```

### Integration with HTML Generation
```python
# Typical workflow integration
from libs.parse_req_md import ReadMDFile, ClassifyParts
from libs.gen_html_doc import GenerateHTML

content = ReadMDFile("requirements.md")
parts = ClassifyParts(content)
html = GenerateHTML(parts, "Requirements Document")
```

## Limitations and Considerations

### Current Limitations
- **Indentation Format**: Requires `&nbsp;` entities (not regular spaces or tabs)
- **Comment Processing**: Basic asterisk removal (doesn't handle complex formatting)
- **ID Validation**: No checking for duplicate requirement/comment IDs
- **Line Length**: Very long lines may impact console output formatting

### Design Decisions
- **In-Place Modification**: `_build_hierarchy()` modifies input list for efficiency
- **Both References**: Maintains both line numbers and object references for flexibility
- **Error Tolerance**: Continues processing even with malformed input
- **Console Output**: Uses print statements for immediate user feedback

### Future Enhancement Opportunities
- **Flexible Indentation**: Support for spaces, tabs, and mixed indentation
- **Advanced Comment Processing**: Handle nested formatting and markdown syntax
- **Validation Framework**: ID uniqueness checking and requirement validation
- **Performance Optimization**: Streaming processing for very large files
- **Format Extensions**: Support for additional markdown patterns and structures

## Testing Recommendations

### Unit Test Coverage
```python
# Test cases to implement
def test_read_existing_file():
    # Test successful file reading
    
def test_read_nonexistent_file():
    # Test file not found handling
    
def test_classify_empty_content():
    # Test empty input handling
    
def test_classify_title_lines():
    # Test title detection and processing
    
def test_classify_requirements():
    # Test requirement pattern matching
    
def test_classify_comments():
    # Test comment processing and asterisk removal
    
def test_classify_subtitles():
    # Test subtitle pattern recognition
    
def test_build_simple_hierarchy():
    # Test basic parent-child relationships
    
def test_build_complex_hierarchy():
    # Test deep nesting and irregular patterns
```

### Integration Test Scenarios
- **Real Document Processing**: Test with actual requirement documents
- **Edge Case Handling**: Test with malformed or unusual markdown
- **Performance Testing**: Measure processing time for large documents
- **Memory Usage**: Monitor memory consumption during processing

---

[← Back to Main README](../README.md) | [📚 Documentation Index](README.md) | [🔧 Main Module](main.md) | [🎨 HTML Generation](gen_html_doc.md)

**Last Updated:** 2025-07-09 14:40
