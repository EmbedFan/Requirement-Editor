# Terminal Editor for Requirement Documents

The Requirement Editor now includes a powerful terminal-based interface for interactive editing of requirement documents. This feature provides a command-line interface with comprehensive editing capabilities.

## 🚀 Getting Started

### Launch Terminal Editor

```bash
# Start with new document
python main.py -ed

# Start and load existing file
python main.py -ed requirements.md
python main.py -ed test/data/test_input.md
```

### First Time Usage

1. **Start the editor**: `python main.py -ed`
2. **Create new document**: `new`
3. **Add your first requirement**: `add after 1 REQUIREMENT 'System shall provide user authentication'`
4. **View document**: `list`
5. **Save**: `saveas my_requirements.md`
6. **Get help anytime**: `help`

## 📚 Command Reference

### 📁 File Operations

| Command | Description | Example |
|---------|-------------|---------|
| `new` | Create new document | `new` |
| `load <file>` | Load markdown file | `load requirements.md` |
| `save` | Save current document | `save` |
| `saveas <file>` | Save as new filename | `saveas new_reqs.md` |
| `export <file>` | Export to HTML | `export output.html` |

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

## 🏃‍♂️ Quick Start Example

```bash
# Start editor
python main.py -ed

# Create basic document structure
new
add after 1 SUBTITLE 'User Requirements'
add under 2 REQUIREMENT 'System shall provide user login'
add after 3 COMMENT 'Authentication via OAuth 2.0'
add after 2 SUBTITLE 'Security Requirements'
add under 5 REQUIREMENT 'All passwords shall be hashed'

# View result
list

# Save work
saveas user_requirements.md

# Export to HTML
export user_requirements.html

# Exit
quit
```

## 🐛 Troubleshooting

### Common Issues

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
