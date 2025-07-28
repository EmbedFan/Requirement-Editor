"""
Markdown Requirements Document to Interactive HTML Converter

This module serves as the main entry point for the Requirement Editor application,
orchestrating the complete workflow from markdown requirements parsing to interactive
HTML document generation with modern web features.

Application Overview:
The Requirement Editor is a specialized tool for converting markdown-formatted technical
requirement documents into professional, interactive HTML documents. It automatically
parses structured requirements, builds hierarchical relationships, and generates
web-based documentation with advanced features like expand/collapse sections,
line number references, and print-to-PDF capabilities.

Key Features:
- Complete markdown-to-HTML conversion pipeline with intelligent parsing
- Automatic classification of requirement document elements (titles, subtitles, requirements, comments)
- Interactive web interface with expand/collapse functionality for structured navigation
- Professional styling with color-coded element types for visual distinction
- Print-optimized output with preserved styling for PDF generation
- Comprehensive command-line interface for batch processing and automation
- Detailed console output for workflow transparency and debugging
- Configurable input sources with robust error handling

Workflow Architecture:
1. **Command Line Processing**: Parses arguments and validates input parameters
2. **File Input**: Reads markdown files with UTF-8 encoding and comprehensive error handling
3. **Content Parsing**: Classifies document elements and builds hierarchical structure
4. **Console Reporting**: Displays detailed processing results for verification
5. **HTML Generation**: Creates interactive web documents with embedded CSS and JavaScript
6. **File Output**: Saves results with proper encoding and error handling

Document Element Classification:
- TITLE: Document and section headers (# Title format)
- SUBTITLE: Section subsections with indentation (&nbsp;&nbsp;**Subtitle** format)
- REQUIREMENT: Numbered requirements (&nbsp;&nbsp;1001 Req: Description format)
- COMMENT: Numbered comments (&nbsp;&nbsp;*1001 Comm: Description* format)
- DATTR: Data attributes with metadata (&nbsp;&nbsp;1001 Dattr: Key-value data format)
- UNKNOWN: Other markdown content (preserved with appropriate styling)

Interactive HTML Features:
- Color-coded element types: green=requirements, yellow=comments, blue=subtitles, cyan=dattr
- Click-to-expand/collapse functionality for all elements except main titles
- Line number references for traceability between markdown source and HTML output
- Print-optimized CSS with background color preservation for professional PDF output
- Control interface: Expand All, Collapse All, Toggle Line Numbers, Print to PDF buttons
- Responsive design that works across desktop and mobile devices

Command Line Interface:
    python main.py                           # Process default input file
    python main.py -h                        # Display comprehensive help information
    python main.py -md2html <filepath>       # Convert specific markdown file to HTML

Configuration:
    cfg_inputfile: Default input file path (configurable at module level)
    Output files: Automatically generated with same name as input but .html extension
    
Error Handling Strategy:
- Graceful degradation with informative error messages at each processing step
- File I/O errors handled with detailed diagnostics and suggested solutions
- Command line validation with helpful usage information on invalid input
- Exit codes: 0=success, 1=error (compatible with shell scripting and automation)

Module Dependencies:
    - libs.parse_req_md: Core markdown parsing and element classification
    - libs.gen_html_doc: HTML generation with CSS styling and JavaScript interactivity
    - sys, os: Standard library modules for system integration

Integration Notes:
This module serves as the primary orchestrator in a modular architecture where
specialized functionality is delegated to appropriate library modules. The design
emphasizes separation of concerns, comprehensive error handling, and user feedback
throughout the conversion process.

Example Console Output:
```
Successfully read 1247 characters from requirements.md

Classified 15 parts:
----------------------------------------------------------------------------------------------------
Line  1: Type: TITLE        | Indent: 0 | ID:  N/A | Parent: None | Children: [2, 5]
         Description: System Requirements Specification...

Line  2: Type: SUBTITLE     | Indent: 1 | ID:  N/A | Parent: 1 | Children: [3, 4]  
         Description: User Interface Requirements...

Line  3: Type: REQUIREMENT  | Indent: 2 | ID: 1001 | Parent: 2 | Children: None
         Description: The system shall provide a graphical user interface...

HTML file saved successfully: requirements.html
```

Author: Attila Gallai <attila@tux-net.hu>
Created: 2025-07-09
Version: 1.1.0
License: MIT License (see LICENSE.txt)
"""

