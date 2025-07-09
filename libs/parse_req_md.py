"""
Markdown Requirements Document Parser Module

This module provides functionality to parse and classify markdown-formatted requirement 
documents into structured hierarchical elements. It handles identification of different 
document element types and builds parent-child relationships based on indentation.

Key Features:
- Parses markdown content to identify titles, subtitles, requirements, and comments
- Builds hierarchical structure based on HTML &nbsp; indentation
- Maintains traceability through line number references
- Processes comment descriptions by removing asterisk formatting
- Uses stack-based algorithm for efficient hierarchy building

Document Structure Support:
- Titles: Lines starting with '#' (highest hierarchy level)
- Subtitles: Lines with &nbsp; indentation and **bold** formatting
- Requirements: Lines with &nbsp; + number + "Req:" pattern
- Comments: Lines with &nbsp; + number + "Comm:" pattern (asterisks auto-removed)
- Unknown: Any other content (preserved with appropriate indentation)

Indentation System:
- Every 2 &nbsp; HTML entities = 1 indentation level
- Parent-child relationships built using stack-based algorithm
- Supports up to 10 indentation levels with CSS styling

Author: Attila Gallai <attila@tux-net.hu>
Created: 2025
License: MIT License (see LICENSE.txt)
"""

import re


def ReadMDFile(filename):
    """
    Read a markdown file and return its contents as a string with proper error handling.
    
    Attempts to read the specified markdown file using UTF-8 encoding, which is
    standard for markdown files and supports international characters.
    
    Args:
        filename (str): Path to the markdown file to read. Can be absolute or relative path.
        
    Returns:
        str: Complete contents of the file as a string if successful.
        None: If file cannot be read due to missing file or I/O errors.
        
    Raises:
        Prints error messages to console but does not raise exceptions:
        - FileNotFoundError: When the specified file doesn't exist
        - IOError: When file exists but cannot be read (permissions, corruption, etc.)
        
    Note:
        Uses UTF-8 encoding which supports international characters commonly
        found in technical documentation and requirements.
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None
    except IOError as e:
        print(f"Error reading file '{filename}': {e}")
        return None


def ClassifyParts(mdContent):
    """
    Parse and classify markdown content into structured requirement document elements.
    
    Analyzes each line of markdown content to identify and classify different types of
    requirement document elements, then builds hierarchical parent-child relationships
    based on indentation levels using HTML &nbsp; entities.
    
    Classification Rules:
    - Lines starting with '#' -> TITLE (indent = 0, highest level)
    - Lines with &nbsp; + number + "Req:" -> REQUIREMENT (indent based on &nbsp; count)
    - Lines with &nbsp; + number + "Comm:" -> COMMENT (indent based on &nbsp; count)
    - Lines with &nbsp; + "**text**" -> SUBTITLE (indent based on &nbsp; count)
    - All other content -> UNKNOWN (indent based on &nbsp; count)
    
    Indentation Logic:
    - Every 2 &nbsp; HTML entities = 1 indentation level
    - Indentation determines parent-child relationships in hierarchy
    - Elements with higher indent become children of nearest lower-indent element
    
    Comment Processing:
    - Automatically removes surrounding '*' characters from comment descriptions
    - Preserves formatting and spacing within comment text
    
    Hierarchy Building:
    - Uses stack-based algorithm to establish parent-child relationships
    - Maintains references both by line number and direct object references
    - Enables efficient traversal and HTML generation
    
    Args:
        mdContent (str): Complete markdown content as a string to analyze.
                        Can contain multiple lines with various formatting.
        
    Returns:
        list: List of dictionaries, each representing a classified document element.
              Each dictionary contains:
              - line_number (int): Original line number in source file (1-based)
              - original_line (str): Complete unmodified line text
              - type (str): Element type ('TITLE', 'REQUIREMENT', 'COMMENT', 'SUBTITLE', 'UNKNOWN')
              - indent (int): Indentation level (0, 1, 2, etc.) based on &nbsp; count
              - id (int|None): Requirement/Comment ID number if applicable
              - description (str): Processed description text (comments have '*' removed)
              - parent (int|None): Line number of parent element (None for root elements)
              - children (list): List of line numbers of direct child elements
              - parent_ref (dict|None): Direct reference to parent element object
              - children_refs (list): List of direct references to child element objects
              
        Returns empty list if mdContent is None or empty.
        
    Example:
        Input markdown:
        ```
        # Main Title
        &nbsp;&nbsp;**Subsection**
        &nbsp;&nbsp;&nbsp;&nbsp;1 Req: This is a requirement
        &nbsp;&nbsp;&nbsp;&nbsp;2 Comm: *This is a comment*
        ```
        
        Output structure:
        - TITLE (indent=0, no parent)
          - SUBTITLE (indent=1, parent=title)
            - REQUIREMENT (indent=2, parent=subtitle)
            - COMMENT (indent=2, parent=subtitle, description="This is a comment")
            
    Note:
        - Empty lines are automatically skipped during processing
        - Hierarchy is built using a stack-based approach for efficiency
        - All text content is preserved exactly as written (except comment asterisks)
        - Line numbers maintain traceability to original source
    """
    if not mdContent:
        return []
    
    lines = mdContent.split('\n')
    classified_parts = []
    
    for line_number, line in enumerate(lines, 1):
        # Skip empty lines
        if not line.strip():
            continue
            
        # Initialize the classification dictionary
        part = {
            'line_number': line_number,
            'original_line': line,
            'type': None,
            'indent': 0,
            'id': None,
            'description': None,
            'parent': None,
            'children': [],
            'parent_ref': None,
            'children_refs': []
        }
        
        # Check if line starts with # (Title)
        if line.strip().startswith('#'):
            part['type'] = 'TITLE'
            part['indent'] = 0
            part['description'] = line.strip()[1:].strip()  # Remove # and trim
            
        else:
            # Count &nbsp; entities to determine indentation
            nbsp_count = 0
            temp_line = line
            
            while temp_line.startswith('&nbsp;'):
                nbsp_count += 1
                temp_line = temp_line[6:]  # Remove &nbsp; (6 characters)
            
            # Calculate indent level (every 2 &nbsp; = 1 indent level)
            calculated_indent = nbsp_count // 2
            
            # Remove leading &nbsp; entities for easier parsing
            clean_line = temp_line.strip()
            
            # Check for requirement/comment pattern: number followed by "Req:" or "Comm:"
            req_pattern = r'^(\d+)\s+(Req|Comm):\s*(.+)$'
            match = re.match(req_pattern, clean_line)
            
            if match:
                req_id = match.group(1)
                req_type = match.group(2)
                description = match.group(3)
                
                part['id'] = int(req_id)
                part['type'] = 'REQUIREMENT' if req_type == 'Req' else 'COMMENT'
                
                # Process description based on type
                if req_type == 'Comm':
                    # Remove first and last '*' characters for comments
                    description = description.strip()
                    if description.startswith('*') and description.endswith('*') and len(description) > 1:
                        description = description[1:-1]
                    part['description'] = description
                else:
                    part['description'] = description.strip()
                
                # Requirements and comments use calculated indent based on &nbsp; count
                part['indent'] = calculated_indent
                
            else:
                # Check for subtitle pattern (bold text **text**)
                subtitle_pattern = r'^\*\*(.+)\*\*$'
                subtitle_match = re.match(subtitle_pattern, clean_line)
                
                if subtitle_match:
                    part['type'] = 'SUBTITLE'
                    part['description'] = subtitle_match.group(1).strip()
                    # Subtitles register the calculated indent from &nbsp; count
                    part['indent'] = calculated_indent
                else:
                    # If it doesn't match any pattern, classify as unknown
                    part['type'] = 'UNKNOWN'
                    part['description'] = clean_line
                    part['indent'] = calculated_indent
        
        classified_parts.append(part)
    
    # Build parent-child relationships
    _build_hierarchy(classified_parts)
    
    return classified_parts


def _build_hierarchy(parts):
    """
    Build parent-child relationships between document elements based on indentation levels.
    
    Uses a stack-based algorithm to efficiently establish hierarchical relationships
    between document elements. Elements with higher indentation levels become children
    of the nearest element with a lower indentation level.
    
    Algorithm:
    1. Maintain a stack of potential parent elements at different indent levels
    2. For each element, remove from stack any elements at same or deeper indent level
    3. If stack has elements, the top element becomes the parent
    4. Add current element to stack as potential parent for subsequent elements
    
    This approach ensures:
    - Correct parent-child relationships based on document structure
    - Efficient O(n) time complexity for building the entire hierarchy
    - Proper handling of skipped indentation levels
    - Maintenance of both line number references and direct object references
    
    Args:
        parts (list): List of classified part dictionaries to process. Each dictionary
                     will be modified in-place to add parent-child relationship data.
                     Must contain 'indent' key for each element.
        
    Returns:
        None: Function modifies the parts list in-place by adding:
              - parent: Line number of parent element (None if root)
              - children: List of line numbers of child elements
              - parent_ref: Direct reference to parent element object
              - children_refs: List of direct references to child element objects
              
    Note:
        - Handles empty or None input gracefully
        - Maintains both numeric references (line numbers) and object references
        - Stack ensures correct parent assignment even with irregular indentation
        - All modifications are made in-place for memory efficiency
    """
    if not parts:
        return
    
    # Stack to keep track of potential parents at each indent level
    parent_stack = []
    
    for current_part in parts:
        current_indent = current_part['indent']
        
        # Remove parents from stack that are at same or deeper level
        while parent_stack and parent_stack[-1]['indent'] >= current_indent:
            parent_stack.pop()
        
        # If we have a potential parent, establish the relationship
        if parent_stack:
            parent = parent_stack[-1]
            current_part['parent'] = parent['line_number']
            current_part['parent_ref'] = parent
            
            parent['children'].append(current_part['line_number'])
            parent['children_refs'].append(current_part)
        
        # Add current part to stack as potential parent for next items
        parent_stack.append(current_part)
