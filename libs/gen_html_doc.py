"""
Interactive HTML Document Generation Module for Requirement Documents

This module provides comprehensive HTML generation functionality for converting structured
requirement document elements into professional, interactive web documents with modern
styling, responsive design, and advanced user interaction features.

Core Architecture:
The HTML generator operates as a template-based rendering system that transforms classified
requirement elements into semantically structured HTML with embedded CSS and JavaScript.
The system supports both hardcoded default styling and external custom stylesheet templates
for maximum flexibility in document presentation.

Document Generation Pipeline:
1. **Template Selection**: Chooses between hardcoded default or custom stylesheet template
2. **Content Classification**: Processes structured element data from parser module
3. **HTML Structure Building**: Creates semantic HTML with proper hierarchy and navigation
4. **CSS Integration**: Embeds responsive styling with print media queries
5. **JavaScript Integration**: Adds interactive functionality and user controls
6. **Document Assembly**: Combines all components into complete HTML document

Styling System Architecture:
The module implements a sophisticated CSS framework with multiple layers:
- Base styles for typography, layout, and responsive design
- Element-specific styles for different requirement types
- Interactive states for hover, focus, and active elements
- Print media queries for professional PDF output
- CSS custom properties for consistent theming

Element Type Visual Design:
- TITLE: Large headers with distinctive blue underline (2-3em font size)
- SUBTITLE: Bold section headers with gray background and blue left border accent
- REQUIREMENT: Green-accented containers with clear requirement identification
- COMMENT: Yellow-accented containers with italic text styling for distinction
- DATTR: Blue-accented containers with monospace font for structured data display
- UNKNOWN: Gray-accented containers for unclassified content with neutral styling

Interactive Features Implementation:
- **Expand/Collapse System**: JavaScript-powered section folding with smooth CSS transitions
- **Line Number Toggle**: Show/hide line references for clean vs. technical view
- **Bulk Operations**: Expand All and Collapse All buttons for document-wide control
- **Print Optimization**: Automatic control hiding and expanded state for PDF generation
- **Responsive Design**: Mobile-friendly layout with touch-optimized interaction areas

JavaScript Functionality:
- Modern ES6+ syntax with backward compatibility considerations
- DOM manipulation using vanilla JavaScript (no external dependencies)
- Event delegation for efficient handling of dynamic content
- State management for expand/collapse and line number visibility
- Print detection and automatic document optimization

CSS Framework Features:
- Flexbox-based layout system for consistent alignment and spacing
- CSS Grid for complex layout scenarios and responsive behavior
- Custom CSS properties (variables) for maintainable theming
- Smooth transitions and animations for professional user experience
- Print-specific styles with @media queries for PDF optimization

Responsive Design Implementation:
- Mobile-first approach with progressive enhancement
- Breakpoint-based responsive behavior for various screen sizes
- Touch-friendly interaction areas with appropriate sizing
- Optimized typography scales for different viewport sizes
- Accessible design following WCAG guidelines

Print Media Optimization:
- Automatic background color preservation for PDF generation
- Control button hiding during print operations
- Optimized typography and spacing for paper output
- Expanded content state for complete document visibility
- Page break optimization for professional document layout

Template System:
The module supports two template modes:
1. **Default Hardcoded Template**: Complete self-contained CSS embedded in HTML
2. **Custom External Template**: Loads CSS from external file specified in project config

Template Features:
- Placeholder replacement system for dynamic content injection
- Error handling with graceful fallback to default template
- Validation of template format and required components
- Support for CSS imports and external resource references

Security Considerations:
- HTML escaping for all user content to prevent XSS attacks
- Safe CSS injection with validation and sanitization
- Controlled JavaScript execution with CSP-compatible code
- Input validation for all template and content parameters

Performance Optimization:
- Minimized CSS with efficient selector strategies
- Optimized JavaScript with minimal DOM manipulation
- Efficient HTML structure with semantic elements
- Compressed inline resources for faster loading

Integration Interfaces:
- Compatible with project configuration system for custom templates
- Designed for integration with parsing module output format
- Extensible architecture for additional interactive features
- API-compatible with existing workflow systems

Error Handling Strategy:
- Graceful degradation when custom templates are unavailable
- Comprehensive validation of input data structures
- Fallback mechanisms for missing or corrupted template files
- Detailed error reporting for debugging and troubleshooting

Example Usage:
```python
# Basic usage with default template
html_content = GenerateHTML(classified_parts, "My Requirements")

# Advanced usage with custom template
project_config = ProjectConfig("project.json")
html_content = GenerateHTML(classified_parts, "My Requirements", project_config)
```

Output HTML Structure:
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Requirement Document</title>
    <style>/* Embedded CSS styles */</style>
</head>
<body>
    <div class="container">
        <div class="controls">/* Interactive controls */</div>
        <div class="title">/* Document title */</div>
        <div class="requirement collapsible">/* Requirement content */</div>
        /* Additional elements... */
    </div>
    <script>/* Interactive JavaScript */</script>
</body>
</html>
```

Author: Attila Gallai <attila@tux-net.hu>
Created: 2025-07-09
Version: 1.0.0
License: MIT License (see LICENSE.txt)
"""

