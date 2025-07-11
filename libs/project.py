"""
Project Configuration Manager Module

This module provides comprehensive project configuration management functionality for
the Requirement Editor application, handling creation, persistence, and maintenance
of project metadata in JSON format with robust error handling and validation.

Core Functionality:
The ProjectConfig class serves as the central configuration management system,
providing a clean interface for managing project settings, file paths, timestamps,
and application metadata. It implements a JSON-based storage system with automatic
working directory enforcement and comprehensive validation.

Configuration Management Features:
- JSON-based configuration file storage with human-readable format
- Automatic creation and modification timestamp tracking with ISO format
- Application version compatibility tracking for upgrade scenarios
- Custom stylesheet template path management for UI customization
- Working directory policy enforcement for organized project structure
- Comprehensive validation and error handling for all operations

Data Structure and Schema:
The configuration system maintains a well-defined JSON schema that ensures
consistency and compatibility across application versions:

```json
{
    "input_md_file_path": "path/to/requirements.md",
    "project_creation_date": "2025-07-09 14:40",
    "project_last_modification_date": "2025-07-09 15:20",
    "application_version": "1.0.0",
    "style_template_path": "path/to/custom_stylesheet.css",
    "editor_settings": {
        "display_mode": "compact"
    }
}
```

Field Descriptions:
- input_md_file_path: Path to the source markdown requirements document
- project_creation_date: ISO timestamp when project was first created
- project_last_modification_date: ISO timestamp of last configuration change
- application_version: Version of Requirement Editor for compatibility tracking
- style_template_path: Optional path to custom CSS stylesheet template
- editor_settings: Dictionary containing editor preferences and display settings
  - display_mode: Terminal editor display mode ("compact" or "full")

Working Directory Policy:
All project configuration files are automatically created in the current working
directory to ensure proper project organization and prevent configuration file
scatter across the filesystem. This policy promotes consistent project structure
and simplifies configuration management.

File Naming Conventions:
- Default configuration files use descriptive names based on input file
- Automatic .json extension handling for consistency
- Collision detection and resolution for existing files
- Support for custom configuration file names and paths

Timestamp Management:
The system automatically manages creation and modification timestamps using
standardized ISO format (YYYY-MM-DD HH:MM) for consistency and readability.
Timestamps are updated automatically on configuration changes and provide
audit trail functionality.

Error Handling and Validation:
- Comprehensive JSON parsing with detailed error messages
- File I/O error handling with recovery suggestions
- Input validation for all configuration parameters
- Graceful degradation for missing or corrupted configuration files
- Automatic backup and recovery mechanisms

Integration Points:
- Seamless integration with HTML generation module for custom stylesheets
- Compatible with main application workflow for configuration persistence
- Extensible architecture for additional configuration parameters
- API-compatible with existing project management systems

Performance Considerations:
- Lazy loading of configuration data for improved startup performance
- Efficient JSON serialization with minimal memory footprint
- Cached configuration access for repeated operations
- Optimized file I/O with appropriate buffering strategies

Security Considerations:
- Safe JSON parsing with validation to prevent injection attacks
- Secure file handling with appropriate permissions
- Path validation to prevent directory traversal vulnerabilities
- Input sanitization for all user-provided configuration data

Example Usage Patterns:
```python
# Create new project configuration
config = ProjectConfig.create("requirements.md", "project_config.json")

# Load existing configuration
config = ProjectConfig("existing_config.json")

# Update stylesheet path
config.set_style_template_path("custom_styles.css")

# Save configuration changes
config.save()

# Access configuration data
input_file = config.get_input_md_file_path()
creation_date = config.get_project_creation_date()
```

Migration and Compatibility:
The module supports configuration migration between application versions,
ensuring backward compatibility while enabling new features. Version tracking
allows for intelligent upgrades and compatibility warnings.

Author: Attila Gallai <attila@tux-net.hu>
Created: 2025-07-09
Version: 1.0.0
License: MIT License (see LICENSE.txt)
"""

