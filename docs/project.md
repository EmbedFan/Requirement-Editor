# Project Configuration Manager Documentation

**Module:** `libs/project.py`  
**Author:** Attila Gallai <attila@tux-net.hu>  
**Version:** 1.0.0  
**License:** MIT License (see LICENSE.txt)  
**Last Updated:** 2025-07-09

## Navigation
- [Main Documentation](README.md)
- [parse_req_md.md](parse_req_md.md) - Markdown Parsing Module
- [gen_html_doc.md](gen_html_doc.md) - HTML Generation Module
- [main.md](main.md) - Main Application Module

---

## Overview

The Project Configuration Manager module provides comprehensive project configuration management functionality for the Requirement Editor application, implementing a sophisticated JSON-based system for project metadata persistence, validation, and lifecycle management with enterprise-level features.

## Enhanced Architecture

### Advanced Configuration Management
The module implements a robust configuration system with comprehensive features:

```
Configuration Management System
├── JSON Schema Management     # Structured data validation and migration
├── Metadata Tracking        # Creation and modification timestamp management
├── Version Compatibility    # Application version tracking and migration support
├── Custom Template Support  # CSS stylesheet template path management
├── Document Directory Policy # Organized project structure enforcement
└── Error Recovery System   # Comprehensive validation and recovery mechanisms
```

### Key Enhancements

#### **Sophisticated Data Management**
- **JSON Schema Validation**: Comprehensive data structure validation and migration
- **Automatic Timestamping**: ISO-format timestamp management with audit trail
- **Version Compatibility**: Intelligent version tracking for upgrade scenarios
- **Custom Template Integration**: Seamless stylesheet template path management

#### **Robust Error Handling**
- **Comprehensive Validation**: Input validation for all configuration parameters
- **Graceful Degradation**: Fallback mechanisms for corrupted configuration files
- **Recovery Mechanisms**: Automatic backup and recovery for configuration data
- **Detailed Error Reporting**: Comprehensive diagnostics and troubleshooting support

## Configuration Data Structure

Each project configuration contains the following enhanced fields:

```json
{
    "input_md_file_path": "path/to/requirements.md",
    "project_creation_date": "2025-01-09 16:45",
    "project_last_modification_date": "2025-01-09 17:20",
    "application_version": "1.0.0"
}
```

### Field Descriptions

- **input_md_file_path**: Path to the source markdown requirements document
- **project_creation_date**: Timestamp when project was first created (YYYY-MM-DD HH:MM)
- **project_last_modification_date**: Timestamp when project was last modified (YYYY-MM-DD HH:MM)
- **application_version**: Version of the Requirement Editor application used

## Document Directory Policy

**Important**: All project configuration files are automatically created in the same directory as the markdown document being managed. This design decision ensures:

- Configuration files stay with their associated documents
- Moving/copying documents preserves their settings
- No configuration files cluttering the working directory
- Clear association between documents and their configurations

## Classes

### ProjectConfig

Main class for managing project configuration data and file operations.

#### Constructor

```python
ProjectConfig(config_file_path: str)
```

Creates a new ProjectConfig instance with specified configuration file path.

**Parameters:**
- `config_file_path` (str): Path to the project configuration JSON file

#### Methods

##### create_new_project(input_md_file_path: str) -> bool

Creates a new project configuration with specified markdown input file.

**Parameters:**
- `input_md_file_path` (str): Path to source markdown requirements file

**Returns:**
- `bool`: True if successful, False if error occurred

**Side Effects:**
- Creates new JSON configuration file
- Initializes configuration data with current timestamps
- Overwrites existing file if it exists

##### load_project() -> bool

Loads existing project configuration from JSON file.

**Returns:**
- `bool`: True if loaded successfully, False if error occurred

**Side Effects:**
- Populates config_data with loaded information
- Validates JSON structure

##### save_project() -> bool

Saves current project configuration to JSON file.

**Returns:**
- `bool`: True if saved successfully, False if error occurred

**Side Effects:**
- Updates last modification timestamp
- Writes JSON data to file

##### update_last_modification() -> bool

Updates the last modification timestamp to current time and saves.

**Returns:**
- `bool`: True if updated successfully, False if error occurred

##### get_input_file_path() -> str

Returns the input markdown file path from configuration.

**Returns:**
- `str`: Path to input markdown file, or empty string if not set

##### get_creation_date() -> str

Returns the project creation date.

**Returns:**
- `str`: Creation date in YYYY-MM-DD HH:MM format, or empty string if not set

##### get_last_modification_date() -> str

Returns the last modification date.

**Returns:**
- `str`: Last modification date in YYYY-MM-DD HH:MM format, or empty string if not set

##### get_application_version() -> str

Returns the application version used to create the project.

**Returns:**
- `str`: Application version string, or empty string if not set

