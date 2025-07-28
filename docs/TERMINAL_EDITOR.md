# Terminal Editor for Requirement Documents

The Requirement Editor now includes a powerful terminal-based interface for interactive editing of requirement documents. This feature provides a command-line interface with comprehensive editing capabilities.

## 🚀 Getting Started

### Launch Terminal Editor

```bash
# Start with new document
python main.py -ed

# Start and load existing file (automatic .md extension)
python main.py -ed requirements          # Finds requirements.md automatically
python main.py -ed test/data/test_input  # Finds test_input.md automatically
python main.py -ed requirements.md       # Direct file specification
```

### Automatic File Extension Handling
The terminal editor automatically tries adding `.md` extension when files are not found:
- `python main.py -ed requirements` → looks for `requirements.md`
- `python main.py -ed specs.txt` → looks for `specs.md` if `specs.txt` doesn't exist
- Provides helpful feedback when files are found with automatic extension

### First Time Usage

1. **Start the editor**: `python main.py -ed`
2. **Create new document**: `new` (creates a document with title, dattr, comment, and sample requirement)
3. **View the default structure**: `list`
4. **Edit the default items**: 
   - `edit 1 'My Project Requirements'` (title)
   - ⚠️ **DATTR** (line 2) is read-only - contains timestamps managed by editor
   - `edit 3 'Created for project documentation'` (comment)
   - `edit 4 'My first requirement'` (requirement)
5. **Add more requirements**: `add after 4 REQUIREMENT 'System shall provide user authentication'`
6. **Save**: `saveas my_requirements.md` ⚠️ **Note**: Use `saveas` after `new` since no filename is set yet
7. **Get help anytime**: `help`

## 📚 Command Reference

### 📁 File Operations

| Command | Description | Example |
|---------|-------------|---------|
| `new` | Create new document with default structure | `new` |
| `load <file>` | Load markdown file (automatic .md extension) | `load requirements` or `load requirements.md` |
| `save` | Save current document ⚠️ | `save` |
| `saveas <file>` | Save as new filename | `saveas new_reqs.md` |
| `export [file]` | Export to HTML | `export` or `export output.html` |

⚠️ **Important**: After creating a new document with `new`, you must use `saveas <filename>` for the first save since no filename is set yet. The `save` command will show an error message but won't exit the program.

**Saveas Filename Processing**: The `saveas` command automatically handles filename extensions and file conflicts:

- **No extension**: Automatically adds `.md` extension
  - Input: `saveas my_document` → Output: `my_document.md`
- **Wrong extension**: Changes extension to `.md` with warning
  - Input: `saveas my_doc.txt` → Output: `my_doc.md` (with warning)
- **Correct extension**: Uses filename as-is
  - Input: `saveas my_doc.md` → Output: `my_doc.md` (no changes)
- **File exists**: Prompts for overwrite confirmation
  - Shows warning and asks "Do you want to overwrite it? (y/N)"
  - User can accept (y/yes) or decline (n/no/Enter)
  - Cancelling preserves the original file

**New Document Structure**: The `new` command creates a document with:
- **Title**: "New Requirement Document" 
- **DATTR**: Document timestamps (DATTR001) - *automatically managed, read-only*
- **Comment**: Default comment explaining document creation (COMM001)
- **Requirement**: Sample requirement that you can edit or replace (REQ001)

**DATTR Management**: DATTR items contain creation and modification timestamps in the format "Created at: YYYY-MM-DD HH:MM Modified at: YYYY-MM-DD HH:MM". These are automatically updated by the editor and cannot be modified by users.

**Export Functionality**: The `export` command provides flexible HTML export options:

- **Smart filename**: When used without a filename, automatically uses the current document name with `.html` extension
  - Example: If current document is `requirements.md`, `export` creates `requirements.html`
- **Custom filename**: When provided with a filename, uses the specified name
  - Example: `export custom_output.html` creates `custom_output.html`
- **New document handling**: For unsaved documents, provides helpful guidance to save first or specify a filename
  - Shows error: "The file doesn't have a filename yet" with suggestions
- **Backward compatible**: All existing export workflows continue to work

### ✏️ Document Editing

| Command | Description | Example |
|---------|-------------|---------|
| `add before <line> <type> <description>` | Add item before line | `add before 5 REQUIREMENT 'New requirement'` |
| `add after <line> <type> <description>` | Add item after line | `add after 3 COMMENT 'Important note'` |
| `add under <line> <type> <description>` | Add child under line | `add under 2 REQUIREMENT 'Sub-requirement'` |
| `move <src> before <target>` | Move item before target | `move 4 before 2` |
| `move <src> after <target>` | Move item after target | `move 6 after 8` |
| `move <src> under <target>` | Move item under target | `move 5 under 3` |
| `delete <line>` | Delete item and children | `delete 7` |
| `edit <line> <description>` | Edit description | `edit 4 'Updated requirement text'` |
| `witheditor <line>` | Edit description with external editor | `witheditor 4` |
| `type <line> <type>` | Change item type | `type 5 COMMENT` |

### 🔍 Navigation & Search

| Command | Description | Example |
|---------|-------------|---------|
| `list` | Display entire document | `list` |
| `list <start> <end>` | Display line range | `list 5 10` |
| `find <text>` | Search descriptions | `find 'authentication'` |
| `findid <id>` | Find by item ID | `findid 1001` |
| `goto <line>` | Show line details | `goto 5` |
| `refresh` | Refresh display | `refresh` |