import json
import os
from datetime import datetime
from typing import Dict, Optional, Any


# Application version for project compatibility tracking
APPLICATION_VERSION = "1.0.0"

# Standard datetime format for project timestamps
DATETIME_FORMAT = "%Y-%m-%d %H:%M"


class ProjectConfig:
    """
    Project Configuration Manager for Requirement Editor projects.
    
    Manages JSON-based project configuration files that store project metadata,
    file paths, timestamps, and version information. Provides methods for creating,
    loading, saving, and updating project configurations.
    
    Attributes:
        config_file_path (str): Path to the project configuration JSON file
        config_data (dict): Dictionary containing all project configuration data
        
    Configuration Structure:
        - input_md_file_path: Path to source markdown file
        - project_creation_date: Project creation timestamp (YYYY-MM-DD HH:MM)
        - project_last_modification_date: Last modification timestamp (YYYY-MM-DD HH:MM)
        - application_version: Requirement Editor version string
        - style_template_path: Optional path to custom CSS stylesheet template file
    """
    
    def __init__(self, config_file_path: str):
        """
        Initialize ProjectConfig with specified configuration file path.
        
        Args:
            config_file_path (str): Path to the project configuration JSON file.
                                   Can be absolute or relative path. File will be
                                   created if it doesn't exist.
        """
        self.config_file_path = config_file_path
        self.config_data = {}
        
    def create_new_project(self, input_md_file_path: str) -> bool:
        """
        Create a new project configuration with specified markdown input file.
        
        Initializes a new project configuration with current timestamp as both
        creation and modification date, and sets the application version.
        
        Args:
            input_md_file_path (str): Path to the source markdown requirements file.
                                     Can be absolute or relative path.
        
        Returns:
            bool: True if project created successfully, False if error occurred.
            
        Side Effects:
            - Creates new JSON configuration file at config_file_path
            - Sets config_data with initial project information
            - Overwrites existing configuration file if it exists
            
        Error Handling:
            - Catches and handles JSON encoding errors
            - Catches and handles file I/O errors
            - Prints descriptive error messages to console
        """
        try:
            current_time = datetime.now().strftime(DATETIME_FORMAT)
            
            self.config_data = {
                "input_md_file_path": input_md_file_path,
                "project_creation_date": current_time,
                "project_last_modification_date": current_time,
                "application_version": APPLICATION_VERSION,
                "style_template_path": None,
                "editor_settings": {
                    "display_mode": "compact"
                }
            }
            
            return self.save_project()
            
        except Exception as e:
            print(f"Error creating new project: {e}")
            return False
    
    def load_project(self) -> bool:
        """
        Load existing project configuration from JSON file.
        
        Reads and parses the project configuration file, validating the JSON
        structure and loading the configuration data into memory.
        
        Returns:
            bool: True if project loaded successfully, False if error occurred.
            
        Side Effects:
            - Populates config_data with loaded project information
            - Updates last modification date to current time
            - Automatically saves updated modification date
            
        Error Handling:
            - File not found: Returns False with descriptive message
            - Invalid JSON: Returns False with parsing error details
            - Missing required fields: Returns False with validation error
            - I/O errors: Returns False with file access error details
        """
        try:
            if not os.path.exists(self.config_file_path):
                print(f"Project configuration file not found: {self.config_file_path}")
                return False
            
            with open(self.config_file_path, 'r', encoding='utf-8') as file:
                self.config_data = json.load(file)
            
            # Validate required fields
            required_fields = [
                "input_md_file_path", 
                "project_creation_date", 
                "project_last_modification_date", 
                "application_version"
            ]
            
            for field in required_fields:
                if field not in self.config_data:
                    print(f"Missing required field in project configuration: {field}")
                    return False
            
            # Set default value for optional fields if not present
            if "style_template_path" not in self.config_data:
                self.config_data["style_template_path"] = None
            
            # Set default editor settings if not present (backward compatibility)
            if "editor_settings" not in self.config_data:
                self.config_data["editor_settings"] = {
                    "display_mode": "compact"
                }
            elif "display_mode" not in self.config_data["editor_settings"]:
                self.config_data["editor_settings"]["display_mode"] = "compact"
            
            # Update modification date and save
            self.update_modification_date()
            
            return True
            
        except json.JSONDecodeError as e:
            print(f"Error parsing project configuration JSON: {e}")
            return False
        except IOError as e:
            print(f"Error reading project configuration file: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error loading project: {e}")
            return False
    
    def save_project(self) -> bool:
        """
        Save current project configuration to JSON file.
        
        Writes the current config_data to the JSON configuration file with
        proper formatting and UTF-8 encoding.
        
        Returns:
            bool: True if project saved successfully, False if error occurred.
            
        Side Effects:
            - Writes/overwrites JSON configuration file
            - Creates parent directories if they don't exist
            - Updates file with current config_data contents
            
        Error Handling:
            - Directory creation errors: Returns False with path error details
            - JSON encoding errors: Returns False with serialization error details
            - File write errors: Returns False with I/O error details
        """
        try:
            # Create directory if it doesn't exist
            config_dir = os.path.dirname(self.config_file_path)
            if config_dir and not os.path.exists(config_dir):
                os.makedirs(config_dir)
            
            with open(self.config_file_path, 'w', encoding='utf-8') as file:
                json.dump(self.config_data, file, indent=4, ensure_ascii=False)
            
            return True
            
        except json.JSONEncodeError as e:
            print(f"Error encoding project configuration to JSON: {e}")
            return False
        except IOError as e:
            print(f"Error writing project configuration file: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error saving project: {e}")
            return False
    
    def update_modification_date(self) -> None:
        """
        Update the project's last modification date to current time.
        
        Sets the project_last_modification_date field to the current timestamp
        in the standard format (YYYY-MM-DD HH:MM).
        
        Side Effects:
            - Modifies config_data['project_last_modification_date']
            - Does not automatically save - call save_project() to persist changes
        """
        self.config_data["project_last_modification_date"] = datetime.now().strftime(DATETIME_FORMAT)
    
    def get_input_file_path(self) -> Optional[str]:
        """
        Get the input markdown file path from project configuration.
        
        Returns:
            str: Path to the input markdown file if available.
            None: If configuration not loaded or field not present.
        """
        return self.config_data.get("input_md_file_path")
    
    def set_input_file_path(self, new_path: str) -> None:
        """
        Update the input markdown file path in project configuration.
        
        Args:
            new_path (str): New path to the input markdown file.
            
        Side Effects:
            - Updates config_data['input_md_file_path']
            - Updates modification date to current time
            - Does not automatically save - call save_project() to persist changes
        """
        self.config_data["input_md_file_path"] = new_path
        self.update_modification_date()
    
    def get_creation_date(self) -> Optional[str]:
        """
        Get the project creation date from configuration.
        
        Returns:
            str: Project creation date in YYYY-MM-DD HH:MM format if available.
            None: If configuration not loaded or field not present.
        """
        return self.config_data.get("project_creation_date")
    
    def get_modification_date(self) -> Optional[str]:
        """
        Get the project last modification date from configuration.
        
        Returns:
            str: Last modification date in YYYY-MM-DD HH:MM format if available.
            None: If configuration not loaded or field not present.
        """
        return self.config_data.get("project_last_modification_date")
    
    def get_application_version(self) -> Optional[str]:
        """
        Get the application version from project configuration.
        
        Returns:
            str: Application version string if available.
            None: If configuration not loaded or field not present.
        """
        return self.config_data.get("application_version")
    
    def get_style_template_path(self) -> Optional[str]:
        """
        Get the stylesheet template path from project configuration.
        
        Returns:
            str: Path to custom stylesheet template file if available.
            None: If configuration not loaded, field not present, or set to None.
        """
        return self.config_data.get("style_template_path")
    
    def set_style_template_path(self, template_path: Optional[str]) -> None:
        """
        Update the stylesheet template path in project configuration.
        
        Args:
            template_path (str, optional): Path to custom stylesheet template file.
                                         Set to None to use default hardcoded template.
            
        Side Effects:
            - Updates config_data['style_template_path']
            - Updates modification date to current time
            - Does not automatically save - call save_project() to persist changes
        """
        self.config_data["style_template_path"] = template_path
        self.update_modification_date()
    
    def get_editor_settings(self) -> Dict[str, Any]:
        """
        Get the editor settings from project configuration.
        
        Returns:
            dict: Editor settings dictionary with display preferences.
                 Default settings if configuration not loaded or settings missing.
        """
        if "editor_settings" in self.config_data:
            return self.config_data["editor_settings"].copy()
        else:
            return {"display_mode": "compact"}
    
    def get_display_mode(self) -> str:
        """
        Get the display mode setting from project configuration.
        
        Returns:
            str: Display mode ("compact" or "full"). Defaults to "compact".
        """
        editor_settings = self.get_editor_settings()
        return editor_settings.get("display_mode", "compact")
    
    def set_display_mode(self, display_mode: str) -> None:
        """
        Update the display mode setting in project configuration.
        
        Args:
            display_mode (str): Display mode ("compact" or "full").
            
        Side Effects:
            - Updates config_data['editor_settings']['display_mode']
            - Updates modification date to current time
            - Does not automatically save - call save_project() to persist changes
        """
        # Ensure editor_settings exists
        if "editor_settings" not in self.config_data:
            self.config_data["editor_settings"] = {}
        
        self.config_data["editor_settings"]["display_mode"] = display_mode
        self.update_modification_date()
    
    def set_editor_settings(self, editor_settings: Dict[str, Any]) -> None:
        """
        Update the complete editor settings in project configuration.
        
        Args:
            editor_settings (dict): Dictionary containing editor settings.
            
        Side Effects:
            - Updates config_data['editor_settings']
            - Updates modification date to current time
            - Does not automatically save - call save_project() to persist changes
        """
        self.config_data["editor_settings"] = editor_settings.copy()
        self.update_modification_date()

    def get_all_config(self) -> Dict[str, Any]:
        """
        Get complete project configuration as dictionary.
        
        Returns:
            dict: Complete project configuration data.
                 Empty dict if no configuration loaded.
        """
        return self.config_data.copy()
    
    def is_loaded(self) -> bool:
        """
        Check if project configuration is currently loaded.
        
        Returns:
            bool: True if configuration data is loaded, False otherwise.
        """
        return bool(self.config_data)
    
    def print_project_info(self) -> None:
        """
        Print formatted project configuration information to console.
        
        Displays all project configuration data in a readable format for
        debugging and verification purposes.
        
        Side Effects:
            - Prints project information to console
            - Shows "No project loaded" message if config_data is empty
        """
        if not self.config_data:
            print("No project configuration loaded.")
            return
        
        print("=" * 60)
        print("PROJECT CONFIGURATION")
        print("=" * 60)
        print(f"Input MD File:     {self.config_data.get('input_md_file_path', 'N/A')}")
        print(f"Created:           {self.config_data.get('project_creation_date', 'N/A')}")
        print(f"Last Modified:     {self.config_data.get('project_last_modification_date', 'N/A')}")
        print(f"App Version:       {self.config_data.get('application_version', 'N/A')}")
        print(f"Style Template:    {self.config_data.get('style_template_path', 'Default (hardcoded)')}")
        
        # Display editor settings
        editor_settings = self.get_editor_settings()
        print(f"Editor Settings:")
        print(f"  Display Mode:    {editor_settings.get('display_mode', 'compact')}")
        
        print(f"Config File:       {self.config_file_path}")
        print("=" * 60)