import sys
import os
from libs.parse_req_md import ReadMDFile, ClassifyParts
from libs.gen_html_doc import GenerateHTML


cfg_inputfile = "C:\\Munka\\Sandbox\\PromptEnginering\\Requirement Editor\\python\\test\\data\\test_input.md"


def SaveHTMLFile(html_content, filename):
    """
    Save HTML content to a file with proper encoding and error handling.
    
    Writes the provided HTML content to a file using UTF-8 encoding to ensure
    proper handling of international characters and special symbols that may
    be present in requirement documents.
    
    Args:
        html_content (str): Complete HTML document content to save. Should be
                           a valid HTML string, typically generated by GenerateHTML().
        filename (str): Output filename with path. Can be absolute or relative path.
                       Recommended to use .html extension for proper file association.
        
    Returns:
        bool: True if file was saved successfully, False if an error occurred.
              Error details are printed to console but function doesn't raise exceptions.
              
    Error Handling:
        - Catches and handles IOError exceptions (file permissions, disk space, etc.)
        - Prints descriptive error messages to console
        - Returns False on any error to allow calling code to handle gracefully
        
    Note:
        - Uses UTF-8 encoding which supports international characters
        - Creates parent directories if they don't exist (depends on OS)
        - Overwrites existing files without warning
        - File is automatically closed even if write operation fails
    """
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(html_content)
        return True
    except IOError as e:
        print(f"Error saving HTML file '{filename}': {e}")
        return False


def process_filename_for_loading(filename):
    """
    Process filename for loading - automatically try .md extension if file not found.
    
    Args:
        filename (str): The original filename provided by user
        
    Returns:
        str: Valid filename that exists, or None if no valid file found
    """
    # First, try the filename as provided
    if os.path.exists(filename):
        return filename
    
    # If the file doesn't exist, check if it needs .md extension
    name, ext = os.path.splitext(filename)
    
    if not ext:
        # No extension - try adding .md
        md_filename = f"{filename}.md"
        if os.path.exists(md_filename):
            print(f"Info: File found with .md extension: {md_filename}")
            return md_filename
    elif ext.lower() != '.md':
        # Different extension - try changing to .md
        md_filename = f"{name}.md"
        if os.path.exists(md_filename):
            print(f"Info: Found .md version: {md_filename}")
            return md_filename
    
    # If we get here, no valid file was found
    return None


def show_help():
    """
    Display help information and usage examples for the command line interface.
    
    Shows available command line options, usage examples, and feature descriptions
    to help users understand how to use the Requirement Editor application.
    """
    print("=" * 80)
    print("REQUIREMENT EDITOR - Markdown to HTML Converter")
    print("=" * 80)
    print()
    print("DESCRIPTION:")
    print("  Converts markdown-formatted requirement documents into interactive,")
    print("  styled HTML documents with hierarchical organization and modern web features.")
    print("  Automatically tries adding .md extension if file is not found.")
    print()
    print("USAGE:")
    print("  python main.py                           # Use default input file")
    print("  python main.py -h                        # Show this help information")
    print("  python main.py -md2html <filepath>       # Convert specific markdown file")
    print("  python main.py -ed [filepath]            # Start terminal editor (optionally load file)")
    print()
    print("COMMAND LINE OPTIONS:")
    print("  -h                     Show help information and usage examples")
    print("  -md2html <filepath>     Convert specified markdown file to HTML")
    print("                         (automatically tries .md extension if file not found)")
    print("  -ed [filepath]         Start terminal-based interactive editor")
    print("                         (automatically tries .md extension if file not found)")
    print()
    print("EXAMPLES:")
    print("  python main.py -md2html requirements     # Finds requirements.md automatically")
    print("  python main.py -md2html requirements.md  # Direct file specification")
    print("  python main.py -md2html \"C:\\\\Documents\\\\specs\"  # Finds specs.md automatically")
    print("  python main.py -ed                       # Start editor with new document")
    print("  python main.py -ed requirements          # Finds and loads requirements.md")
    print("  python main.py -md2html ../project/requirements")
    print("  python main.py -md2html test_input")
    print("  python main.py -md2html example")
    print()
    print("OUTPUT:")
    print("  - HTML file is created with same name as input file but .html extension")
    print("  - Interactive features: expand/collapse, line numbers, print-to-PDF")
    print("  - Professional styling with color-coded element types")
    print()
    print("SUPPORTED ELEMENTS:")
    print("  - TITLE: Document and section titles")
    print("  - SUBTITLE: Section headers with indentation")
    print("  - REQUIREMENT: Requirements with ID numbers (e.g., 1001 Req: description)")
    print("  - COMMENT: Comments with ID numbers (e.g., 1001 Comm: description)")
    print("  - DATTR: Data attributes with metadata (e.g., 1001 Dattr: key-value data)")
    print("  - UNKNOWN: Other markdown content")
    print()
    print("AUTHOR: Attila Gallai <attila@tux-net.hu>")
    print("LICENSE: MIT License")
    print("=" * 80)