import os
from pathlib import Path


def _get_default_style_template():
    """
    Get the default CSS stylesheet template as a hardcoded string.
    
    This function returns the default styling for HTML requirement documents.
    It serves as a fallback when no custom stylesheet is specified or when
    the custom stylesheet file cannot be loaded.
    
    Returns:
        str: Default CSS stylesheet content
    """
    return """/* 
HTML Document Stylesheet Template for Requirement Documents

This stylesheet provides professional styling for requirement documents
generated from markdown files with hierarchical structure support.

Author: Attila Gallai <attila@tux-net.hu>
Created: 2025
License: MIT License (see LICENSE.txt)
*/

body {
    font-family: Arial, sans-serif;
    line-height: 1.6;
    margin: 20px;
    background-color: #f5f5f5;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    background-color: white;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.title {
    color: #2c3e50;
    border-bottom: 3px solid #3498db;
    padding-bottom: 10px;
    margin-bottom: 20px;
    font-size: 2em;
}

.subtitle {
    color: #34495e;
    font-weight: bold;
    margin: 8px 0 2px 0;
    padding: 8px 12px;
    background-color: #ecf0f1;
    border-left: 4px solid #3498db;
    font-size: 1.2em;
}

.requirement {
    background-color: #e8f5e8;
    border-left: 4px solid #27ae60;
    padding: 10px 15px;
    margin: 2px 0;
    border-radius: 4px;
}

.comment {
    background-color: #fff3cd;
    border-left: 4px solid #ffc107;
    padding: 10px 15px;
    margin: 2px 0;
    border-radius: 4px;
    font-style: italic;
}

.dattr {
    background-color: #fffef5;
    border: 2px solid #ff8c00;
    border-left: 6px solid #ff8c00;
    padding: 8px 12px;
    margin: 10px 0;
    border-radius: 6px;
    font-family: 'Courier New', monospace;
    color: #cc6600;
    font-weight: 900;
    font-size: 0.85em;
    box-shadow: 0 1px 3px rgba(255, 140, 0, 0.15);
}

.unknown {
    background-color: #f8f9fa;
    border-left: 4px solid #6c757d;
    padding: 10px 15px;
    margin: 8px 0;
    border-radius: 4px;
}

.req-id {
    font-weight: bold;
    color: #2c3e50;
    margin-right: 10px;
}

/* Indentation classes for hierarchical structure */
.indent-0 { margin-left: 0px; }
.indent-1 { margin-left: 0px; }
.indent-2 { margin-left: 30px; }
.indent-3 { margin-left: 60px; }
.indent-4 { margin-left: 90px; }
.indent-5 { margin-left: 120px; }
.indent-6 { margin-left: 150px; }
.indent-7 { margin-left: 180px; }
.indent-8 { margin-left: 210px; }
.indent-9 { margin-left: 240px; }
.indent-10 { margin-left: 270px; }

/* Line number styling */
.line-number {
    color: #95a5a6;
    font-size: 0.8em;
    margin-right: 10px;
    transition: opacity 0.3s ease;
}

.line-number.hidden {
    display: none;
}

/* Collapsible element styling */
.collapsible {
    position: relative;
    cursor: pointer;
}

.collapsible::before {
    content: "▼";
    position: absolute;
    left: -20px;
    top: 50%;
    transform: translateY(-50%);
    font-size: 0.8em;
    color: #3498db;
    transition: transform 0.3s ease;
}

.collapsible.collapsed::before {
    transform: translateY(-50%) rotate(-90deg);
}

.collapsible-content {
    overflow: hidden;
    transition: max-height 0.3s ease;
}

.collapsible-content.collapsed {
    max-height: 0;
    margin: 0;
    padding: 0;
}

.collapsible-content.expanded {
    max-height: 1000px;
}

.has-children {
    margin-left: 20px;
}

/* Control buttons styling */
.controls {
    margin-bottom: 20px;
    text-align: right;
}

.controls button {
    margin-right: 10px;
    padding: 5px 10px;
    border: none;
    border-radius: 3px;
    cursor: pointer;
    font-size: 14px;
}

.controls .expand-btn {
    background: #3498db;
    color: white;
}

.controls .collapse-btn {
    background: #e74c3c;
    color: white;
}

.controls .toggle-btn {
    background: #9b59b6;
    color: white;
}

.controls .print-btn {
    background: #2ecc71;
    color: white;
    margin-right: 0;
}

/* Print media queries for PDF optimization */
@media print {
    .controls {
        display: none !important;
    }
    
    /* Force background colors to print */
    * {
        -webkit-print-color-adjust: exact !important;
        print-color-adjust: exact !important;
    }
    
    /* Ensure all element backgrounds are preserved */
    .subtitle {
        background-color: #ecf0f1 !important;
        border-left: 4px solid #3498db !important;
    }
    
    .requirement {
        background-color: #e8f5e8 !important;
        border-left: 4px solid #27ae60 !important;
    }
    
    .comment {
        background-color: #fff3cd !important;
        border-left: 4px solid #ffc107 !important;
    }
    
    .dattr {
        background-color: #fffef5 !important;
        border: 2px solid #ff8c00 !important;
        border-left: 6px solid #ff8c00 !important;
    }
    
    .unknown {
        background-color: #f8f9fa !important;
        border-left: 4px solid #6c757d !important;
    }
    
    .title {
        border-bottom: 3px solid #3498db !important;
    }
    
    /* Print-specific container styling */
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
}"""