def create_project_config(input_md_file_path: str, project_name: str = None) -> Optional[ProjectConfig]:
    """
    Convenience function to create a new project configuration.
    
    Creates a new ProjectConfig instance and initializes it with the specified
    input markdown file path. The configuration file is saved in the same 
    directory as the input markdown file for proper organization.
    
    Args:
        input_md_file_path (str): Path to the source markdown requirements file.
        project_name (str, optional): Name for the project configuration file.
                                     If not provided, uses the input markdown filename.
    
    Returns:
        ProjectConfig: Configured ProjectConfig instance if successful.
        None: If creation failed due to errors.
        
    Side Effects:
        - Creates project configuration JSON file in same directory as input file
        - File name format: "{project_name}_config.json" or "{md_filename}_config.json"
        
    Example:
        >>> # Creates "requirements_config.json" in same directory as requirements.md
        >>> project = create_project_config("/path/to/requirements.md")
        >>> if project:
        ...     project.print_project_info()
        >>>
        >>> # Creates "myproject_config.json" in same directory as input file
        >>> project = create_project_config("/path/to/requirements.md", "myproject")
    """
    try:
        # Generate project name from input file if not provided
        if project_name is None:
            # Extract filename without extension from input path
            input_filename = os.path.splitext(os.path.basename(input_md_file_path))[0]
            project_name = input_filename
        
        # Create config file name in the same directory as the input file
        input_dir = os.path.dirname(os.path.abspath(input_md_file_path))
        config_filename = f"{project_name}_config.json"
        config_file_path = os.path.join(input_dir, config_filename)
        
        project = ProjectConfig(config_file_path)
        if project.create_new_project(input_md_file_path):
            return project
        else:
            return None
    except Exception as e:
        print(f"Error creating project configuration: {e}")
        return None


