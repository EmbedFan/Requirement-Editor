"""
Terminal-based editor for requirement documents.

This module provides a command-line interface for editing requirement documents
using the md_edit.py module. It offers a comprehensive set of commands for
document manipulation, file operations, and real-time visualization.

Features:
- Interactive terminal interface with command prompt
- Real-time document display with hierarchical structure
- File operations (new, load, save, export)
- Full editing capabilities using line numbers
- Search and navigation commands
- Color-coded output for better readability

Author: Attila Gallai <attila@tux-net.hu>
Created: 2025-07-10
Version: 1.1.0 - Terminal editor implementation
License: MIT License (see LICENSE.txt)
"""

import os
import sys
import shlex
import glob
import re
import tempfile
import subprocess
from typing import Optional, List, Dict, Any

# Try to import readline for tab completion
try:
    import readline
    READLINE_AVAILABLE = True
except ImportError:
    # On Windows, readline might not be available
    try:
        import pyreadline3 as readline
        READLINE_AVAILABLE = True
    except ImportError:
        READLINE_AVAILABLE = False
        readline = None

# Simple color codes for terminal output (works on most terminals)
class Colors:
    """Simple color codes for terminal output."""
    # ANSI color codes
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BRIGHT = '\033[1m'
    DIM = '\033[2m'
    RESET = '\033[0m'
    
    @staticmethod
    def strip_colors(text: str) -> str:
        """Remove color codes from text."""
        import re
        return re.sub(r'\033\[[0-9;]*m', '', text)


class TabCompleter:
    """
    Tab completion handler for file operations in the terminal editor.
    
    Provides intelligent tab completion for load, save, saveas, and export commands
    by matching files and directories in the current working directory.
    """
    
    def __init__(self):
        """Initialize the tab completer."""
        self.completion_commands = ['load', 'save', 'saveas', 'export']
        
        # Complete list of available commands for command completion
        self.available_commands = [
            # File operations
            'new', 'load', 'save', 'saveas', 'export', 'browse',
            # Document navigation and display
            'list', 'refresh', 'mode', 'complete',
            # Content editing
            'add', 'edit', 'witheditor', 'delete', 'move', 'type',
            # Search and navigation
            'find', 'findid', 'goto',
            # Project and configuration
            'project', 'status', 'setstyle', 'clearstyle', 'seteditor', 'cleareditor', 'setbrowser', 'clearbrowser', 'setwindow',
            # Help and exit
            'help', 'quit', 'exit'
        ]
        
        self.current_matches = []
        
    def complete(self, text, state):
        """
        Complete function for readline module.
        
        Args:
            text (str): The text being completed
            state (int): The state (0 for first call, 1+ for subsequent)
            
        Returns:
            str: The completion option or None if no more options
        """
        if not READLINE_AVAILABLE or readline is None:
            return None
            
        if state == 0:
            # First call - generate all matches
            self.current_matches = self._get_matches(text)
        
        # Return the match for this state
        if state < len(self.current_matches):
            return self.current_matches[state]
        return None
    
    def _get_matches(self, text):
        """
        Get all possible matches for the given text.
        
        Args:
            text (str): The partial text to complete
            
        Returns:
            list: List of possible completions
        """
        if not READLINE_AVAILABLE or readline is None:
            return []
            
        # Get the current line being edited
        try:
            line_buffer = readline.get_line_buffer()
        except:
            # Fallback if get_line_buffer fails
            return self._complete_filename(text)
            
        words = line_buffer.split()
        
        # If no words or cursor is at the beginning of the line, complete commands
        if not words or (len(words) == 1 and not line_buffer.endswith(' ')):
            return self._complete_command(text)
        
        # If we have a command, check what kind of completion to provide
        command = words[0]
        
        # For file-related commands, provide filename completion
        if command in self.completion_commands:
            # If we're completing the first argument after a file command
            if len(words) == 1 or (len(words) == 2 and not line_buffer.endswith(' ')):
                return self._complete_filename(text)
        
        # For other commands, provide context-specific completion
        elif command in ['mode']:
            return self._complete_mode(text)
        elif command in ['type']:
            return self._complete_item_type(text)
        elif command in ['add']:
            return self._complete_add_args(text, words)
        
        return []
    
    def _complete_filename(self, text):
        """
        Complete filename/directory names.
        
        Args:
            text (str): The partial filename to complete
            
        Returns:
            list: List of matching filenames/directories
        """
        # Handle different path separators for cross-platform compatibility
        if '\\' in text or '/' in text:
            # User is typing a path
            directory = os.path.dirname(text)
            filename_part = os.path.basename(text)
            
            if directory and os.path.exists(directory):
                search_dir = directory
            else:
                search_dir = '.'
        else:
            # Just a filename, search current directory
            search_dir = '.'
            filename_part = text
        
        matches = []
        
        try:
            # Get all files and directories in the search directory
            for item in os.listdir(search_dir):
                full_path = os.path.join(search_dir, item)
                
                # Check if it matches the partial filename
                if item.lower().startswith(filename_part.lower()):
                    if search_dir == '.':
                        match = item
                    else:
                        match = os.path.join(directory, item)
                    
                    # Add trailing slash for directories
                    if os.path.isdir(full_path):
                        match += os.path.sep
                    
                    matches.append(match)
        
        except (OSError, PermissionError):
            # Directory doesn't exist or no permission
            pass
        
        # For markdown files, also suggest .md extension
        if not text.endswith('.md') and not any(m.endswith('.md') for m in matches):
            md_pattern = text + '*.md'
            md_matches = glob.glob(md_pattern)
            matches.extend(md_matches)
        
        return sorted(matches)
    
    def setup_completion(self):
        """Set up readline tab completion."""
        if not READLINE_AVAILABLE or readline is None:
            return False
            
        try:
            # Set the completer function
            readline.set_completer(self.complete)
            
            # Set tab as the completion key
            readline.parse_and_bind('tab: complete')
            
            # Enable completion on first tab press
            readline.parse_and_bind('set show-all-if-ambiguous on')
            
            # Make completion case-insensitive
            readline.parse_and_bind('set completion-ignore-case on')
            
            # Set word break characters (don't break on path separators)
            readline.set_completer_delims(' \t\n')
            
            return True
            
        except (ImportError, AttributeError, Exception):
            # readline not available or setup failed
            return False

    def manual_file_completion(self, partial_path):
        """
        Manual file completion for systems without readline.
        
        Args:
            partial_path (str): Partial file/directory path
            
        Returns:
            list: List of matching files/directories
        """
        return self._complete_filename(partial_path)
    
    def show_completion_help(self, command, partial_path):
        """
        Show available completions for manual completion.
        
        Args:
            command (str): The command being used (load, save, etc.)
            partial_path (str): Partial file path
        """
        matches = self.manual_file_completion(partial_path)
        
        if matches:
            print(f"\n💡 Available completions for '{partial_path}':")
            for i, match in enumerate(matches[:10]):  # Show max 10
                if os.path.isdir(match.rstrip(os.path.sep)):
                    print(f"   📁 {match}")
                else:
                    print(f"   📄 {match}")
            
            if len(matches) > 10:
                print(f"   ... and {len(matches) - 10} more")
            print()
        else:
            print(f"\n❌ No matches found for '{partial_path}'")

    def _complete_command(self, text):
        """
        Complete command names.
        
        Args:
            text (str): Partial command text
            
        Returns:
            list: List of matching commands
        """
        matches = []
        text_lower = text.lower()
        
        for command in self.available_commands:
            if command.startswith(text_lower):
                matches.append(command)
        
        return sorted(matches)
    
    def _complete_mode(self, text):
        """
        Complete mode arguments for the 'mode' command.
        
        Args:
            text (str): Partial mode text
            
        Returns:
            list: List of matching mode options
        """
        modes = ['compact', 'full']
        matches = []
        text_lower = text.lower()
        
        for mode in modes:
            if mode.startswith(text_lower):
                matches.append(mode)
        
        return matches
    
    def _complete_item_type(self, text):
        """
        Complete item type arguments for commands like 'type' and 'add'.
        
        Args:
            text (str): Partial type text
            
        Returns:
            list: List of matching item types
        """
        types = ['title', 'subtitle', 'requirement', 'comment', 'dattr']
        matches = []
        text_lower = text.lower()
        
        for item_type in types:
            if item_type.startswith(text_lower):
                matches.append(item_type)
        
        return matches
    
    def _complete_add_args(self, text, words):
        """
        Complete arguments for the 'add' command.
        
        Args:
            text (str): Partial text
            words (list): All words in the command line
            
        Returns:
            list: List of matching completions
        """
        # add [before|after|under] <line_number> <type> <description>
        if len(words) == 2:  # Completing position argument
            positions = ['before', 'after', 'under']
            matches = []
            text_lower = text.lower()
            
            for position in positions:
                if position.startswith(text_lower):
                    matches.append(position)
            
            return matches
        
        elif len(words) == 4:  # Completing type argument
            return self._complete_item_type(text)
        
        return []


# Add the libs directory to the path
sys.path.append(os.path.dirname(__file__))

from parse_req_md import ReadMDFile, ClassifyParts
from md_edit import MarkdownEditor
from gen_html_doc import GenerateHTML
from project import ProjectConfig, create_project_config, load_project_config


