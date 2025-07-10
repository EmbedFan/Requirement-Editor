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
Version: 1.0.0 - Terminal editor implementation
License: MIT License (see LICENSE.txt)
"""

import os
import sys
import shlex
from typing import Optional, List, Dict, Any

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
        
        # Format indentation
        indent_str = "  " * indent
        
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
        
        # Determine range
        if end_line is None:
            end_line = len(parts)
        
        # Display lines
        for part in parts:
            line_num = part['line_number']
            if start_line <= line_num <= end_line:
                print(self._format_line(part, self.display_mode == "full"))
        
        print(f"\n{self.colors['info']}Displaying lines {start_line}-{min(end_line, len(parts))} of {len(parts)}{Colors.RESET}")
    
    def _print_help(self):
        """Print help information."""
        help_text = f"""
{self.colors['title']}📚 Requirement Editor Commands{Colors.RESET}

{self.colors['subtitle']}📁 File Operations:{Colors.RESET}
  new                           - Create new document
  load <file>                   - Load markdown file
  save                          - Save current document
  saveas <file>                 - Save as new filename
  export <file>                 - Export to HTML
  
{self.colors['subtitle']}✏️  Document Editing:{Colors.RESET}
  add before <line> <type> <description>    - Add item before line
  add after <line> <type> <description>     - Add item after line
  add under <line> <type> <description>     - Add child under line
  move <src> before <target>                - Move item before target
  move <src> after <target>                 - Move item after target
  move <src> under <target>                 - Move item under target
  delete <line>                            - Delete item and children
  edit <line> <new_description>            - Edit description
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
  project                       - Show project configuration
  setstyle <path>               - Set custom stylesheet template path
  clearstyle                    - Clear custom stylesheet (use default)
  
{self.colors['subtitle']}❓ System:{Colors.RESET}
  help                          - Show this help
  quit, exit                    - Exit editor

{self.colors['subtitle']}📝 Item Types:{Colors.RESET} TITLE, SUBTITLE, REQUIREMENT, COMMENT, DATTR, UNKNOWN

{self.colors['info']}💡 Tip: Use line numbers from the display for editing commands{Colors.RESET}
"""
        print(help_text)
    
    def _create_new_document(self):
        """Create a new empty document."""
        # Create a minimal document structure
        empty_parts = [{
            'line_number': 1,
            'original_line': '# New Requirement Document',
            'type': 'TITLE',
            'indent': 0,
            'id': None,
            'description': 'New Requirement Document',
            'parent': None,
            'children': [],
            'children_refs': []
        }]
        
        self.md_editor = MarkdownEditor(empty_parts)
        self.current_file = None
        self.modified = True
        print(f"{self.colors['success']}✅ New document created.{Colors.RESET}")
    
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
            return False
        
        try:
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
    
    def _export_html(self, filename: str) -> bool:
        """Export document to HTML using project configuration if available."""
        if not self.md_editor:
            print(f"{self.colors['error']}❌ No document to export.{Colors.RESET}")
            return False
        
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
            line_num = int(args[1])
            item_type = args[2].upper()
            description = ' '.join(args[3:])
            
            if position == "before":
                result = self.md_editor.add_item_before(line_num, item_type, description)
            elif position == "after":
                result = self.md_editor.add_item_after(line_num, item_type, description)
            elif position == "under":
                result = self.md_editor.add_item_under(line_num, item_type, description)
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
            src_line = int(args[0])
            position = args[1].lower()
            target_line = int(args[2])
            
            if position == "before":
                success = self.md_editor.move_item_before(src_line, target_line)
            elif position == "after":
                success = self.md_editor.move_item_after(src_line, target_line)
            elif position == "under":
                success = self.md_editor.move_item_under(src_line, target_line)
            else:
                print(f"{self.colors['error']}❌ Invalid position. Use: before, after, or under{Colors.RESET}")
                return False
            
            if success:
                self.modified = True
                print(f"{self.colors['success']}✅ Moved item from line {src_line} {position} line {target_line}{Colors.RESET}")
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
                return False
            return self._load_file(args[0])
            
        elif command == "save":
            return self._save_file()
            
        elif command == "saveas":
            if not args:
                print(f"{self.colors['error']}❌ Usage: saveas <filename>{Colors.RESET}")
                return False
            return self._save_file(args[0])
            
        elif command == "export":
            if not args:
                print(f"{self.colors['error']}❌ Usage: export <filename>{Colors.RESET}")
                return False
            return self._export_html(args[0])
            
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
                    return False
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
                return False
        
        # Editing commands
        elif command == "add":
            return self._process_add_command(args)
            
        elif command == "move":
            return self._process_move_command(args)
            
        elif command == "delete":
            if not self.md_editor:
                print(f"{self.colors['error']}❌ No document loaded.{Colors.RESET}")
                return False
            if not args:
                print(f"{self.colors['error']}❌ Usage: delete <line>{Colors.RESET}")
                return False
            try:
                line_num = int(args[0])
                success = self.md_editor.delete_item(line_num)
                if success:
                    self.modified = True
                    print(f"{self.colors['success']}✅ Deleted item at line {line_num}{Colors.RESET}")
                    return True
                else:
                    print(f"{self.colors['error']}❌ Failed to delete item{Colors.RESET}")
                    return False
            except ValueError as e:
                print(f"{self.colors['error']}❌ Error: {e}{Colors.RESET}")
                return False
                
        elif command == "edit":
            if not self.md_editor:
                print(f"{self.colors['error']}❌ No document loaded.{Colors.RESET}")
                return False
            if len(args) < 2:
                print(f"{self.colors['error']}❌ Usage: edit <line> <new_description>{Colors.RESET}")
                return False
            try:
                line_num = int(args[0])
                new_description = ' '.join(args[1:])
                success = self.md_editor.update_content(line_num, new_description)
                if success:
                    self.modified = True
                    print(f"{self.colors['success']}✅ Updated item at line {line_num}{Colors.RESET}")
                    return True
                else:
                    print(f"{self.colors['error']}❌ Failed to update item{Colors.RESET}")
                    return False
            except ValueError as e:
                print(f"{self.colors['error']}❌ Error: {e}{Colors.RESET}")
                return False
        
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
                line_num = int(args[0])
                part = self.md_editor._find_part_by_line(line_num)
                if part:
                    print(f"{self.colors['success']}✅ Line {line_num} info:{Colors.RESET}")
                    print(f"  {self._format_line(part, True)}")
                    
                    # Show parent and children info
                    if part['parent']:
                        parent = self.md_editor._find_part_by_line(part['parent'])
                        print(f"  {self.colors['info']}Parent: Line {part['parent']} - {parent['description'][:30]}...{Colors.RESET}")
                    
                    if part['children']:
                        print(f"  {self.colors['info']}Children: {part['children']}{Colors.RESET}")
                else:
                    print(f"{self.colors['warning']}Line {line_num} not found{Colors.RESET}")
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
                    parts = shlex.split(user_input)
                    command = parts[0]
                    args = parts[1:]
                except ValueError:
                    # Fallback for quote parsing issues
                    parts = user_input.split()
                    command = parts[0]
                    args = parts[1:]
                
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