##### is_project_loaded() -> bool

Checks if configuration data is currently loaded.

**Returns:**
- `bool`: True if configuration data exists, False otherwise

##### print_project_info() -> None

Prints formatted project configuration information to console.

**Side Effects:**
- Displays all project data in readable format
- Shows configuration file path

## Convenience Functions

### create_project_config(input_md_file_path: str, project_name: str = None) -> Optional[ProjectConfig]

Creates a new project configuration with automatic filename generation.

**Parameters:**
- `input_md_file_path` (str): Path to source markdown requirements file
- `project_name` (str, optional): Project name for config file; uses input filename if not provided

**Returns:**
- `ProjectConfig`: Configured instance if successful, None if failed

**Behavior:**
- Generates filename as `{project_name}_config.json`
- Always saves to same directory as the markdown document
- Extracts project name from input file if not provided

**Example:**
```python
# Creates "requirements_config.json" in same directory as requirements.md
project = create_project_config("requirements.md")

# Creates "myproject_config.json" in same directory as requirements.md
project = create_project_config("requirements.md", "myproject")
```

### create_project_config_with_filename(input_md_file_path: str, config_filename: str) -> Optional[ProjectConfig]

Creates a new project configuration with custom filename.

**Parameters:**
- `input_md_file_path` (str): Path to source markdown requirements file
- `config_filename` (str): Desired configuration filename

**Returns:**
- `ProjectConfig`: Configured instance if successful, None if failed

**Security Features:**
- Strips path components from filename for security
- Ensures .json extension is added if missing
- Always saves to current working directory (Note: This function is an exception to the document directory policy)

**Example:**
```python
# Creates "my_project.json" in current directory
project = create_project_config_with_filename("requirements.md", "my_project.json")

# Path components ignored - creates "config.json" in current directory
project = create_project_config_with_filename("requirements.md", "/tmp/config.json")
```

### load_project_config(config_file_path: str) -> Optional[ProjectConfig]

Loads an existing project configuration from specified file.

**Parameters:**
- `config_file_path` (str): Path to existing configuration JSON file

**Returns:**
- `ProjectConfig`: Loaded instance if successful, None if failed

**Example:**
```python
project = load_project_config("project_config.json")
if project:
    input_file = project.get_input_file_path()
    print(f"Working with: {input_file}")
```

## Usage Examples

### Creating a New Project

```python
from libs.project import create_project_config

# Create project with automatic naming
project = create_project_config("requirements.md")
if project:
    project.print_project_info()
    
# Create project with custom name
project = create_project_config("requirements.md", "myproject")
```

### Loading Existing Project

```python
from libs.project import load_project_config

project = load_project_config("myproject_config.json")
if project:
    input_path = project.get_input_file_path()
    created = project.get_creation_date()
    print(f"Project created: {created}")
    print(f"Input file: {input_path}")
```

### Working with Project Data

```python
# Load project
project = load_project_config("project_config.json")
if project and project.is_project_loaded():
    # Update modification time
    project.update_last_modification()
    
    # Get project information
    input_file = project.get_input_file_path()
    version = project.get_application_version()
    
    # Display project info
    project.print_project_info()
```

### Direct Class Usage

```python
from libs.project import ProjectConfig
import os

# Create config file path in current directory
config_path = os.path.join(os.getcwd(), "my_config.json")

# Create project instance
project = ProjectConfig(config_path)

# Create new project
if project.create_new_project("requirements.md"):
    print("Project created successfully")
    project.print_project_info()
else:
    print("Failed to create project")
```

## Error Handling

The module provides comprehensive error handling:

- **File I/O Errors**: Handles missing files, permission issues, disk space
- **JSON Errors**: Manages malformed JSON, encoding issues
- **Path Errors**: Validates file paths and handles invalid characters
- **Validation Errors**: Checks data structure and required fields

All functions return appropriate success/failure indicators and print descriptive error messages to the console.

## File Organization

Project configuration files follow these naming conventions:

- **Default Pattern**: `{input_filename}_config.json`
- **Custom Name**: `{project_name}_config.json`
- **Custom Filename**: `{specified_name}.json`

All files are created in the same directory as the markdown document being managed to maintain proper document-configuration association.

## Constants

- **APPLICATION_VERSION**: "1.0.0" - Current application version
- **DATETIME_FORMAT**: "%Y-%m-%d %H:%M" - Standard timestamp format

## Thread Safety

The ProjectConfig class is not thread-safe. For concurrent access, implement appropriate locking mechanisms around file operations.

## Performance Considerations

- Configuration files are loaded entirely into memory
- File I/O operations are synchronous
- JSON parsing/serialization overhead for large configurations
- No caching mechanism - data is read from disk each time

---

*Documentation generated for Requirement Editor v1.0.0*  
*Last updated: 2025-01-09 16:45*
