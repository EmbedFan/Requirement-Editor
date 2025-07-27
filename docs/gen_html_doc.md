# gen_html_doc.py Documentation

[← Back to Main README](../README.md) | [📚 Documentation Index](README.md) | [🔧 Main Module](main.md) | [🔍 Parsing Module](parse_req_md.md)

---

## Overview

The `gen_html_doc.py` module provides sophisticated HTML generation functionality for converting structured requirement elements into professional, interactive web documents with advanced styling, responsive design, and modern web features.

**Author:** Attila Gallai <attila@tux-net.hu>  
**Created:** 2025-07-09  
**Version:** 1.0.0  
**Location:** `libs/gen_html_doc.py`

## Enhanced Architecture

### Advanced HTML Generation System
The module implements a comprehensive template-based rendering system:

```
HTML Generation Pipeline
├── Template Management       # Default and custom stylesheet handling
├── Content Processing       # Element transformation and HTML escaping
├── Structure Assembly      # Hierarchical HTML document construction
├── Style Integration      # CSS embedding and responsive design
├── Script Integration     # JavaScript functionality and interactivity
└── Document Optimization  # Performance and accessibility enhancements
```

### Key Enhancements

#### **Sophisticated Template System**
- **Dual Template Mode**: Hardcoded default and external custom stylesheet support
- **Template Validation**: Comprehensive validation and error handling for custom templates
- **Fallback Mechanisms**: Graceful degradation when custom templates are unavailable
- **Dynamic Content Injection**: Intelligent placeholder replacement and content integration

#### **Advanced Interactive Features**
- **Modern JavaScript Implementation**: ES6+ syntax with backward compatibility
- **State Management**: Sophisticated expand/collapse state tracking
- **Event Handling**: Efficient event delegation and user interaction management
- **Performance Optimization**: Minimized DOM manipulation and efficient rendering

#### **Professional Web Design**
- **Responsive Framework**: Mobile-first design with progressive enhancement
- **Accessibility Support**: WCAG compliance and semantic HTML structure
- **Print Optimization**: Advanced CSS media queries for PDF generation
- **Cross-browser Compatibility**: Extensive testing and compatibility measures

#### **Enhanced Documentation**
- **Technical Specifications**: Detailed implementation documentation
- **Template Development Guide**: Custom stylesheet creation guidelines
- **Integration Patterns**: Best practices for module integration
- **Performance Guidelines**: Optimization techniques and recommendations
- **Responsive Design**: Works on various screen sizes
- **Modern Standards**: Uses current web technologies

### Visual Design
- **Color-coded Elements**: Different background colors for element types
- **Professional Typography**: Clean, readable font styling
- **Smooth Animations**: CSS transitions for better user experience
- **Visual Hierarchy**: Clear distinction between different element levels
- **Consistent Spacing**: Carefully designed margins and padding

## Element Type Styling