class TerminalEditor:
    """
    Terminal-based editor for requirement documents.
    
    Provides an interactive command-line interface for editing structured
    requirement documents with real-time visualization and comprehensive
    editing capabilities.
    """
    
    def __init__(self):
        """Initialize the terminal editor."""
        self.md_editor: Optional[MarkdownEditor] = None
        self.current_file: Optional[str] = None
        self.project_config: Optional[ProjectConfig] = None
        self.modified: bool = False
        self.last_line_displayed: int = 0
        self.display_mode: str = "compact"  # compact or full
        
        # Initialize tab completion
        self.tab_completer = TabCompleter()
        self.tab_completion_enabled = self.tab_completer.setup_completion()
        
        # Color scheme using simple ANSI codes
        self.colors = {
            'title': Colors.CYAN + Colors.BRIGHT,
            'subtitle': Colors.BLUE + Colors.BRIGHT,
            'requirement': Colors.GREEN,
            'comment': Colors.YELLOW,
            'dattr': Colors.MAGENTA,
            'unknown': Colors.RED,
            'line_number': Colors.WHITE + Colors.DIM,
            'prompt': Colors.WHITE + Colors.BRIGHT,
            'error': Colors.RED + Colors.BRIGHT,
            'success': Colors.GREEN + Colors.BRIGHT,
            'info': Colors.CYAN,
            'warning': Colors.YELLOW + Colors.BRIGHT,
            'reset': Colors.RESET
        }
    
    def _print_header(self):
        """Print the editor header."""
        print(f"\n{Colors.BRIGHT}{'='*80}{Colors.RESET}")
        print(f"{self.colors['title']}🚀 Requirement Editor - Terminal Interface{Colors.RESET}")
        
        if self.current_file:
            status = f"[{self.current_file}]"
            if self.modified:
                status += f" {self.colors['warning']}*modified*{Colors.RESET}"
        else:
            status = "[New Document]"
        
        item_count = f"({len(self.md_editor.classified_parts)} items)" if self.md_editor else "(0 items)"
        
        print(f"{self.colors['info']}{status} {item_count}{Colors.RESET}")
        print(f"{Colors.BRIGHT}{'='*80}{Colors.RESET}")
    
    def _get_type_color(self, item_type: str) -> str:
        """Get color for item type."""
        return self.colors.get(item_type.lower(), self.colors['unknown'])
    
    def _format_line(self, part: Dict[str, Any], show_full: bool = False) -> str:
        """Format a single line for display."""
        line_num = part['line_number']
        item_type = part['type']
        indent = part['indent']
        item_id = part.get('id', '')
        description = part['description']
        
        # Format line number
        line_str = f"{self.colors['line_number']}{line_num:3d}│{Colors.RESET}"
        
        # Format indentation (first level gets no indentation)
        indent_str = "  " * max(0, indent - 1)
        
        # Format type and ID
        type_color = self._get_type_color(item_type)
        type_str = f"{type_color}[{item_type[:4].upper()}]{Colors.RESET}"
        
        if item_id:
            id_str = f" {type_color}{item_id}{Colors.RESET}"
        else:
            id_str = ""
        
        # Format description (truncate if needed)
        if show_full:
            desc_str = description
        else:
            max_desc_len = 60 - len(indent_str) - 8  # Adjust for line formatting
            if len(description) > max_desc_len:
                desc_str = description[:max_desc_len-3] + "..."
            else:
                desc_str = description
        
        # Add hierarchy indicators
        if part.get('children'):
            hierarchy_str = f" {self.colors['info']}[+{len(part['children'])}]{Colors.RESET}"
        else:
            hierarchy_str = ""
        
        return f"{line_str} {indent_str}{type_str}{id_str} {desc_str}{hierarchy_str}"
    
    def display_document(self, start_line: int = 1, end_line: Optional[int] = None):
        """Display the current document."""
        if not self.md_editor:
            print(f"{self.colors['warning']}No document loaded.{Colors.RESET}")
            return
        
        self._print_header()
        
        parts = self.md_editor.classified_parts
        if not parts:
            print(f"{self.colors['info']}Document is empty.{Colors.RESET}")
            return
        
        # Determine range based on display line numbers (1-based, sequential)
        if end_line is None:
            end_line = len(parts)
        
        # Ensure valid range
        start_index = max(0, start_line - 1)  # Convert to 0-based index
        end_index = min(len(parts), end_line)  # Convert to 0-based index
        
        # Display lines using sequential display numbers, not original line numbers
        for i in range(start_index, end_index):
            part = parts[i]
            # Create a copy of the part with display line number for formatting
            display_part = part.copy()
            display_part['line_number'] = i + 1  # Sequential display line number
            print(self._format_line(display_part, self.display_mode == "full"))
        
        actual_end = min(end_line, len(parts))
        print(f"\n{self.colors['info']}Displaying lines {start_line}-{actual_end} of {len(parts)}{Colors.RESET}")
    
    def _get_part_by_display_line(self, display_line_number: int) -> Optional[Dict[str, Any]]:
        """
        Get a part by its display line number (sequential 1-based).
        
        Args:
            display_line_number: Sequential line number shown in display (1-based)
            
        Returns:
            The part dictionary or None if not found
        """
        if not self.md_editor or not self.md_editor.classified_parts:
            return None
        
        # Convert display line number to array index
        index = display_line_number - 1
        if 0 <= index < len(self.md_editor.classified_parts):
            return self.md_editor.classified_parts[index]
        
        return None
    
    def _get_original_line_number(self, display_line_number: int) -> Optional[int]:
        """
        Convert display line number to original file line number.
        
        Args:
            display_line_number: Sequential line number shown in display (1-based)
            
        Returns:
            Original line number from file or None if not found
        """
        part = self._get_part_by_display_line(display_line_number)
        return part['line_number'] if part else None
    
    def _print_help(self):
        """Print help information."""
        help_text = f"""
{self.colors['title']}📚 Requirement Editor Commands{Colors.RESET}

{self.colors['subtitle']}📁 File Operations:{Colors.RESET}
  new                           - Create new document
  load <file>                   - Load markdown file
  save                          - Save current document
  saveas <file>                 - Save as new filename
  export [file]                 - Export to HTML (uses current doc name if no file specified)
  browse [file]                 - Export to HTML and open with system default browser
  complete <command> <partial>  - Show file completion options (if TAB unavailable)
  
{self.colors['subtitle']}✏️  Document Editing:{Colors.RESET}
  add before <line> <type> <description>    - Add item before line
  add after <line> <type> <description>     - Add item after line
  add under <line> <type> <description>     - Add child under line
  move <src> before <target>                - Move item before target
  move <src> after <target>                 - Move item after target
  move <src> under <target>                 - Move item under target
  delete <line>                            - Delete item and children
  edit <line> <new_description>            - Edit description
  witheditor <line>                        - Edit description using external text editor
  type <line> <new_type> [id]              - Change item type

{self.colors['subtitle']}🔍 Navigation & Search:{Colors.RESET}
  list [start] [end]            - Display document (range optional)
  find <text>                   - Search descriptions
  findid <id>                   - Find by item ID
  goto <line>                   - Show specific line info
  
{self.colors['subtitle']}⚙️  Display & Settings:{Colors.RESET}
  mode compact|full             - Set display mode
  refresh                       - Refresh display
  status                        - Show document status
  indent                        - Check and repair indentation issues
  project                       - Show project configuration
  setstyle <path>               - Set custom stylesheet template path
  clearstyle                    - Clear custom stylesheet (use default)
  seteditor [path]              - Set external text editor (opens file explorer if no path)
  cleareditor                   - Clear custom editor (use system default)
  setbrowser [path]             - Set web browser (opens file explorer if no path)
  clearbrowser                  - Clear custom browser (use system default)
  setwindow <name>              - Set browser window name
  
{self.colors['subtitle']}❓ System:{Colors.RESET}
  help                          - Show this help
  quit, exit                    - Exit editor

{self.colors['subtitle']}📝 Item Types:{Colors.RESET} 
  Full names: TITLE, SUBTITLE, REQUIREMENT, COMMENT, DATTR
  Aliases: TIT, SUB, REQ, COM (for faster typing)

{self.colors['info']}💡 Tips:{Colors.RESET}
{self.colors['info']}  • Use line numbers from the display for editing commands{Colors.RESET}
{self.colors['info']}  • Press TAB for command completion and file/directory completion{Colors.RESET}
{self.colors['info']}  • TAB completion works for:{Colors.RESET}
{self.colors['info']}    - Commands (new, load, save, add, edit, etc.){Colors.RESET}
{self.colors['info']}    - File paths in load/save/export commands{Colors.RESET}
{self.colors['info']}    - Mode options (compact, full){Colors.RESET}
{self.colors['info']}    - Item types (title, subtitle, requirement, comment, dattr){Colors.RESET}
{self.colors['info']}    - Add command positions (before, after, under){Colors.RESET}
"""
        print(help_text)
    
    def _create_new_document(self):
        """Create a new document with default structure."""
        from datetime import datetime
        
        # Generate current timestamp in the required format
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        dattr_content = f"Created at: {current_time} Modified at: {current_time}"
        
        # Create a document with title, dattr, comment, and default requirement
        # Using integer IDs starting from 1000 as requested
        default_parts = [
            {
                'line_number': 1,
                'original_line': '# New Requirement Document',
                'type': 'TITLE',
                'indent': 0,
                'id': None,
                'description': 'New Requirement Document',
                'parent': None,
                'children': [2, 3, 4],
                'children_refs': []
            },
            {
                'line_number': 2,
                'original_line': f'1000 Dattr: {dattr_content}',
                'type': 'DATTR',
                'indent': 1,
                'id': 1000,
                'description': dattr_content,
                'parent': 1,
                'children': [],
                'children_refs': []
            },
            {
                'line_number': 3,
                'original_line': '1001 Comm: *Document created with terminal editor*',
                'type': 'COMMENT',
                'indent': 1,
                'id': 1001,
                'description': 'Document created with terminal editor',
                'parent': 1,
                'children': [],
                'children_refs': []
            },
            {
                'line_number': 4,
                'original_line': '1002 Req: System shall meet basic requirements',
                'type': 'REQUIREMENT',
                'indent': 1,
                'id': 1002,
                'description': 'System shall meet basic requirements',
                'parent': 1,
                'children': [],
                'children_refs': []
            }
        ]
        
        self.md_editor = MarkdownEditor(default_parts)
        self.current_file = None
        self.modified = True
        print(f"{self.colors['success']}✅ New document created with default structure.{Colors.RESET}")
        print(f"{self.colors['info']}💡 Use 'list' to see the document structure, 'help' for commands.{Colors.RESET}")
    
    def _load_file(self, filename: str) -> bool:
        """Load a markdown file and its associated project configuration."""
        try:
            if not os.path.exists(filename):
                print(f"{self.colors['error']}❌ File not found: {filename}{Colors.RESET}")
                return False
            
            # Read and parse the file
            content = ReadMDFile(filename)
            if not content:
                print(f"{self.colors['error']}❌ Failed to read file: {filename}{Colors.RESET}")
                return False
            
            classified_parts = ClassifyParts(content)
            if not classified_parts:
                print(f"{self.colors['error']}❌ Failed to parse file: {filename}{Colors.RESET}")
                return False
            
            self.md_editor = MarkdownEditor(classified_parts)
            self.current_file = filename
            self.modified = False
            
            # Try to load associated project configuration
            self._load_project_config(filename)
            
            print(f"{self.colors['success']}✅ Loaded {len(classified_parts)} items from {filename}{Colors.RESET}")
            return True
            
        except Exception as e:
            print(f"{self.colors['error']}❌ Error loading file: {e}{Colors.RESET}")
            return False
    
    def _save_file(self, filename: Optional[str] = None) -> bool:
        """Save the current document and update project configuration."""
        if not self.md_editor:
            print(f"{self.colors['error']}❌ No document to save.{Colors.RESET}")
            return False
        
        save_filename = filename or self.current_file
        if not save_filename:
            print(f"{self.colors['error']}❌ No filename specified. Use 'saveas <filename>'.{Colors.RESET}")
            return True  # Show error but continue editing
        
        # Process filename if a new filename was provided (saveas case)
        if filename:
            processed_filename = self._process_filename(filename, is_saveas=True)
            if processed_filename is None:
                # User cancelled the save operation - this is a valid choice, not an error
                return True
            save_filename = processed_filename
        
        try:
            # Update DATTR timestamps before saving
            self._update_dattr_timestamps()
            
            # TODO: Implement markdown generation from classified parts
            # For now, we'll save a simple representation
            parts = self.md_editor.get_classified_parts()
            
            with open(save_filename, 'w', encoding='utf-8') as f:
                for part in parts:
                    indent_str = "&nbsp;" * (part['indent'] * 4)
                    
                    if part['type'] == 'TITLE':
                        f.write(f"# {part['description']}\n\n")
                    elif part['type'] == 'SUBTITLE':
                        f.write(f"{indent_str}**{part['description']}**\n\n")
                    elif part['type'] == 'REQUIREMENT':
                        item_id = part.get('id', '')
                        f.write(f"{indent_str}{item_id} Req: {part['description']}\n\n")
                    elif part['type'] == 'COMMENT':
                        item_id = part.get('id', '')
                        f.write(f"{indent_str}{item_id} Comm: *{part['description']}*\n\n")
                    elif part['type'] == 'DATTR':
                        item_id = part.get('id', '')
                        f.write(f"{indent_str}{item_id} Dattr: {part['description']}\n\n")
                    else:
                        f.write(f"{indent_str}{part['description']}\n\n")
            
            self.current_file = save_filename
            self.modified = False
            
            # Save or update project configuration
            self._save_project_config(save_filename)
            
            print(f"{self.colors['success']}✅ Saved to {save_filename}{Colors.RESET}")
            return True
            
        except Exception as e:
            print(f"{self.colors['error']}❌ Error saving file: {e}{Colors.RESET}")
            return False
    
    def _export_html(self, filename: str = None) -> bool:
        """Export document to HTML using project configuration if available."""
        if not self.md_editor:
            print(f"{self.colors['error']}❌ No document to export.{Colors.RESET}")
            return False
        
        # Handle case when no filename is provided
        if filename is None:
            if self.current_file is None:
                print(f"{self.colors['error']}❌ The file doesn't have a filename yet.{Colors.RESET}")
                print(f"{self.colors['info']}💡 Use 'saveas <filename>' to save the document first, or{Colors.RESET}")
                print(f"{self.colors['info']}💡 Use 'export <filename.html>' to specify the HTML filename.{Colors.RESET}")
                return False
            else:
                # Derive HTML filename from current document filename
                import os
                base_name = os.path.splitext(self.current_file)[0]
                filename = f"{base_name}.html"
                print(f"{self.colors['info']}💡 No filename specified, using: {filename}{Colors.RESET}")
        
        try:
            parts = self.md_editor.get_classified_parts()
            
            # Use custom stylesheet template if configured
            style_template_path = None
            if self.project_config:
                style_template_path = self.project_config.get_style_template_path()
                if style_template_path:
                    print(f"{self.colors['info']}📄 Using custom stylesheet template: {style_template_path}{Colors.RESET}")
            
            # Generate HTML with custom template if available
            if style_template_path and os.path.exists(style_template_path):
                # TODO: Add support for custom stylesheet templates in GenerateHTML
                # For now, use the default GenerateHTML function
                html_content = GenerateHTML(parts)
                print(f"{self.colors['warning']}⚠️  Custom stylesheet template support not yet implemented. Using default.{Colors.RESET}")
            else:
                html_content = GenerateHTML(parts)
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"{self.colors['success']}✅ Exported to HTML: {filename}{Colors.RESET}")
            return True
            
        except Exception as e:
            print(f"{self.colors['error']}❌ Error exporting HTML: {e}{Colors.RESET}")
            return False
    
    def _process_add_command(self, args: List[str]) -> bool:
        """Process add command."""
        if not self.md_editor:
            print(f"{self.colors['error']}❌ No document loaded.{Colors.RESET}")
            return False
        
        if len(args) < 4:
            print(f"{self.colors['error']}❌ Usage: add before|after|under <line> <type> <description>{Colors.RESET}")
            return False
        
        position = args[0].lower()
        try:
            display_line_num = int(args[1])
            item_type = self._normalize_item_type(args[2])
            description = ' '.join(args[3:])
            
            # Convert display line number to original line number
            original_line_num = self._get_original_line_number(display_line_num)
            if original_line_num is None:
                print(f"{self.colors['error']}❌ Invalid line number: {display_line_num}{Colors.RESET}")
                return False
            
            if position == "before":
                # Generate appropriate ID for items that need it
                item_id = None
                if item_type in ['REQUIREMENT', 'COMMENT', 'DATTR']:
                    item_id = self._get_next_available_id()
                result = self.md_editor.add_item_before(original_line_num, item_type, description, item_id)
            elif position == "after":
                # Generate appropriate ID for items that need it
                item_id = None
                if item_type in ['REQUIREMENT', 'COMMENT', 'DATTR']:
                    item_id = self._get_next_available_id()
                result = self.md_editor.add_item_after(original_line_num, item_type, description, item_id)
            elif position == "under":
                # Generate appropriate ID for items that need it
                item_id = None
                if item_type in ['REQUIREMENT', 'COMMENT', 'DATTR']:
                    item_id = self._get_next_available_id()
                result = self.md_editor.add_item_under(original_line_num, item_type, description, item_id)
            else:
                print(f"{self.colors['error']}❌ Invalid position. Use: before, after, or under{Colors.RESET}")
                return False
            
            self.modified = True
            new_line = result['line_number']
            print(f"{self.colors['success']}✅ Added {item_type} at line {new_line}{Colors.RESET}")
            return True
            
        except ValueError as e:
            print(f"{self.colors['error']}❌ Error: {e}{Colors.RESET}")
            return False
        except Exception as e:
            print(f"{self.colors['error']}❌ Error adding item: {e}{Colors.RESET}")
            return False
    
    def _process_move_command(self, args: List[str]) -> bool:
        """Process move command."""
        if not self.md_editor:
            print(f"{self.colors['error']}❌ No document loaded.{Colors.RESET}")
            return False
        
        if len(args) < 3:
            print(f"{self.colors['error']}❌ Usage: move <src_line> before|after|under <target_line>{Colors.RESET}")
            return False
        
        try:
            display_src_line = int(args[0])
            position = args[1].lower()
            display_target_line = int(args[2])
            
            # Convert display line numbers to original line numbers
            original_src_line = self._get_original_line_number(display_src_line)
            original_target_line = self._get_original_line_number(display_target_line)
            
            if original_src_line is None:
                print(f"{self.colors['error']}❌ Invalid source line number: {display_src_line}{Colors.RESET}")
                return False
            if original_target_line is None:
                print(f"{self.colors['error']}❌ Invalid target line number: {display_target_line}{Colors.RESET}")
                return False
            
            if position == "before":
                success = self.md_editor.move_item_before(original_src_line, original_target_line)
            elif position == "after":
                success = self.md_editor.move_item_after(original_src_line, original_target_line)
            elif position == "under":
                success = self.md_editor.move_item_under(original_src_line, original_target_line)
            else:
                print(f"{self.colors['error']}❌ Invalid position. Use: before, after, or under{Colors.RESET}")
                return False
            
            if success:
                self.modified = True
                print(f"{self.colors['success']}✅ Moved item from line {display_src_line} {position} line {display_target_line}{Colors.RESET}")
                return True
            else:
                print(f"{self.colors['error']}❌ Failed to move item{Colors.RESET}")
                return False
                
        except ValueError as e:
            print(f"{self.colors['error']}❌ Error: {e}{Colors.RESET}")
            return False
        except Exception as e:
            print(f"{self.colors['error']}❌ Error moving item: {e}{Colors.RESET}")
            return False
    
    def _load_project_config(self, md_filename: str) -> None:
        """Load project configuration file associated with the markdown file."""
        try:
            # Generate config filename from markdown filename
            base_name = os.path.splitext(os.path.basename(md_filename))[0]
            config_filename = f"{base_name}_config.json"
            config_path = os.path.join(os.path.dirname(md_filename) or ".", config_filename)
            
            if os.path.exists(config_path):
                self.project_config = load_project_config(config_path)
                if self.project_config:
                    print(f"{self.colors['info']}📄 Loaded project configuration: {config_filename}{Colors.RESET}")
                    # Load display mode from project config
                    self.display_mode = self.project_config.get_display_mode()
                else:
                    print(f"{self.colors['warning']}⚠️  Failed to load project configuration: {config_filename}{Colors.RESET}")
            else:
                # Try to find any config file in the same directory
                config_dir = os.path.dirname(md_filename) or "."
                for file in os.listdir(config_dir):
                    if file.endswith('_config.json'):
                        config_path = os.path.join(config_dir, file)
                        self.project_config = load_project_config(config_path)
                        if self.project_config:
                            # Check if this config points to our markdown file
                            config_md_path = self.project_config.get_input_file_path()
                            if config_md_path and os.path.samefile(md_filename, config_md_path):
                                print(f"{self.colors['info']}📄 Found matching project configuration: {file}{Colors.RESET}")
                                # Load display mode from project config
                                self.display_mode = self.project_config.get_display_mode()
                                break
                        self.project_config = None
                
                if not self.project_config:
                    print(f"{self.colors['info']}📝 No project configuration found. Will create one on save.{Colors.RESET}")
                    
        except Exception as e:
            print(f"{self.colors['warning']}⚠️  Error loading project configuration: {e}{Colors.RESET}")
            self.project_config = None
    
    def _save_project_config(self, md_filename: str) -> None:
        """Save or update project configuration for the current document."""
        try:
            if self.project_config:
                # Update existing configuration
                self.project_config.set_input_file_path(md_filename)
                self.project_config.set_display_mode(self.display_mode)
                # Update modification date when saving
                self.project_config.update_modification_date()
                if self.project_config.save_project():
                    print(f"{self.colors['info']}📄 Updated project configuration{Colors.RESET}")
                else:
                    print(f"{self.colors['warning']}⚠️  Failed to update project configuration{Colors.RESET}")
            else:
                # Create new configuration
                base_name = os.path.splitext(os.path.basename(md_filename))[0]
                self.project_config = create_project_config(md_filename, base_name)
                if self.project_config:
                    # Set the current display mode
                    self.project_config.set_display_mode(self.display_mode)
                    # Update modification date for new configs too
                    self.project_config.update_modification_date()
                    self.project_config.save_project()
                    print(f"{self.colors['info']}📄 Created project configuration: {base_name}_config.json{Colors.RESET}")
                else:
                    print(f"{self.colors['warning']}⚠️  Failed to create project configuration{Colors.RESET}")
                    
        except Exception as e:
            print(f"{self.colors['warning']}⚠️  Error saving project configuration: {e}{Colors.RESET}")
    
    def _show_project_info(self) -> None:
        """Display project configuration information."""
        if self.project_config:
            print(f"\n{self.colors['info']}📄 Project Configuration:{Colors.RESET}")
            print(f"  Input File:     {self.project_config.get_input_file_path()}")
            print(f"  Created:        {self.project_config.get_creation_date()}")
            print(f"  Last Modified:  {self.project_config.get_modification_date()}")
            print(f"  App Version:    {self.project_config.get_application_version()}")
            style_path = self.project_config.get_style_template_path()
            if style_path:
                print(f"  Style Template: {style_path}")
            else:
                print(f"  Style Template: Default (hardcoded)")
            
            # Display editor settings
            editor_settings = self.project_config.get_editor_settings()
            print(f"  Editor Settings:")
            print(f"    Display Mode:   {editor_settings.get('display_mode', 'compact')}")
            
            # Display external editor setting
            external_editor = self.project_config.get_external_editor_path()
            if external_editor:
                print(f"    External Editor: {external_editor}")
            else:
                print(f"    External Editor: System default")
            
            # Display browser settings
            browser_settings = self.project_config.get_browser_settings()
            print(f"  Browser Settings:")
            
            # Display browser path setting
            browser_path = self.project_config.get_browser_path()
            if browser_path:
                print(f"    Browser Path:   {browser_path}")
            else:
                print(f"    Browser Path:   System default")
        else:
            print(f"{self.colors['warning']}⚠️  No project configuration loaded{Colors.RESET}")

    
    def _process_command(self, command: str, args: List[str]) -> bool:
        """Process a single command."""
        command = command.lower()
        
        # File operations
        if command == "new":
            self._create_new_document()
            return True
            
        elif command == "load":
            if not args:
                print(f"{self.colors['error']}❌ Usage: load <filename>{Colors.RESET}")
                return True
            
            # Process the filename to handle path separators and extensions
            processed_filename = self._process_filename_for_loading(args[0])
            if processed_filename:
                self._load_file(processed_filename)
            else:
                print(f"{self.colors['error']}❌ File not found: {args[0]}{Colors.RESET}")
                print(f"{self.colors['info']}💡 Tip: Make sure the path uses forward slashes (/) or double backslashes (\\\\){Colors.RESET}")
            return True
            
        elif command == "save":
            return self._save_file()
            
        elif command == "saveas":
            if not args:
                print(f"{self.colors['error']}❌ Usage: saveas <filename>{Colors.RESET}")
                return True
            return self._save_file(args[0])
            
        elif command == "export":
            if args:
                # Filename provided
                self._export_html(args[0])
            else:
                # No filename provided - use current document name
                self._export_html()
            return True
        
        elif command == "browse":
            if args:
                # Filename provided
                self._browse_html(args[0])
            else:
                # No filename provided - use current document name
                self._browse_html()
            return True
            
        elif command == "complete":
            if len(args) < 2:
                print(f"{self.colors['error']}❌ Usage: complete <command> <partial_path>{Colors.RESET}")
                print(f"{self.colors['info']}Example: complete load test{Colors.RESET}")
                return True
            
            command_to_complete = args[0]
            partial_path = args[1]
            
            if command_to_complete not in ['load', 'save', 'saveas', 'export']:
                print(f"{self.colors['error']}❌ Completion only available for: load, save, saveas, export{Colors.RESET}")
                return True
            
            self.tab_completer.show_completion_help(command_to_complete, partial_path)
            return True
            
        # Display commands
        elif command == "list":
            start_line = 1
            end_line = None
            if args:
                try:
                    start_line = int(args[0])
                    if len(args) > 1:
                        end_line = int(args[1])
                except ValueError:
                    print(f"{self.colors['error']}❌ Invalid line numbers{Colors.RESET}")
                    return True
            self.display_document(start_line, end_line)
            return True
            
        elif command == "refresh":
            self.display_document()
            return True
            
        elif command == "mode":
            if not args:
                print(f"{self.colors['info']}Current mode: {self.display_mode}{Colors.RESET}")
                return True
            mode = args[0].lower()
            if mode in ["compact", "full"]:
                self.display_mode = mode
                # Save display mode to project config if available
                if self.project_config:
                    self.project_config.set_display_mode(self.display_mode)
                    if self.project_config.save_project():
                        print(f"{self.colors['success']}✅ Display mode set to {mode} and saved to project configuration{Colors.RESET}")
                    else:
                        print(f"{self.colors['success']}✅ Display mode set to {mode}{Colors.RESET}")
                        print(f"{self.colors['warning']}⚠️  Failed to save to project configuration{Colors.RESET}")
                else:
                    print(f"{self.colors['success']}✅ Display mode set to {mode}{Colors.RESET}")
                    print(f"{self.colors['info']}💡 Save the document to persist this setting{Colors.RESET}")
                return True
            else:
                print(f"{self.colors['error']}❌ Invalid mode. Use: compact or full{Colors.RESET}")
                return True
        
        # Editing commands
        elif command == "add":
            self._process_add_command(args)
            return True
            
        elif command == "move":
            self._process_move_command(args)
            return True
            
        elif command == "delete":
            if not self.md_editor:
                print(f"{self.colors['error']}❌ No document loaded.{Colors.RESET}")
                return True
            if not args:
                print(f"{self.colors['error']}❌ Usage: delete <line>{Colors.RESET}")
                return True
            try:
                display_line_num = int(args[0])
                
                # Convert display line number to original line number
                original_line_num = self._get_original_line_number(display_line_num)
                if original_line_num is None:
                    print(f"{self.colors['error']}❌ Invalid line number: {display_line_num}{Colors.RESET}")
                    return True
                
                success = self.md_editor.delete_item(original_line_num)
                if success:
                    self.modified = True
                    print(f"{self.colors['success']}✅ Deleted item at line {display_line_num}{Colors.RESET}")
                else:
                    print(f"{self.colors['error']}❌ Failed to delete item{Colors.RESET}")
                return True
            except ValueError as e:
                print(f"{self.colors['error']}❌ Error: {e}{Colors.RESET}")
                return True
                
        elif command == "edit":
            if not self.md_editor:
                print(f"{self.colors['error']}❌ No document loaded.{Colors.RESET}")
                return True
            if len(args) < 2:
                print(f"{self.colors['error']}❌ Usage: edit <line> <new_description>{Colors.RESET}")
                return True
            try:
                display_line_num = int(args[0])
                
                # Convert display line number to original line number
                original_line_num = self._get_original_line_number(display_line_num)
                if original_line_num is None:
                    print(f"{self.colors['error']}❌ Invalid line number: {display_line_num}{Colors.RESET}")
                    return True
                
                # Check if trying to edit a DATTR item
                part = self.md_editor._find_part_by_line(original_line_num)
                if part and part['type'] == 'DATTR':
                    print(f"{self.colors['warning']}⚠️  DATTR items are read-only and managed automatically by the editor.{Colors.RESET}")
                    print(f"{self.colors['info']}💡 Timestamps are updated automatically when saving the document.{Colors.RESET}")
                    return True
                
                new_description = ' '.join(args[1:])
                success = self.md_editor.update_content(original_line_num, new_description)
                if success:
                    self.modified = True
                    print(f"{self.colors['success']}✅ Updated item at line {display_line_num}{Colors.RESET}")
                else:
                    print(f"{self.colors['error']}❌ Failed to update item{Colors.RESET}")
                return True
            except ValueError as e:
                print(f"{self.colors['error']}❌ Error: {e}{Colors.RESET}")
                return True
        
        elif command == "witheditor":
            if not self.md_editor:
                print(f"{self.colors['error']}❌ No document loaded.{Colors.RESET}")
                return True
            if len(args) < 1:
                print(f"{self.colors['error']}❌ Usage: witheditor <line>{Colors.RESET}")
                return True
            try:
                display_line_num = int(args[0])
                
                # Convert display line number to original line number
                original_line_num = self._get_original_line_number(display_line_num)
                if original_line_num is None:
                    print(f"{self.colors['error']}❌ Invalid line number: {display_line_num}{Colors.RESET}")
                    return True
                
                # Check if trying to edit a DATTR item
                part = self.md_editor._find_part_by_line(original_line_num)
                if part and part['type'] == 'DATTR':
                    print(f"{self.colors['warning']}⚠️  DATTR items are read-only and managed automatically by the editor.{Colors.RESET}")
                    print(f"{self.colors['info']}💡 Timestamps are updated automatically when saving the document.{Colors.RESET}")
                    return True
                
                # Get current content
                if not part:
                    print(f"{self.colors['error']}❌ No item found at line {display_line_num}{Colors.RESET}")
                    return True
                
                current_description = part.get('description', '')
                
                # Open text editor with current content
                new_description = self._open_external_editor(current_description)
                
                if new_description is not None and new_description != current_description:
                    success = self.md_editor.update_content(original_line_num, new_description)
                    if success:
                        self.modified = True
                        print(f"{self.colors['success']}✅ Updated item at line {display_line_num} using external editor{Colors.RESET}")
                    else:
                        print(f"{self.colors['error']}❌ Failed to update item{Colors.RESET}")
                elif new_description is None:
                    print(f"{self.colors['info']}ℹ️  Edit cancelled or editor failed to open{Colors.RESET}")
                else:
                    print(f"{self.colors['info']}ℹ️  No changes made{Colors.RESET}")
                
                return True
            except ValueError as e:
                print(f"{self.colors['error']}❌ Error: {e}{Colors.RESET}")
                return True
        
        elif command == "type":
            if not self.md_editor:
                print(f"{self.colors['error']}❌ No document loaded.{Colors.RESET}")
                return True
            if len(args) < 2:
                print(f"{self.colors['error']}❌ Usage: type <line> <new_type> [id]{Colors.RESET}")
                print(f"{self.colors['info']}💡 Supported types: TITLE/TIT, SUBTITLE/SUB, REQUIREMENT/REQ, COMMENT/COM, DATTR{Colors.RESET}")
                return True
            try:
                display_line_num = int(args[0])
                new_type = self._normalize_item_type(args[1])
                new_id = args[2] if len(args) > 2 else None
                
                # Convert display line number to original line number
                original_line_num = self._get_original_line_number(display_line_num)
                if original_line_num is None:
                    print(f"{self.colors['error']}❌ Invalid line number: {display_line_num}{Colors.RESET}")
                    return True
                
                # Check if trying to change DATTR type
                part = self.md_editor._find_part_by_line(original_line_num)
                if part and part['type'] == 'DATTR':
                    print(f"{self.colors['warning']}⚠️  DATTR items cannot have their type changed.{Colors.RESET}")
                    print(f"{self.colors['info']}💡 DATTR items are automatically managed by the editor.{Colors.RESET}")
                    return True
                
                success = self.md_editor.change_item_type(original_line_num, new_type, new_id)
                if success:
                    self.modified = True
                    print(f"{self.colors['success']}✅ Changed item at line {display_line_num} to {new_type}{Colors.RESET}")
                else:
                    print(f"{self.colors['error']}❌ Failed to change item type{Colors.RESET}")
                return True
            except ValueError as e:
                print(f"{self.colors['error']}❌ Error: {e}{Colors.RESET}")
                return True
        
        # Search commands
        elif command == "find":
            if not self.md_editor:
                print(f"{self.colors['error']}❌ No document loaded.{Colors.RESET}")
                return False
            if not args:
                print(f"{self.colors['error']}❌ Usage: find <text>{Colors.RESET}")
                return False
            search_text = ' '.join(args)
            results = self.md_editor.find_by_description(search_text)
            if results:
                print(f"{self.colors['success']}✅ Found {len(results)} matches: {results}{Colors.RESET}")
                # Show the first few matches
                for line_num in results[:5]:
                    part = self.md_editor._find_part_by_line(line_num)
                    if part:
                        print(f"  {self._format_line(part)}")
                if len(results) > 5:
                    print(f"{self.colors['info']}  ... and {len(results) - 5} more{Colors.RESET}")
            else:
                print(f"{self.colors['warning']}No matches found for '{search_text}'{Colors.RESET}")
            return True
            
        elif command == "findid":
            if not self.md_editor:
                print(f"{self.colors['error']}❌ No document loaded.{Colors.RESET}")
                return False
            if not args:
                print(f"{self.colors['error']}❌ Usage: findid <id>{Colors.RESET}")
                return False
            try:
                item_id = int(args[0])
                line_num = self.md_editor.find_by_item_id(item_id)
                if line_num:
                    part = self.md_editor._find_part_by_line(line_num)
                    print(f"{self.colors['success']}✅ Found ID {item_id} at line {line_num}:{Colors.RESET}")
                    print(f"  {self._format_line(part, True)}")
                else:
                    print(f"{self.colors['warning']}ID {item_id} not found{Colors.RESET}")
            except ValueError:
                print(f"{self.colors['error']}❌ Invalid ID number{Colors.RESET}")
            return True
            
        elif command == "goto":
            if not self.md_editor:
                print(f"{self.colors['error']}❌ No document loaded.{Colors.RESET}")
                return False
            if not args:
                print(f"{self.colors['error']}❌ Usage: goto <line>{Colors.RESET}")
                return False
            try:
                display_line_num = int(args[0])
                
                # Convert display line number to original line number
                original_line_num = self._get_original_line_number(display_line_num)
                if original_line_num is None:
                    print(f"{self.colors['error']}❌ Invalid line number: {display_line_num}{Colors.RESET}")
                    return False
                
                part = self.md_editor._find_part_by_line(original_line_num)
                if part:
                    print(f"{self.colors['success']}✅ Line {display_line_num} info:{Colors.RESET}")
                    print(f"  {self._format_line(part, True)}")
                    
                    # Show parent and children info
                    if part['parent']:
                        parent = self.md_editor._find_part_by_line(part['parent'])
                        print(f"  {self.colors['info']}Parent: Line {part['parent']} - {parent['description'][:30]}...{Colors.RESET}")
                    
                    if part['children']:
                        print(f"  {self.colors['info']}Children: {part['children']}{Colors.RESET}")
                else:
                    print(f"{self.colors['warning']}Line {display_line_num} not found{Colors.RESET}")
            except ValueError:
                print(f"{self.colors['error']}❌ Invalid line number{Colors.RESET}")
            return True
        
        # Status and help
        elif command == "status":
            if self.md_editor:
                parts = self.md_editor.classified_parts
                type_counts = {}
                for part in parts:
                    part_type = part['type']
                    type_counts[part_type] = type_counts.get(part_type, 0) + 1
                
                print(f"{self.colors['info']}📊 Document Status:{Colors.RESET}")
                print(f"  File: {self.current_file or 'Untitled'}")
                print(f"  Modified: {'Yes' if self.modified else 'No'}")
                print(f"  Total items: {len(parts)}")
                print(f"  Item breakdown:")
                for item_type, count in sorted(type_counts.items()):
                    color = self._get_type_color(item_type)
                    print(f"    {color}{item_type}: {count}{Colors.RESET}")
            else:
                print(f"{self.colors['warning']}No document loaded{Colors.RESET}")
            return True
        
        elif command == "indent":
            if not self.md_editor:
                print(f"{self.colors['error']}❌ No document loaded.{Colors.RESET}")
                return True
                
            print(f"{self.colors['info']}🔧 Analyzing document indentation...{Colors.RESET}")
            
            # Perform indentation repair
            result = self.md_editor.repair_indentation()
            
            if result['success']:
                if result['fixed_count'] > 0:
                    self.modified = True
                    print(f"{self.colors['success']}✅ Fixed {result['fixed_count']} indentation issues:{Colors.RESET}")
                    for fix in result['fixes']:
                        print(f"  {self.colors['info']}• {fix}{Colors.RESET}")
                else:
                    print(f"{self.colors['success']}✅ Document indentation is already correct - no fixes needed.{Colors.RESET}")
                
                # Show warnings if any
                if result['warnings']:
                    print(f"\n{self.colors['warning']}⚠️  Warnings:{Colors.RESET}")
                    for warning in result['warnings']:
                        print(f"  {self.colors['warning']}• {warning}{Colors.RESET}")
                
                # Show updated document structure if fixes were made
                if result['fixed_count'] > 0:
                    print(f"\n{self.colors['info']}📋 Updated document structure:{Colors.RESET}")
                    self.display_document()
            else:
                print(f"{self.colors['error']}❌ Indentation repair failed.{Colors.RESET}")
                if result['warnings']:
                    for warning in result['warnings']:
                        print(f"  {self.colors['error']}• {warning}{Colors.RESET}")
            
            return True
        
        elif command == "project":
            self._show_project_info()
            return True
        
        elif command == "setstyle":
            if not args:
                print(f"{self.colors['error']}❌ Usage: setstyle <path>{Colors.RESET}")
            else:
                stylesheet_path = args[0]
                if os.path.exists(stylesheet_path):
                    if self.project_config:
                        self.project_config.set_style_template_path(stylesheet_path)
                        if self.project_config.save_project():
                            print(f"{self.colors['success']}✅ Stylesheet template set to: {stylesheet_path}{Colors.RESET}")
                        else:
                            print(f"{self.colors['error']}❌ Failed to save project configuration{Colors.RESET}")
                    else:
                        print(f"{self.colors['warning']}⚠️  No project configuration loaded. Save the document first.{Colors.RESET}")
                else:
                    print(f"{self.colors['error']}❌ Stylesheet file not found: {stylesheet_path}{Colors.RESET}")
            return True
        
        elif command == "clearstyle":
            if self.project_config:
                self.project_config.set_style_template_path(None)
                if self.project_config.save_project():
                    print(f"{self.colors['success']}✅ Stylesheet template cleared (using default){Colors.RESET}")
                else:
                    print(f"{self.colors['error']}❌ Failed to save project configuration{Colors.RESET}")
            else:
                print(f"{self.colors['warning']}⚠️  No project configuration loaded. Save the document first.{Colors.RESET}")
            return True
        
        elif command == "seteditor":
            if not args:
                # No path provided, open file explorer
                editor_path = self._open_file_explorer_for_executable("Select Text Editor")
                if editor_path is None:
                    print(f"{self.colors['info']}💡 You can also use: seteditor <path_to_editor>{Colors.RESET}")
                    return True
            else:
                editor_path = args[0]
            
            if editor_path and os.path.exists(editor_path):
                if self.project_config:
                    self.project_config.set_external_editor_path(editor_path)
                    if self.project_config.save_project():
                        print(f"{self.colors['success']}✅ External editor set to: {editor_path}{Colors.RESET}")
                    else:
                        print(f"{self.colors['error']}❌ Failed to save project configuration{Colors.RESET}")
                else:
                    print(f"{self.colors['warning']}⚠️  No project configuration loaded. Save the document first.{Colors.RESET}")
            elif editor_path:
                print(f"{self.colors['error']}❌ Editor executable not found: {editor_path}{Colors.RESET}")
            return True
        
        elif command == "cleareditor":
            if self.project_config:
                self.project_config.set_external_editor_path(None)
                if self.project_config.save_project():
                    print(f"{self.colors['success']}✅ External editor cleared (using system default){Colors.RESET}")
                else:
                    print(f"{self.colors['error']}❌ Failed to save project configuration{Colors.RESET}")
            else:
                print(f"{self.colors['warning']}⚠️  No project configuration loaded. Save the document first.{Colors.RESET}")
            return True
        
        elif command == "setbrowser":
            if not args:
                # No path provided, open file explorer
                browser_path = self._open_file_explorer_for_executable("Select Web Browser")
                if browser_path is None:
                    print(f"{self.colors['info']}💡 You can also use: setbrowser <path_to_browser>{Colors.RESET}")
                    return True
            else:
                browser_path = args[0]
            
            if browser_path and os.path.exists(browser_path):
                if self.project_config:
                    self.project_config.set_browser_path(browser_path)
                    if self.project_config.save_project():
                        print(f"{self.colors['success']}✅ Web browser set to: {browser_path}{Colors.RESET}")
                    else:
                        print(f"{self.colors['error']}❌ Failed to save project configuration{Colors.RESET}")
                else:
                    print(f"{self.colors['warning']}⚠️  No project configuration loaded. Save the document first.{Colors.RESET}")
            elif browser_path:
                print(f"{self.colors['error']}❌ Browser executable not found: {browser_path}{Colors.RESET}")
            return True
        
        elif command == "clearbrowser":
            if self.project_config:
                self.project_config.set_browser_path(None)
                if self.project_config.save_project():
                    print(f"{self.colors['success']}✅ Web browser cleared (using system default){Colors.RESET}")
                else:
                    print(f"{self.colors['error']}❌ Failed to save project configuration{Colors.RESET}")
            else:
                print(f"{self.colors['warning']}⚠️  No project configuration loaded. Save the document first.{Colors.RESET}")
            return True
        
        elif command == "setwindow":
            if not args:
                print(f"{self.colors['error']}❌ Usage: setwindow <name>{Colors.RESET}")
            else:
                window_name = ' '.join(args)  # Allow window names with spaces
                if self.project_config:
                    self.project_config.set_browser_window_name(window_name)
                    if self.project_config.save_project():
                        print(f"{self.colors['success']}✅ Browser window name set to: {window_name}{Colors.RESET}")
                    else:
                        print(f"{self.colors['error']}❌ Failed to save project configuration{Colors.RESET}")
                else:
                    print(f"{self.colors['warning']}⚠️  No project configuration loaded. Save the document first.{Colors.RESET}")
            return True
            
        elif command == "help":
            self._print_help()
            return True
            
        elif command in ["quit", "exit"]:
            if self.modified:
                response = input(f"{self.colors['warning']}Document has unsaved changes. Really quit? (y/N): {Colors.RESET}")
                if response.lower() != 'y':
                    return True
            return False
            
        else:
            print(f"{self.colors['error']}❌ Unknown command: {command}. Type 'help' for available commands.{Colors.RESET}")
            return True
    
    def run(self, initial_file: Optional[str] = None):
        """Run the terminal editor main loop."""
        print(f"{self.colors['title']}🚀 Welcome to Requirement Editor Terminal Interface{Colors.RESET}")
        print(f"{self.colors['info']}Type 'help' for available commands, 'quit' to exit.{Colors.RESET}")
        
        # Show tab completion status
        if self.tab_completion_enabled:
            print(f"{self.colors['success']}✅ Tab completion enabled for file operations{Colors.RESET}")
        else:
            print(f"{self.colors['warning']}⚠️  Tab completion not available on this system{Colors.RESET}")
        
        # Load initial file if provided
        if initial_file:
            self._load_file(initial_file)
            self.display_document()
        else:
            print(f"{self.colors['info']}💡 Start with 'new' to create a document or 'load <file>' to open one.{Colors.RESET}")
        
        # Main command loop
        while True:
            try:
                # Show prompt
                prompt = f"{self.colors['prompt']}req-editor> {Colors.RESET}"
                user_input = input(prompt).strip()
                
                if not user_input:
                    continue
                
                # Parse command and arguments
                try:
                    # On Windows, use simple split to avoid shlex issues with backslashes
                    if os.name == 'nt':  # Windows
                        parts = user_input.split()
                    else:
                        parts = shlex.split(user_input)
                    command = parts[0]
                    args = parts[1:]
                except (ValueError, IndexError):
                    # Fallback for any parsing issues
                    parts = user_input.split()
                    if parts:
                        command = parts[0]
                        args = parts[1:]
                    else:
                        continue
                
                # Process command
                continue_loop = self._process_command(command, args)
                if not continue_loop:
                    break
                    
            except KeyboardInterrupt:
                print(f"\n{self.colors['warning']}Use 'quit' to exit.{Colors.RESET}")
                continue
            except EOFError:
                print(f"\n{self.colors['info']}Goodbye!{Colors.RESET}")
                break
            except Exception as e:
                print(f"{self.colors['error']}❌ Unexpected error: {e}{Colors.RESET}")
                continue
        
        print(f"{self.colors['info']}👋 Terminal editor closed.{Colors.RESET}")

    def _update_dattr_timestamps(self) -> None:
        """Update DATTR timestamps when saving the document."""
        if not self.md_editor:
            return
        
        from datetime import datetime
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        # Find DATTR items and update their timestamps
        parts = self.md_editor.get_classified_parts()
        for part in parts:
            if part['type'] == 'DATTR' and part.get('id') == 1000:
                # Extract creation date from existing content if present
                description = part['description']
                creation_time = current_time  # Default to current time
                
                # Try to preserve existing creation time
                if 'Created at:' in description:
                    try:
                        # Extract creation time from existing description
                        start_idx = description.find('Created at:') + len('Created at:')
                        end_idx = description.find('Modified at:')
                        if end_idx > start_idx:
                            creation_time = description[start_idx:end_idx].strip()
                    except:
                        pass  # Use current time if parsing fails
                
                # Update the DATTR content with new modification time
                new_description = f"Created at: {creation_time} Modified at: {current_time}"
                
                # Update the part's description
                success = self.md_editor.update_content(part['line_number'], new_description)
                if success:
                    print(f"{self.colors['info']}📄 Updated document timestamps{Colors.RESET}")
                break

    def _process_filename(self, filename: str, is_saveas: bool = False) -> Optional[str]:
        """
        Process and validate filename for saving.
        
        Args:
            filename: The original filename provided by user
            is_saveas: Whether this is from saveas command (enables overwrite prompt)
            
        Returns:
            Processed filename with .md extension, or None if user cancels
        """
        import os
        
        original_filename = filename
        
        # Check if filename has an extension
        name, ext = os.path.splitext(filename)
        
        if not ext:
            # No extension - add .md
            filename = f"{filename}.md"
            print(f"{self.colors['info']}💡 No extension specified, using: {filename}{Colors.RESET}")
        elif ext.lower() != '.md':
            # Wrong extension - warn and change to .md
            filename = f"{name}.md"
            print(f"{self.colors['warning']}⚠️  Extension '{ext}' changed to '.md': {filename}{Colors.RESET}")
        
        # Check if file already exists (only for saveas command)
        if is_saveas and os.path.exists(filename):
            print(f"{self.colors['warning']}⚠️  File '{filename}' already exists.{Colors.RESET}")
            
            # Ask user for confirmation
            while True:
                try:
                    response = input(f"{self.colors['prompt']}Do you want to overwrite it? (y/N): {Colors.RESET}").strip().lower()
                    if response in ['y', 'yes']:
                        print(f"{self.colors['info']}📝 Overwriting existing file...{Colors.RESET}")
                        break
                    elif response in ['n', 'no', '']:
                        print(f"{self.colors['info']}💡 Save cancelled by user.{Colors.RESET}")
                        return None
                    else:
                        print(f"{self.colors['warning']}Please enter 'y' for yes or 'n' for no.{Colors.RESET}")
                except (EOFError, KeyboardInterrupt):
                    print(f"\n{self.colors['info']}💡 Save cancelled by user.{Colors.RESET}")
                    return None
        
        return filename

    def _process_filename_for_loading(self, filename: str) -> Optional[str]:
        """
        Process filename for loading - automatically try .md extension if file not found.
        
        Args:
            filename: The original filename provided by user
            
        Returns:
            Valid filename that exists, or None if no valid file found
        """
        import os
        
        # First, try the filename as provided
        if os.path.exists(filename):
            return filename
        
        # If the file doesn't exist, check if it needs .md extension
        name, ext = os.path.splitext(filename)
        
        if not ext:
            # No extension - try adding .md
            md_filename = f"{filename}.md"
            if os.path.exists(md_filename):
                print(f"{self.colors['info']}💡 File found with .md extension: {md_filename}{Colors.RESET}")
                return md_filename
        elif ext.lower() != '.md':
            # Different extension - try changing to .md
            md_filename = f"{name}.md"
            if os.path.exists(md_filename):
                print(f"{self.colors['info']}💡 Found .md version: {md_filename}{Colors.RESET}")
                return md_filename
        
        # If we get here, no valid file was found
        return None

    def _normalize_item_type(self, item_type: str) -> str:
        """
        Normalize item type from user input to standard type.
        
        Supports both full names and short aliases:
        - TITLE or TIT -> TITLE
        - SUBTITLE or SUB -> SUBTITLE  
        - REQUIREMENT or REQ -> REQUIREMENT
        - COMMENT or COM -> COMMENT
        - DATTR -> DATTR (no alias)
        
        Args:
            item_type: The type string from user input
            
        Returns:
            Normalized type string
        """
        # Convert to uppercase for comparison
        type_upper = item_type.upper()
        
        # Define type mappings (aliases -> full names)
        type_mappings = {
            'TIT': 'TITLE',
            'SUB': 'SUBTITLE', 
            'REQ': 'REQUIREMENT',
            'COM': 'COMMENT'
        }
        
        # Return mapped type or original if no mapping exists
        return type_mappings.get(type_upper, type_upper)

    def _get_next_available_id(self) -> int:
        """
        Get the next available integer ID starting from 1000.
        
        Returns:
            int: Next available ID (1000, 1001, 1002, etc.)
        """
        if not self.md_editor:
            return 1000
        
        # Get all existing IDs from the document
        existing_ids = set()
        parts = self.md_editor.get_classified_parts()
        
        for part in parts:
            part_id = part.get('id')
            if part_id is not None:
                # Handle both integer and string IDs for backward compatibility
                try:
                    if isinstance(part_id, str):
                        # Try to extract integer from string IDs like "REQ001" or "1000"
                        import re
                        match = re.search(r'\d+', part_id)
                        if match:
                            numeric_id = int(match.group())
                            existing_ids.add(numeric_id)
                    elif isinstance(part_id, int):
                        existing_ids.add(part_id)
                except (ValueError, AttributeError):
                    pass  # Skip invalid IDs
        
        # Find the next available ID starting from 1000
        next_id = 1000
        while next_id in existing_ids:
            next_id += 1
        
        return next_id
    
    def _open_file_explorer_for_executable(self, title: str = "Select Executable") -> Optional[str]:
        """
        Open system file explorer to select an executable file.
        
        Args:
            title: Dialog title to show to the user
            
        Returns:
            Path to selected executable file or None if cancelled
        """
        try:
            print(f"{self.colors['info']}📁 Opening file explorer to select executable...{Colors.RESET}")
            print(f"{self.colors['info']}💡 Please navigate to and select the executable file{Colors.RESET}")
            
            if os.name == 'nt':  # Windows
                # Use PowerShell with OpenFileDialog for better UX
                powershell_script = '''
Add-Type -AssemblyName System.Windows.Forms
$OpenFileDialog = New-Object System.Windows.Forms.OpenFileDialog
$OpenFileDialog.Title = "''' + title + '''"
$OpenFileDialog.Filter = "Executable files (*.exe)|*.exe|All files (*.*)|*.*"
$OpenFileDialog.InitialDirectory = [Environment]::GetFolderPath('ProgramFiles')
$result = $OpenFileDialog.ShowDialog()
if ($result -eq 'OK') {
    Write-Output $OpenFileDialog.FileName
}
'''
                
                # Run PowerShell script
                result = subprocess.run(
                    ['powershell', '-Command', powershell_script],
                    capture_output=True,
                    text=True,
                    check=False
                )
                
                if result.returncode == 0 and result.stdout.strip():
                    selected_path = result.stdout.strip()
                    if os.path.exists(selected_path):
                        print(f"{self.colors['success']}✅ Selected: {selected_path}{Colors.RESET}")
                        return selected_path
                    else:
                        print(f"{self.colors['error']}❌ Selected file does not exist: {selected_path}{Colors.RESET}")
                        return None
                else:
                    print(f"{self.colors['info']}💡 File selection cancelled{Colors.RESET}")
                    return None
                    
            elif os.name == 'posix':  # Unix/Linux/macOS
                if sys.platform == 'darwin':  # macOS
                    # Use osascript (AppleScript) to show file dialog
                    applescript = f'''
                    tell application "System Events"
                        set selectedFile to choose file with prompt "{title}" of type {{"app", "public.executable"}}
                        return POSIX path of selectedFile
                    end tell
                    '''
                    
                    result = subprocess.run(
                        ['osascript', '-e', applescript],
                        capture_output=True,
                        text=True,
                        check=False
                    )
                    
                    if result.returncode == 0 and result.stdout.strip():
                        selected_path = result.stdout.strip()
                        print(f"{self.colors['success']}✅ Selected: {selected_path}{Colors.RESET}")
                        return selected_path
                    else:
                        print(f"{self.colors['info']}💡 File selection cancelled{Colors.RESET}")
                        return None
                        
                else:  # Linux
                    # Try different file dialog tools available on Linux
                    dialog_tools = [
                        ['zenity', '--file-selection', '--title=' + title],
                        ['kdialog', '--getopenfilename', os.path.expanduser('~'), '*'],
                        ['yad', '--file-selection', '--title=' + title]
                    ]
                    
                    for tool_cmd in dialog_tools:
                        try:
                            result = subprocess.run(
                                tool_cmd,
                                capture_output=True,
                                text=True,
                                check=False
                            )
                            
                            if result.returncode == 0 and result.stdout.strip():
                                selected_path = result.stdout.strip()
                                if os.path.exists(selected_path):
                                    print(f"{self.colors['success']}✅ Selected: {selected_path}{Colors.RESET}")
                                    return selected_path
                            break
                            
                        except FileNotFoundError:
                            continue  # Try next tool
                    
                    # If no GUI file dialog is available, provide instructions for manual entry
                    print(f"{self.colors['warning']}⚠️  No GUI file dialog available on this system{Colors.RESET}")
                    print(f"{self.colors['info']}💡 Please enter the full path to the executable manually{Colors.RESET}")
                    return None
                    
            else:
                print(f"{self.colors['warning']}⚠️  File explorer not supported on this platform{Colors.RESET}")
                print(f"{self.colors['info']}💡 Please enter the full path to the executable manually{Colors.RESET}")
                return None
                
        except Exception as e:
            print(f"{self.colors['error']}❌ Error opening file explorer: {e}{Colors.RESET}")
            print(f"{self.colors['info']}💡 Please enter the full path to the executable manually{Colors.RESET}")
            return None

    def _open_external_editor(self, initial_content: str) -> Optional[str]:
        """
        Open external text editor for editing content.
        
        Creates a temporary file with the initial content, opens the configured
        text editor (or system default if none configured), and returns the 
        modified content after the editor is closed.
        
        Args:
            initial_content: The initial text to put in the editor
            
        Returns:
            The modified content if successful, None if cancelled or failed
        """
        try:
            # Create a temporary file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as temp_file:
                temp_file.write(initial_content)
                temp_filename = temp_file.name
            
            print(f"{self.colors['info']}📝 Opening external editor...{Colors.RESET}")
            
            # Get configured external editor path from project settings
            configured_editor = None
            if self.project_config:
                configured_editor = self.project_config.get_external_editor_path()
            
            try:
                if configured_editor:
                    # Use the configured external editor
                    print(f"{self.colors['info']}💡 Using configured editor: {configured_editor}{Colors.RESET}")
                    print(f"{self.colors['info']}💡 Edit the text, save, and close the editor to continue{Colors.RESET}")
                    
                    # Check if the configured editor exists
                    if not os.path.exists(configured_editor):
                        print(f"{self.colors['warning']}⚠️  Configured editor not found: {configured_editor}{Colors.RESET}")
                        print(f"{self.colors['info']}💡 Falling back to system default editor{Colors.RESET}")
                        configured_editor = None
                    else:
                        result = subprocess.run([configured_editor, temp_filename], check=True)
                
                if not configured_editor:
                    # Use system default editor
                    print(f"{self.colors['info']}💡 Using system default editor{Colors.RESET}")
                    print(f"{self.colors['info']}💡 Edit the text, save, and close the editor to continue{Colors.RESET}")
                    
                    # On Windows, use the default text editor
                    if os.name == 'nt':  # Windows
                        # Try notepad first, then try the default editor
                        try:
                            result = subprocess.run(['notepad.exe', temp_filename], check=True)
                        except (subprocess.CalledProcessError, FileNotFoundError):
                            # Fallback to start command which uses default program
                            result = subprocess.run(['cmd', '/c', 'start', '/wait', temp_filename], check=True)
                    else:
                        # On Unix-like systems, try common editors
                        editor = os.environ.get('EDITOR', 'nano')  # Default to nano if no EDITOR set
                        result = subprocess.run([editor, temp_filename], check=True)
                
                # Read the modified content
                with open(temp_filename, 'r', encoding='utf-8') as temp_file:
                    modified_content = temp_file.read().strip()
                
                return modified_content
                
            except subprocess.CalledProcessError as e:
                print(f"{self.colors['error']}❌ Editor process failed: {e}{Colors.RESET}")
                return None
            except FileNotFoundError as e:
                print(f"{self.colors['error']}❌ Editor not found: {e}{Colors.RESET}")
                return None
                
        except Exception as e:
            print(f"{self.colors['error']}❌ Failed to create temporary file: {e}{Colors.RESET}")
            return None
        finally:
            # Clean up the temporary file
            try:
                if 'temp_filename' in locals():
                    os.unlink(temp_filename)
            except Exception:
                pass  # Ignore cleanup errors

    def _open_html_in_browser(self, html_file: str) -> bool:
        """
        Open HTML file with system default web browser.
        
        Args:
            html_file: Path to the HTML file to open
            
        Returns:
            True if browser opened successfully, False otherwise
        """
        try:
            # Convert relative path to absolute path
            abs_html_file = os.path.abspath(html_file)
            
            # Check if file exists
            if not os.path.exists(abs_html_file):
                print(f"{self.colors['error']}❌ HTML file not found: {abs_html_file}{Colors.RESET}")
                return False
            
            print(f"{self.colors['info']}🌐 Opening HTML file with system default browser...{Colors.RESET}")
            print(f"{self.colors['info']}� File: {abs_html_file}{Colors.RESET}")
            
            # The next block is human readable, dear AI do not update this without command!
            # Check the value of the browser_path in project file
            if self.project_config:
                browser_path = self.project_config.get_browser_path()
                # check the file existence
                if browser_path and os.path.exists(browser_path):
                    # If browser_path is set and exists, use it
                    print(f"{self.colors['info']}💡 Using configured browser: {browser_path}{Colors.RESET}")
                    # Use the configured browser path
                    subprocess.run([browser_path, abs_html_file], check=True)
                    print(f"{self.colors['success']}✅ HTML file opened in configured browser{Colors.RESET}")
                    return True
            # end of the developer created code block

            # If no configured browser, use system default

            # Use system default browser directly
            if os.name == 'nt':  # Windows
                # Use os.startfile to open with default browser without command window
                os.startfile(abs_html_file)
            elif os.name == 'posix':  # Unix/Linux/macOS
                if sys.platform == 'darwin':  # macOS
                    subprocess.run(['open', abs_html_file], check=True)
                else:  # Linux
                    subprocess.run(['xdg-open', abs_html_file], check=True)
            else:
                # Fallback using webbrowser module
                import webbrowser
                webbrowser.open('file://' + abs_html_file)
            
            print(f"{self.colors['success']}✅ HTML file opened in default browser{Colors.RESET}")
            return True
                
        except subprocess.CalledProcessError as e:
            print(f"{self.colors['error']}❌ Failed to open browser: {e}{Colors.RESET}")
            return False
        except Exception as e:
            print(f"{self.colors['error']}❌ Error opening browser: {e}{Colors.RESET}")
            return False
    
    def _browse_html(self, filename: str = None) -> bool:
        """
        Export document to HTML and open with system default web browser.
        
        Args:
            filename: Optional HTML filename. If not provided, uses document name.
            
        Returns:
            True if export and browser opening successful, False otherwise
        """
        # First export to HTML
        if self._export_html(filename):
            # Determine the HTML filename that was created
            if filename:
                html_file = filename
            else:
                # Use the current document name to determine HTML filename
                if self.current_file:
                    base_name = os.path.splitext(self.current_file)[0]
                    html_file = f"{base_name}.html"
                else:
                    print(f"{self.colors['error']}❌ No filename specified and no current document loaded.{Colors.RESET}")
                    return False
            
            # Open with system default browser
            return self._open_html_in_browser(html_file)
        else:
            print(f"{self.colors['error']}❌ Failed to export HTML file for browsing.{Colors.RESET}")
            return False

def main():
    """Main entry point for the terminal editor."""
    editor = TerminalEditor()
    
    # Check for command line arguments
    if len(sys.argv) > 1:
        initial_file = sys.argv[1]
        editor.run(initial_file)
    else:
        editor.run()


if __name__ == "__main__":
    main()