def process_command_line():
    """
    Process command line arguments and return the input file path to use.
    
    Parses command line arguments and handles the following options:
    - No arguments: Use default input file
    - -h: Show help and exit
    - -md2html <filepath>: Use specified file path
    
    Returns:
        str: Path to the markdown file to process, or None if help was shown
        
    Error Handling:
        - Shows help and exits if invalid arguments provided
        - Validates file path exists for -md2html option
        - Provides clear error messages for missing arguments
    """
    args = sys.argv[1:]  # Remove script name
    
    # No arguments - use default file
    if len(args) == 0:
        return cfg_inputfile
    
    # Help option
    if len(args) == 1 and args[0] == "-h":
        show_help()
        sys.exit(0)  # Success exit for help
    
    # Terminal editor option
    if len(args) >= 1 and args[0] == "-ed":
        # Import the terminal editor
        try:
            from libs.terminal_editor import TerminalEditor
            editor = TerminalEditor()
            
            # Check if a file was specified to load
            if len(args) == 2:
                initial_file = args[1]
                
                # Process filename - try to find with .md extension if needed
                processed_file = editor._process_filename_for_loading(initial_file)
                
                if processed_file:
                    # File found (possibly with .md extension added)
                    editor.run(processed_file)
                else:
                    # No valid file found
                    print(f"Warning: Input file not found: {initial_file}")
                    if not initial_file.endswith('.md'):
                        print(f"Also tried: {initial_file}.md")
                    print("Starting with empty document...")
                    editor.run()
            else:
                editor.run()
            
            sys.exit(0)  # Terminal editor handles its own exit
            
        except ImportError as e:
            print(f"Error: Could not import terminal editor: {e}")
            print("Please ensure all required modules are available.")
            sys.exit(1)
        except Exception as e:
            print(f"Error starting terminal editor: {e}")
            sys.exit(1)
    
    # Convert specific file option
    if len(args) >= 1 and args[0] == "-md2html":
        if len(args) != 2:
            print("Error: -md2html requires a file path argument.")
            print()
            print("Usage: python main.py -md2html <filepath>")
            print("Use 'python main.py -h' for help information.")
            sys.exit(1)  # Error exit for missing file argument
        
        input_file = args[1]
        
        # Try to find the file (with automatic .md extension if needed)
        processed_file = process_filename_for_loading(input_file)
        
        if processed_file:
            return processed_file
        else:
            # No valid file found
            print(f"Error: Input file not found: {input_file}")
            if not input_file.endswith('.md'):
                print(f"Also tried: {input_file}.md")
            print()
            print("Use 'python main.py -h' for help information.")
            sys.exit(1)  # Error exit for missing file
    
    # Invalid arguments
    print("Error: Invalid command line arguments.")
    print()
    print("Valid usage:")
    print("  python main.py                           # Use default input file")
    print("  python main.py -h                       # Show help information")
    print("  python main.py -md2html <filepath>       # Convert specific file")
    print("  python main.py -ed [filepath]            # Start terminal editor")
    print()
    print("Use 'python main.py -h' for detailed help information.")
    sys.exit(1)  # Error exit for invalid arguments


