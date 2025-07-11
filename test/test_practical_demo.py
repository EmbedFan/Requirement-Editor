#!/usr/bin/env python3
"""
Practical demonstration of project config creation in terminal editor context
"""

import os
import sys
import tempfile
from pathlib import Path

# Add libs to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'libs'))

def demonstrate_practical_usage():
    """Demonstrate how the config creation works in practical usage"""
    
    print("=" * 70)
    print("PRACTICAL DEMONSTRATION: Terminal Editor Config Creation")
    print("=" * 70)
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a realistic project structure
        project_dir = os.path.join(temp_dir, "my_project", "documents")
        os.makedirs(project_dir)
        
        print(f"📁 Project directory: {project_dir}")
        print(f"🏠 Current working directory: {os.getcwd()}")
        
        # Simulate creating a requirements document in the project directory
        md_file = os.path.join(project_dir, "system_requirements.md")
        
        # Create sample content (what the terminal editor would create)
        sample_content = """# System Requirements Document

## DATTR001 - Document Attributes
Created at: 2025-01-27 10:30:00
Modified at: 2025-01-27 10:30:00

## COM001 - Document Introduction
This document contains the system requirements for our new application.

## REQ001 - User Authentication
The system shall provide secure user authentication functionality.

## REQ002 - Data Storage  
The system shall store user data securely in an encrypted database.
"""
        
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(sample_content)
        
        print(f"📄 Created markdown file: {md_file}")
        
        # Simulate what happens when terminal editor saves a file
        from project import create_project_config
        
        base_name = os.path.splitext(os.path.basename(md_file))[0]
        project_config = create_project_config(md_file, base_name)
        
        if project_config:
            config_path = project_config.config_file_path
            print(f"⚙️  Created config file: {config_path}")
            
            # Show that both files are in the same directory
            md_dir = os.path.dirname(md_file)
            config_dir = os.path.dirname(config_path)
            
            print(f"\n📊 Directory Analysis:")
            print(f"   Markdown file directory: {md_dir}")
            print(f"   Config file directory:   {config_dir}")
            print(f"   Same directory? {'✅ YES' if md_dir == config_dir else '❌ NO'}")
            
            # List the contents of the project directory
            print(f"\n📂 Contents of project directory ({project_dir}):")
            for item in sorted(os.listdir(project_dir)):
                item_path = os.path.join(project_dir, item)
                if os.path.isfile(item_path):
                    print(f"   📄 {item}")
                else:
                    print(f"   📁 {item}/")
            
            # Show what this means for users
            print(f"\n🎯 User Benefits:")
            print(f"   1. Config file is kept with the document it manages")
            print(f"   2. Moving/copying documents preserves their settings")
            print(f"   3. No config files cluttering the working directory")
            print(f"   4. Easy to identify which config belongs to which document")
            
            return True
        else:
            print("❌ Failed to create project configuration")
            return False

if __name__ == "__main__":
    success = demonstrate_practical_usage()
    print(f"\n{'🎉 Demonstration completed successfully!' if success else '❌ Demonstration failed'}")