| Element Type | Background Color | Border Color | Special Features |
|--------------|-----------------|--------------|------------------|
| **TITLE** | White | Blue underline | Large font, not collapsible |
| **SUBTITLE** | Light gray (#ecf0f1) | Blue left border | Bold text, collapsible |
| **REQUIREMENT** | Light green (#e8f5e8) | Green left border | ID display, collapsible |
| **COMMENT** | Light yellow (#fff3cd) | Yellow left border | Italic text, collapsible |
| **DATTR** | Light yellow (#fffef5) | Orange border (#ff8c00) | Compact bold font (0.85em, weight 900), read-only |
| **UNKNOWN** | Light gray (#f8f9fa) | Gray left border | Standard formatting |

## Interactive Features

### Collapsible Sections
- **Click to Toggle**: Click any element (except titles) to expand/collapse
- **Visual Indicators**: Arrow icons show expand/collapse state
- **Smooth Animation**: CSS transitions provide smooth expand/collapse
- **Nested Support**: Proper handling of nested collapsible elements

### Control Buttons
- **Expand All**: Opens all collapsible sections at once
- **Collapse All**: Closes all collapsible sections at once
- **Toggle Line Numbers**: Show/hide line number references
- **Print to PDF**: Triggers browser print dialog

### Print Optimization
- **Hidden Controls**: All buttons automatically hidden during printing
- **Preserved Colors**: Background colors maintained in PDF output
- **Clean Layout**: Optimized spacing and formatting for print
- **Professional Appearance**: Print-ready styling

## Functions

### GenerateHTML(classified_parts, title="Requirement Document")

Generates a complete interactive HTML document from classified markdown parts.

**Parameters:**
- `classified_parts` (list): List of dictionaries containing classified parts from ClassifyParts function
- `title` (str, optional): Title for the HTML document. Defaults to "Requirement Document"

**Returns:**
- `str`: Complete HTML document as string with embedded CSS and JavaScript

**Required Dictionary Structure:**
```python
{
    'line_number': int,        # Original line number in source file
    'type': str,              # 'TITLE', 'SUBTITLE', 'REQUIREMENT', 'COMMENT', 'UNKNOWN'
    'indent': int,            # Indentation level (0, 1, 2, etc.)
    'id': int|None,           # Requirement/Comment ID number (if applicable)
    'description': str,       # Processed description text
    'children_refs': list     # List of direct references to child elements
}
```

**Generated HTML Structure:**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document Title</title>
    <style>/* Embedded CSS */</style>
</head>
<body>
    <div class="container">
        <!-- Control buttons added by JavaScript -->
        <!-- Document content -->
    </div>
    <script>/* Embedded JavaScript */</script>
</body>
</html>
```

**Features:**
- Complete self-contained HTML document
- No external dependencies required
- Embedded CSS for all styling
- Embedded JavaScript for interactivity
- Responsive design support
- Print optimization included

### _generate_hierarchical_content(classified_parts)

Generates hierarchical HTML content with proper parent-child nesting for collapsible elements.

**Parameters:**
- `classified_parts` (list): List of classified part dictionaries containing hierarchical structure

**Returns:**
- `str`: HTML content string with proper hierarchical nesting

**Processing Logic:**
1. Identifies root elements (parts with `parent=None`)
2. Delegates recursive HTML generation to `_generate_element_html()` for each root
3. Builds complete hierarchical structure

**Note:** This function only processes root elements directly, as child elements are handled recursively by their parents.

### _generate_element_html(part)

Generates HTML representation for a single element and recursively processes its children.

**Parameters:**
- `part` (dict): Part dictionary containing element information

**Returns:**
- `str`: HTML content string for the element and all its children

**Element Processing:**

#### TITLE Elements
```html
<div class="title indent-{level}">
    <span class="line-number">[{line_number}]</span>
    {escaped_description}
</div>
<!-- Children rendered directly (no collapsible container) -->
```

#### SUBTITLE Elements
```html
<div class="subtitle indent-{level} collapsible" onclick="toggleCollapse(this)">
    <span class="line-number">[{line_number}]</span>
    {escaped_description}
</div>
<div class="collapsible-content expanded" id="content-{line_number}">
    <!-- Child elements -->
</div>
```

#### REQUIREMENT Elements
```html
<div class="requirement indent-{level} collapsible" onclick="toggleCollapse(this)">
    <span class="line-number">[{line_number}]</span>
    <span class="req-id">{id} Req:</span>
    {escaped_description}
</div>
<div class="collapsible-content expanded" id="content-{line_number}">
    <!-- Child elements -->
</div>
```

#### COMMENT Elements
```html
<div class="comment indent-{level} collapsible" onclick="toggleCollapse(this)">
    <span class="line-number">[{line_number}]</span>
    <span class="req-id">{id} Comm:</span>
    {escaped_description}
</div>
<div class="collapsible-content expanded" id="content-{line_number}">
    <!-- Child elements -->
</div>
```

**Features:**
- Proper CSS class assignment for styling
- Line number references for traceability
- Recursive child processing
- Collapsible containers for all elements except titles
- HTML escaping for security

### _escape_html(text)

Escapes HTML special characters in text to prevent XSS attacks and ensure proper display.

**Parameters:**
- `text` (str): Raw text string that may contain HTML special characters

**Returns:**
- `str`: HTML-safe string with special characters converted to HTML entities

**Character Conversions:**
| Character | HTML Entity | Note |
|-----------|-------------|------|
| `&` | `&amp;` | Must be first to avoid double-escaping |
| `<` | `&lt;` | Less than |
| `>` | `&gt;` | Greater than |
| `"` | `&quot;` | Double quote |
| `'` | `&#39;` | Single quote/apostrophe |

**Security Importance:**
- Prevents XSS (Cross-Site Scripting) attacks
- Ensures safe rendering of user-generated content
- Essential for displaying external content in HTML

## CSS Classes and Styling

### Container Classes
- `.container`: Main document container with max-width and centering
- `.controls`: Control button container (hidden during print)

### Element Type Classes
- `.title`: Main titles with large font and blue underline
- `.subtitle`: Section headers with gray background
- `.requirement`: Requirements with green accent
- `.comment`: Comments with yellow accent and italic text
- `.unknown`: Unknown content with gray accent

### Indentation Classes
- `.indent-0` through `.indent-10`: Margin-left styling for hierarchy
- Each level adds 30px of left margin

### Interactive Classes
- `.collapsible`: Clickable elements with expand/collapse arrows
- `.collapsible.collapsed`: Collapsed state with rotated arrow
- `.collapsible-content`: Container for child elements
- `.collapsible-content.collapsed`: Hidden state with max-height: 0
- `.collapsible-content.expanded`: Visible state with max-height: 1000px

### Utility Classes
- `.line-number`: Line reference styling
- `.line-number.hidden`: Hidden line numbers
- `.req-id`: Requirement/comment ID styling

## JavaScript Functionality

### Core Functions

#### toggleCollapse(element)
Toggles the expand/collapse state of a single element.

**Parameters:**
- `element`: DOM element that was clicked

**Behavior:**
- Checks if element has `collapsible` class
- Toggles `collapsed` class on element
- Finds corresponding content div and toggles its state
- Updates arrow direction via CSS

#### expandAll()
Expands all collapsible elements in the document.

**Behavior:**
- Finds all elements with `collapsible` class
- Removes `collapsed` class from all elements
- Sets all content divs to `expanded` state

#### collapseAll()
Collapses all collapsible elements in the document.

**Behavior:**
- Finds all elements with `collapsible` class
- Adds `collapsed` class to all elements
- Sets all content divs to `collapsed` state

#### toggleLineNumbers()
Shows or hides line number references throughout the document.

**Behavior:**
- Finds all elements with `line-number` class
- Toggles `hidden` class on all line numbers
- Updates button text to reflect current state

#### printToPDF()
Triggers the browser's print dialog for PDF generation.

**Behavior:**
- Calls `window.print()`
- Browser applies print media queries automatically
- Control buttons hidden via CSS during print

### Initialization

The JavaScript includes a `DOMContentLoaded` event listener that:
1. Creates control button container with `controls` class
2. Adds all control buttons with inline styling
3. Inserts control container at the top of the document
4. Sets up click handlers for all functionality

## Print Media Queries

### Control Hiding
```css
@media print {
    .controls {
        display: none !important;
    }
}
```

### Color Preservation
```css
@media print {
    * {
        -webkit-print-color-adjust: exact !important;
        color-adjust: exact !important;
        print-color-adjust: exact !important;
    }
}
```

### Layout Optimization
```css
@media print {
    .container {
        box-shadow: none;
        border-radius: 0;
        margin: 0;
        padding: 10px;
        background-color: white !important;
    }
    
    body {
        margin: 0;
        background-color: white !important;
    }
}
```

## Browser Compatibility

### Modern Browser Features
- CSS Grid and Flexbox support
- CSS Variables (custom properties)
- ES6 JavaScript features
- Print media queries
- CSS transitions and transforms

### Supported Browsers
- Chrome 60+
- Firefox 60+
- Safari 12+
- Edge 79+

### Fallback Considerations
- Basic functionality works in older browsers
- CSS gracefully degrades without advanced features
- JavaScript uses standard DOM methods

## Performance Optimizations

### CSS Efficiency
- Minimal CSS with targeted selectors
- Hardware-accelerated CSS transforms
- Efficient cascade and specificity
- Optimized for fast rendering

### JavaScript Efficiency
- Event delegation where appropriate
- Minimal DOM queries
- Efficient element selection
- No external library dependencies

### HTML Structure
- Semantic HTML elements
- Minimal nested structures
- Efficient class usage
- Clean, valid markup

## Security Considerations

### XSS Prevention
- All user content passed through `_escape_html()`
- No unsafe innerHTML usage
- Controlled script execution
- Safe CSS class assignment

### Content Security
- No external resource dependencies
- Self-contained HTML documents
- Safe printing functionality
- Controlled user interactions

## Customization Options

### Styling Customization
Modify CSS variables in the embedded styles:
```css
:root {
    --primary-color: #3498db;
    --requirement-color: #e8f5e8;
    --comment-color: #fff3cd;
    --subtitle-color: #ecf0f1;
}
```

### Layout Customization
Adjust container and spacing:
```css
.container {
    max-width: 1200px;  /* Modify max width */
    padding: 20px;      /* Adjust padding */
}

.indent-1 { margin-left: 30px; }  /* Modify indentation */
```

### Color Customization
Change element background colors:
```css
.requirement { background-color: #custom-color; }
.comment { background-color: #custom-color; }
.subtitle { background-color: #custom-color; }
```

## Error Handling

### Input Validation
- Graceful handling of empty or None input
- Safe processing of malformed data structures
- Default values for missing dictionary keys
- Robust type checking

### Runtime Safety
- Protected against None values
- Safe string operations
- Defensive programming practices
- No unhandled exceptions

### Browser Compatibility
- Graceful degradation for unsupported features
- Safe JavaScript execution
- CSS fallbacks for older browsers
- Standard HTML compliance

## Usage Examples

### Basic Usage
```python
from libs.gen_html_doc import GenerateHTML

# Generate HTML from classified parts
html_content = GenerateHTML(classified_parts, "My Document")

# Save to file
with open("output.html", "w", encoding="utf-8") as f:
    f.write(html_content)
```

### Custom Title
```python
html_content = GenerateHTML(
    classified_parts, 
    "Project Requirements Specification v2.1"
)
```

### Error Handling
```python
try:
    html_content = GenerateHTML(classified_parts)
    if html_content:
        # Save or process HTML
        pass
except Exception as e:
    print(f"HTML generation failed: {e}")
```

## Integration Notes

### With Main Module
- Imported as: `from libs.gen_html_doc import GenerateHTML`
- Called after `ClassifyParts()` processing
- Output saved using `SaveHTMLFile()`

### Data Flow
1. Main module classifies markdown content
2. Classified parts passed to `GenerateHTML()`
3. Complete HTML document returned
4. HTML saved to file system

### Dependencies
- No external Python libraries required
- Uses only Python standard library features
- Self-contained HTML output
- No runtime dependencies for generated HTML

## Testing Considerations

### Unit Testing
- Test individual functions with various inputs
- Verify HTML structure correctness
- Check CSS class assignments
- Validate JavaScript functionality

### Integration Testing
- Test with real classified parts data
- Verify complete workflow
- Check browser rendering
- Test print functionality

### Edge Cases
- Empty input handling
- Malformed data structures
- Very deep hierarchies
- Large documents
- Special characters in content

## Future Enhancements

### Potential Improvements
- **Themes**: Multiple color schemes and layouts
- **Templates**: Customizable HTML templates
- **Plugins**: Extensible functionality system
- **Export Formats**: Additional output formats (Word, PDF direct)
- **Accessibility**: Enhanced screen reader support
- **Mobile**: Better mobile device optimization

---

[← Back to Main README](../README.md) | [📚 Documentation Index](README.md) | [🔧 Main Module](main.md) | [🔍 Parsing Module](parse_req_md.md)

**Last Updated:** 2025-07-09 14:40