def main():
    """
    Main entry point for the Markdown to HTML requirement document converter.
    
    Orchestrates the complete workflow of reading a markdown requirements document,
    parsing and classifying its contents, generating an interactive HTML document,
    and saving the result to a file. This function serves as the workflow coordinator,
    delegating specialized tasks to appropriate modules.
    
    Workflow:
    1. **File Reading**: Uses ReadMDFile() from libs.parse_req_md to read input markdown
    2. **Content Parsing**: Uses ClassifyParts() from libs.parse_req_md to parse and classify elements
    3. **Console Display**: Shows detailed classification results for verification and debugging
    4. **HTML Generation**: Uses GenerateHTML() from libs.gen_html_doc to create interactive HTML
    5. **File Output**: Uses local SaveHTMLFile() to save the result with proper encoding
    
    Console Output Features:
    - File reading success/failure messages with character counts
    - Detailed classification table showing:
      * Line numbers and element types (TITLE, SUBTITLE, REQUIREMENT, COMMENT, UNKNOWN)
      * Indentation levels and ID numbers for requirements/comments
      * Parent-child relationships in the document hierarchy
      * Description text (truncated to 120 characters for readability)
    - HTML generation and file saving status messages
    
    Error Handling Strategy:
    - Gracefully handles file reading errors from the parsing module
    - Continues processing even if some steps fail (except critical file reading)
    - Provides informative error messages to user at each step
    - Exits gracefully with clear message if input file cannot be read
    
    Configuration:
    - Input file path specified in global variable cfg_inputfile
    - Output file automatically determined by replacing .md extension with .html
    - HTML document title set to "Requirement Document for Requirement Editor"
    
    Module Dependencies:
    - libs.parse_req_md.ReadMDFile(): File input with UTF-8 encoding and error handling
    - libs.parse_req_md.ClassifyParts(): Content parsing, classification, and hierarchy building
    - libs.gen_html_doc.GenerateHTML(): Interactive HTML generation with CSS and JavaScript
    - Local SaveHTMLFile(): File output with UTF-8 encoding and error handling
    
    Integration Notes:
    - Serves as the primary orchestrator in a modular architecture
    - Minimal business logic - delegates specialized tasks to appropriate modules
    - Provides user feedback and transparency throughout the conversion process
    - No return value - results are saved to file and status printed to console
    
    Example Console Output:
    ```
    Successfully read 1247 characters from C:\\...\\test_input.md
    
    Classified 15 parts:
    ----------------------------------------------------------------------------------------------------
    Line  1: Type: TITLE        | Indent: 0 | ID:  N/A | Parent: None | Children: [2, 5]
             Description: System Requirements...
    
    Line  2: Type: SUBTITLE     | Indent: 1 | ID:  N/A | Parent: 1 | Children: [3, 4]  
             Description: User Interface...
    
    HTML file saved successfully: C:\\...\\test_input.html
    ```
    """

    # Command line argument processing
    input_file = process_command_line()
    if input_file is None:
        return  # Help was shown, exit the program
    
    cfg_inputfile = input_file

    # Read the markdown file
    md_content = ReadMDFile(cfg_inputfile)
    
    if md_content:
        print(f"Successfully read {len(md_content)} characters from {cfg_inputfile}")
        
        # Classify the parts
        classified_parts = ClassifyParts(md_content)
        
        print(f"\nClassified {len(classified_parts)} parts:")
        print("-" * 100)
        
        for part in classified_parts:
            parent_info = f"Parent: {part['parent']}" if part['parent'] else "Parent: None"
            children_info = f"Children: {part['children']}" if part['children'] else "Children: None"
            
            print(f"Line {part['line_number']:2d}: "
                  f"Type: {part['type']:12s} | "
                  f"Indent: {part['indent']} | "
                  f"ID: {str(part['id']) if part['id'] else 'N/A':>4s} | "
                  f"{parent_info} | "
                  f"{children_info}")
            print(f"         Description: {part['description'][:120]}...")
            print()
        
        # Generate HTML
        html_content = GenerateHTML(classified_parts, "Requirement Document for Requirement Editor")
        
        # Save HTML file
        html_filename = cfg_inputfile.replace('.md', '.html')
        if SaveHTMLFile(html_content, html_filename):
            print(f"\nHTML file saved successfully: {html_filename}")
            sys.exit(0)  # Success exit
        else:
            print("\nFailed to save HTML file")
            sys.exit(1)  # Error exit
        
    else:
        print("Failed to read the markdown file. Exiting...")
        sys.exit(1)  # Error exit

    pass


if __name__ == "__main__":
    main()