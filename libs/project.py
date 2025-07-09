"""
Project Configuration Manager Module

This module provides functionality to manage project configuration files in JSON format
for the Requirement Editor application. It handles creation, loading, saving, and updating
of project configuration data including file paths, timestamps, and version information.

Key Features:
- Creates and manages JSON-based project configuration files
- Tracks input markdown file paths and project metadata
- Maintains creation and modification timestamps in standardized format
- Handles application version tracking for compatibility
- Provides comprehensive error handling for file operations
- Supports project configuration validation and migration

Configuration Data Structure:
- input_md_file_path: Path to the source markdown requirements document
- project_creation_date: When the project was first created (YYYY-MM-DD HH:MM)
- project_last_modification_date: When the project was last modified (YYYY-MM-DD HH:MM)
- application_version: Version of the Requirement Editor used

JSON Schema:
{
    "input_md_file_path": "path/to/requirements.md",
    "project_creation_date": "2025-07-09 14:40",
    "project_last_modification_date": "2025-07-09 15:20",
    "application_version": "1.0.0"
}

Author: Attila Gallai <attila@tux-net.hu>
Created: 2025
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
                "application_version": APPLICATION_VERSION
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
        print(f"Config File:       {self.config_file_path}")
        print("=" * 60)


def create_project_config(config_file_path: str, input_md_file_path: str) -> Optional[ProjectConfig]:
    """
    Convenience function to create a new project configuration.
    
    Creates a new ProjectConfig instance and initializes it with the specified
    input markdown file path. Handles the complete creation process.
    
    Args:
        config_file_path (str): Path where the project configuration JSON will be saved.
        input_md_file_path (str): Path to the source markdown requirements file.
    
    Returns:
        ProjectConfig: Configured ProjectConfig instance if successful.
        None: If creation failed due to errors.
        
    Example:
        >>> project = create_project_config("project.json", "requirements.md")
        >>> if project:
        ...     project.print_project_info()
    """
    try:
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