### ⚙️ Display & Settings

| Command | Description | Example |
|---------|-------------|---------|
| `mode compact` | Set compact display mode | `mode compact` |
| `mode full` | Set full display mode | `mode full` |
| `status` | Show document status | `status` |

### ❓ System Commands

| Command | Description | Example |
|---------|-------------|---------|
| `help` | Show all commands | `help` |
| `quit` or `exit` | Exit editor | `quit` |

## 📝 Item Types

The editor supports these item types:

- **TITLE** - Document and section titles
- **SUBTITLE** - Section headers
- **REQUIREMENT** - Numbered requirements
- **COMMENT** - Comments and notes
- **DATTR** - Data attributes
- **UNKNOWN** - Other content

## 🎨 Display Features

### Color-Coded Output
- **Green**: Requirements
- **Yellow**: Comments  
- **Blue**: Subtitles
- **Magenta**: Data attributes
- **Cyan**: Information messages
- **Red**: Errors

### Document View
```
=== Requirement Editor ===                      [requirements.md] *modified*
  1│ # Requirement Document                                        [TITLE]
  2│   └─ 1001 REQ: System shall provide authentication            [REQ]
  3│     └─ 1002 COMM: *Uses OAuth 2.0 protocol*                 [COMM]
  4│   ** Security Requirements                                   [SUBTITLE]
  5│     └─ 1010 REQ: All data shall be encrypted                 [REQ] [+2]

Commands: add, move, delete, edit, find, save, export, quit
> _
```

## 💡 Pro Tips

### Efficient Editing Workflow
1. **Start with structure**: Create TITLE and SUBTITLE items first
2. **Add requirements**: Use `add under` to create hierarchical structure
3. **Add comments**: Use `add after` requirements to add explanatory comments
4. **Organize**: Use `move` commands to reorganize as needed
5. **Search efficiently**: Use `find` to locate items quickly

### Batch Operations
```bash
# Add multiple requirements quickly
add after 1 REQUIREMENT 'User authentication requirement'
add after 2 REQUIREMENT 'Password complexity requirement'
add after 3 REQUIREMENT 'Session management requirement'

# Search and organize
find 'security'
move 5 under 4
move 6 under 4
```

### File Management
```bash
# Save work frequently
save

# Export to HTML for review
export requirements.html

# Load different files
load project_specs.md
```

## 🔧 Advanced Features

### Line Number References
- All operations use line numbers shown in the display
- Line numbers automatically update after insertions/deletions
- Use `goto <line>` to see detailed item information

### Hierarchical Structure
- Items automatically maintain parent-child relationships
- Moving items adjusts indentation levels
- Use `add under` to create logical document hierarchy

### Search Capabilities
- Text search across all descriptions
- ID-based lookup for numbered items
- Case-insensitive search by default

### External Editor Integration
- **`witheditor <line>`**: Opens system text editor for editing descriptions
- **Perfect for long text**: Multi-line editing with full editor features
- **Cross-platform**: Works on Windows (Notepad) and Unix-like systems (nano/$EDITOR)
- **Safe operation**: Uses temporary files with automatic cleanup
- **UTF-8 support**: Full international character support
- **DATTR protection**: Prevents editing of read-only timestamp items

**Usage Examples:**
```bash
witheditor 4                    # Edit requirement #4 in external editor
witheditor 7                    # Edit comment #7 with full editor features
```

## 🏃‍♂️ Quick Start Example

```bash
# Start editor
python main.py -ed

# Create new document (with default structure including DATTR)
new

# View the default structure
list

# Customize the default content
edit 1 'User Authentication Requirements'
edit 2 'Authentication system metadata and configuration'  
edit 3 'Requirements for user login and security'
edit 4 'System shall provide secure user authentication'

# Add more requirements
add after 4 REQUIREMENT 'System shall enforce strong password policies'
add after 5 REQUIREMENT 'System shall support multi-factor authentication'

# View updated document
list

# Save work (automatically updates modification date with HH:mm)
saveas user_auth_requirements.md

# Export to HTML
export user_auth_requirements.html

# Exit
quit
```

## 🐛 Troubleshooting

### Common Issues

**"DATTR items are read-only" message when editing**
- This happens when you try to edit a DATTR item (line 2 in new documents)
- **Solution**: DATTR items contain timestamps managed automatically by the editor
- They are updated automatically when saving and cannot be manually edited

**"No filename specified" error when using `save`**
- This happens when you create a new document with `new` and try to use `save`
- **Solution**: Use `saveas <filename>` for the first save of a new document
- After the first save, you can use `save` to update the same file

**File not found when loading**
- Check file path is correct
- Use relative or absolute paths
- File must exist and be readable

**Colors not showing**
- Terminal must support ANSI color codes
- Most modern terminals support colors
- Commands work the same with or without colors

**Line numbers seem wrong**
- Line numbers update automatically after edits
- Use `refresh` to update display
- Use `goto <line>` to verify line contents

### Getting Help
- Type `help` in the editor for complete command list
- Use `status` to see document information
- Use `list` to see current document state

---

**Author**: Attila Gallai <attila@tux-net.hu>  
**License**: MIT License  
**Version**: 1.0.0