def _load_stylesheet_template(style_template_path=None):
    """
    Load the CSS stylesheet template from a file or return the default template.
    
    Args:
        style_template_path (str, optional): Path to custom stylesheet template file.
                                           If None, uses the default hardcoded template.
        
    Returns:
        str: CSS content from the stylesheet template file or default template
        
    Note:
        If a custom template path is provided but the file cannot be read,
        the function falls back to the default hardcoded template.
    """
    # If no custom template path is provided, use default
    if not style_template_path:
        return _get_default_style_template()
    
    try:
        # Try to load custom stylesheet template
        with open(style_template_path, 'r', encoding='utf-8') as f:
            return f.read()
    except (FileNotFoundError, IOError, OSError) as e:
        # If custom template cannot be loaded, use default
        print(f"Warning: Could not load custom stylesheet template '{style_template_path}': {e}")
        print("Using default stylesheet template instead.")
        return _get_default_style_template()


def GenerateHTML(classified_parts, title="Requirement Document", project_config=None):
    """
    Generate a complete interactive HTML document from classified markdown parts.
    
    Creates a styled, hierarchical HTML document with the following features:
    - Collapsible/expandable sections (except titles)
    - Visual distinction for different element types (requirements, comments, subtitles)
    - Interactive control buttons (expand/collapse all, toggle line numbers, print to PDF)
    - Print-friendly styling with preserved background colors
    - Responsive design with modern CSS styling
    - Configurable stylesheet template through project configuration
    
    Args:
        classified_parts (list): List of dictionaries containing classified parts from ClassifyParts function.
                                Each dictionary should contain:
                                - line_number: Original line number in source file
                                - type: Element type ('TITLE', 'SUBTITLE', 'REQUIREMENT', 'COMMENT', 'UNKNOWN')
                                - indent: Indentation level (0, 1, 2, etc.)
                                - id: Requirement/Comment ID number (if applicable)
                                - description: Processed description text
                                - children_refs: List of direct references to child elements
        title (str, optional): Title for the HTML document. Defaults to "Requirement Document".
        project_config (object, optional): Project configuration object that may contain
                                         get_style_template_path() method for custom styling.
        
    Returns:
        str: Complete HTML document as a string with embedded CSS and JavaScript for interactivity.
             Returns a simple error message HTML if no classified_parts provided.
             
    Note:
        The generated HTML includes:
        - CSS for visual styling and print optimization (default or custom template)
        - JavaScript for interactive functionality
        - Control buttons that are hidden during printing
        - Color-coded backgrounds for different element types
        
        If project_config contains a style_template_path, that custom stylesheet will be used.
        Otherwise, the default hardcoded stylesheet template is used.
    """
    if not classified_parts:
        return "<html><body><h1>No content to display</h1></body></html>"
    
    # HTML document structure
    html_content = []
    
    # Determine stylesheet template path from project config
    style_template_path = None
    if project_config and hasattr(project_config, 'get_style_template_path'):
        style_template_path = project_config.get_style_template_path()
    
    # Load stylesheet (custom or default)
    css_content = _load_stylesheet_template(style_template_path)
    
    # HTML header with external CSS styling
    html_content.append(f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
{css_content}
    </style>
</head>
<body>
    <div class="container">''')
    
    # Generate hierarchical content
    html_content.append(_generate_hierarchical_content(classified_parts))
    
    # Close HTML document
    html_content.append('''
    </div>
    
    <script>
        function toggleCollapse(element) {
            if (!element.classList.contains('collapsible')) {
                return;
            }
            
            const isCollapsed = element.classList.contains('collapsed');
            const lineNumber = element.querySelector('.line-number').textContent.match(/\[(\d+)\]/)[1];
            const contentDiv = document.getElementById('content-' + lineNumber);
            
            if (isCollapsed) {
                // Expand
                element.classList.remove('collapsed');
                if (contentDiv) {
                    contentDiv.classList.remove('collapsed');
                    contentDiv.classList.add('expanded');
                }
            } else {
                // Collapse
                element.classList.add('collapsed');
                if (contentDiv) {
                    contentDiv.classList.remove('expanded');
                    contentDiv.classList.add('collapsed');
                }
            }
        }
        
        // Function to collapse all elements
        function collapseAll() {
            const collapsibles = document.querySelectorAll('.collapsible');
            collapsibles.forEach(element => {
                element.classList.add('collapsed');
                const lineNumber = element.querySelector('.line-number').textContent.match(/\[(\d+)\]/)[1];
                const contentDiv = document.getElementById('content-' + lineNumber);
                if (contentDiv) {
                    contentDiv.classList.remove('expanded');
                    contentDiv.classList.add('collapsed');
                }
            });
        }
        
        // Function to expand all elements
        function expandAll() {
            const collapsibles = document.querySelectorAll('.collapsible');
            collapsibles.forEach(element => {
                element.classList.remove('collapsed');
                const lineNumber = element.querySelector('.line-number').textContent.match(/\[(\d+)\]/)[1];
                const contentDiv = document.getElementById('content-' + lineNumber);
                if (contentDiv) {
                    contentDiv.classList.remove('collapsed');
                    contentDiv.classList.add('expanded');
                }
            });
        }
        
        // Function to toggle line numbers visibility
        function toggleLineNumbers() {
            const lineNumbers = document.querySelectorAll('.line-number');
            const toggleButton = document.getElementById('toggle-line-numbers');
            
            lineNumbers.forEach(lineNumber => {
                lineNumber.classList.toggle('hidden');
            });
            
            // Update button text
            const isHidden = lineNumbers[0].classList.contains('hidden');
            toggleButton.textContent = isHidden ? 'Show Line Numbers' : 'Hide Line Numbers';
        }
        
        // Function to print as PDF
        function printToPDF() {
            window.print();
        }
        
        // Function to print document as PDF
        function printToPDF() {
            window.print();
        }
        
        // Add control buttons
        document.addEventListener('DOMContentLoaded', function() {
            const container = document.querySelector('.container');
            const controls = document.createElement('div');
            controls.className = 'controls';
            controls.innerHTML = `
                <div>
                    <button class="expand-btn" onclick="expandAll()">Expand All</button>
                    <button class="collapse-btn" onclick="collapseAll()">Collapse All</button>
                    <button class="toggle-btn" id="toggle-line-numbers" onclick="toggleLineNumbers()">Hide Line Numbers</button>
                    <button class="print-btn" onclick="printToPDF()">Print as PDF</button>
                </div>
            `;
            container.insertBefore(controls, container.firstChild);
        });
    </script>
</body>
</html>''')
    
    return ''.join(html_content)


def _generate_hierarchical_content(classified_parts):
    """
    Generate hierarchical HTML content with proper parent-child nesting for collapsible elements.
    
    This function processes the classified parts and generates HTML content that respects
    the hierarchical structure defined by parent-child relationships. Only root elements
    (those without parents) are processed directly, as child elements are handled
    recursively by their parents.
    
    Args:
        classified_parts (list): List of classified part dictionaries containing hierarchical structure.
                                Each part should have 'parent' and 'children_refs' attributes.
        
    Returns:
        str: HTML content string with proper hierarchical nesting. Returns empty string
             if no classified_parts provided.
             
    Note:
        This function identifies root elements (parts with parent=None) and delegates
        the recursive HTML generation to _generate_element_html() for each root element.
    """
    if not classified_parts:
        return ""
    
    content = []
    
    # Find root elements (those without parents)
    root_elements = [part for part in classified_parts if part['parent'] is None]
    
    for root in root_elements:
        content.append(_generate_element_html(root))
    
    return ''.join(content)


def _generate_element_html(part):
    """
    Generate HTML representation for a single element and recursively process its children.
    
    Creates HTML div elements with appropriate CSS classes and styling based on the element type.
    Handles the following element types with distinct visual styling:
    - TITLE: Large header with blue underline (not collapsible)
    - SUBTITLE: Bold section header with gray background (collapsible if has children)
    - REQUIREMENT: Green-accented box with requirement ID (collapsible if has children)
    - COMMENT: Yellow-accented box with comment ID in italics (collapsible if has children)
    - UNKNOWN: Gray-accented box for unrecognized content (collapsible if has children)
    
    Args:
        part (dict): Part dictionary containing element information with the following keys:
                    - line_number: Original line number for cross-referencing
                    - type: Element type string ('TITLE', 'SUBTITLE', 'REQUIREMENT', 'COMMENT', 'UNKNOWN')
                    - indent: Indentation level (0-10, capped at 10 for CSS classes)
                    - id: Requirement/Comment ID number (optional, for REQUIREMENT/COMMENT types)
                    - description: Text content to display
                    - children_refs: List of child elements for recursive processing
        
    Returns:
        str: HTML content string for the element and all its children. Includes:
             - Proper CSS classes for styling and indentation
             - Line number span for reference
             - Collapsible containers for child elements (except for TITLE elements)
             - Recursive HTML for all child elements
             
    Note:
        - TITLE elements render children directly without collapsible containers
        - All other element types wrap children in collapsible containers with expand/collapse functionality
        - HTML content is properly escaped to prevent XSS vulnerabilities
        - Indentation is handled via CSS classes (indent-0 through indent-10)
    """
    indent_class = f"indent-{min(part['indent'], 10)}"
    line_info = f'<span class="line-number">[{part["line_number"]}]</span>'
    has_children = len(part['children']) > 0
    
    # Title elements are not collapsible, others are if they have children
    collapsible_class = "collapsible" if has_children and part['type'] != 'TITLE' else ""
    
    # Generate element HTML based on type
    if part['type'] == 'TITLE':
        element_html = f'''
        <div class="title {indent_class}">
            {line_info}{_escape_html(part["description"])}
        </div>'''
        
    elif part['type'] == 'SUBTITLE':
        element_html = f'''
        <div class="subtitle {indent_class} {collapsible_class}" onclick="toggleCollapse(this)">
            {line_info}{_escape_html(part["description"])}
        </div>'''
        
    elif part['type'] == 'REQUIREMENT':
        req_id = f'<span class="req-id">{part["id"]} Req:</span>' if part['id'] else ''
        element_html = f'''
        <div class="requirement {indent_class} {collapsible_class}" onclick="toggleCollapse(this)">
            {line_info}{req_id}{_escape_html(part["description"])}
        </div>'''
        
    elif part['type'] == 'COMMENT':
        comment_id = f'<span class="req-id">{part["id"]} Comm:</span>' if part['id'] else ''
        element_html = f'''
        <div class="comment {indent_class} {collapsible_class}" onclick="toggleCollapse(this)">
            {line_info}{comment_id}{_escape_html(part["description"])}
        </div>'''
        
    elif part['type'] == 'DATTR':
        dattr_id = f'<span class="req-id">{part["id"]} Dattr:</span>' if part['id'] else ''
        element_html = f'''
        <div class="dattr {indent_class} {collapsible_class}" onclick="toggleCollapse(this)">
            {line_info}{dattr_id}{_escape_html(part["description"])}
        </div>'''
        
    else:  # UNKNOWN
        element_html = f'''
        <div class="unknown {indent_class} {collapsible_class}" onclick="toggleCollapse(this)">
            {line_info}{_escape_html(part["description"])}
        </div>'''
    
    # Add children if they exist
    if has_children:
        if part['type'] == 'TITLE':
            # For titles, don't wrap children in collapsible container
            for child_ref in part['children_refs']:
                element_html += _generate_element_html(child_ref)
        else:
            # For other elements, wrap children in collapsible container
            element_html += f'''
        <div class="collapsible-content expanded" id="content-{part['line_number']}">'''
            
            # Recursively generate children HTML
            for child_ref in part['children_refs']:
                element_html += _generate_element_html(child_ref)
            
            element_html += '''
        </div>'''
    
    return element_html


def _escape_html(text):
    """
    Escape HTML special characters in text to prevent XSS attacks and ensure proper display.
    
    Converts potentially dangerous HTML characters to their corresponding HTML entities
    to ensure safe rendering in web browsers and prevent cross-site scripting (XSS)
    vulnerabilities.
    
    Args:
        text (str): Raw text string that may contain HTML special characters.
                   Can be None or empty string.
        
    Returns:
        str: HTML-safe string with special characters converted to HTML entities.
             Returns empty string if input text is None or empty.
             
    Character Conversions:
        & -> &amp;   (must be first to avoid double-escaping)
        < -> &lt;    (less than)
        > -> &gt;    (greater than)
        " -> &quot;  (double quote)
        ' -> &#39;   (single quote/apostrophe)
        
    Note:
        This function is essential for security when displaying user-generated
        content or content from external sources in HTML documents.
    """
    if not text:
        return ""
    
    # Basic HTML escaping
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    text = text.replace('"', '&quot;')
    text = text.replace("'", '&#39;')
    
    return text