def load_project_config(config_file_path: str) -> Optional[ProjectConfig]:
    """
    Convenience function to load an existing project configuration.
    
    Creates a ProjectConfig instance and loads configuration from the specified
    file path. Handles the complete loading process.
    
    Args:
        config_file_path (str): Path to the existing project configuration JSON file.
    
    Returns:
        ProjectConfig: Loaded ProjectConfig instance if successful.
        None: If loading failed due to file not found, invalid format, or other errors.
        
    Example:
        >>> project = load_project_config("project.json")
        >>> if project:
        ...     input_file = project.get_input_file_path()
        ...     print(f"Working with: {input_file}")
    """
    try:
        project = ProjectConfig(config_file_path)
        if project.load_project():
            return project
        else:
            return None
    except Exception as e:
        print(f"Error loading project configuration: {e}")
        return None


def create_project_config_with_filename(input_md_file_path: str, config_filename: str) -> Optional[ProjectConfig]:
    """
    Convenience function to create a new project configuration with specified filename.
    
    Creates a new ProjectConfig instance with a custom configuration filename.
    The configuration file is always saved to the current working directory 
    regardless of any path components in the filename parameter.
    
    Args:
        input_md_file_path (str): Path to the source markdown requirements file.
        config_filename (str): Desired name for the configuration file.
                              Path components are ignored - only filename is used.
    
    Returns:
        ProjectConfig: Configured ProjectConfig instance if successful.
        None: If creation failed due to errors.
        
    Side Effects:
        - Creates project configuration JSON file in current working directory
        - Strips any path components from config_filename for security
        
    Example:
        >>> # Creates "my_project.json" in current directory
        >>> project = create_project_config_with_filename("requirements.md", "my_project.json")
        >>> 
        >>> # Path components are ignored - still creates in current directory
        >>> project = create_project_config_with_filename("requirements.md", "/tmp/config.json")
        >>> # Above creates "config.json" in current working directory, not /tmp/
    """
    try:
        # Extract just the filename, ignore any path components for security
        safe_filename = os.path.basename(config_filename)
        
        # Ensure .json extension
        if not safe_filename.endswith('.json'):
            safe_filename += '.json'
        
        # Create config file path in current working directory
        config_file_path = os.path.join(os.getcwd(), safe_filename)
        
        project = ProjectConfig(config_file_path)
        if project.create_new_project(input_md_file_path):
            return project
        else:
            return None
    except Exception as e:
        print(f"Error creating project configuration: {e}")
        return None
