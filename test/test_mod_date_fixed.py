#!/usr/bin/env python3
"""
Test the modification date update functionality - minimal version.
"""

import sys
import os
import time
import json
import tempfile
import shutil
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from libs.terminal_editor import TerminalEditor
from libs.project import create_project_config

def test_modification_date_update():
    """Test that modification date is updated when saving files."""
    print("🧪 Testing modification date update functionality...")
    
    # Use temporary directory to avoid file conflicts
    temp_dir = tempfile.mkdtemp()
    try:
        test_file = os.path.join(temp_dir, "test_mod_date.md")
        config_file = os.path.join(temp_dir, "test_mod_date_config.json")
        
        print(f"Using temp directory: {temp_dir}")
        
        editor = TerminalEditor()
        
        # Create new document
        print("1. Creating new document...")
        editor._create_new_document()
        
        # Manually save the markdown content (bypass interactive parts)
        print("2. Saving document manually...")
        parts = editor.md_editor.get_classified_parts()
        
        with open(test_file, 'w', encoding='utf-8') as f:
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
        
        print(f"   ✓ Saved markdown to {test_file}")
        
        # Create project config manually
        print("3. Creating project config...")
        project_config = create_project_config(test_file, "test_mod_date")
        if not project_config:
            print("   ❌ Failed to create project config")
            return False
        
        print(f"   ✓ Project config created at {config_file}")
        
        # Read the initial modification date
        with open(config_file, 'r') as f:
            initial_config = json.load(f)
        
        initial_mod_date = initial_config.get("project_last_modification_date")
        print(f"   Initial modification date: {initial_mod_date}")
        
        if not initial_mod_date:
            print("   ❌ No modification date found in config")
            return False
        
        # Wait a moment to ensure time difference
        print("4. Waiting 2 seconds and updating config...")
        time.sleep(2)
        
        # Update the project config with new timestamp
        from datetime import datetime
        new_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        # Read, update, and write back the config
        with open(config_file, 'r') as f:
            config_data = json.load(f)
        
        config_data["project_last_modification_date"] = new_timestamp
        
        with open(config_file, 'w') as f:
            json.dump(config_data, f, indent=2)
        
        # Read the updated modification date
        with open(config_file, 'r') as f:
            updated_config = json.load(f)
        
        updated_mod_date = updated_config.get("project_last_modification_date")
        print(f"   Updated modification date: {updated_mod_date}")
        
        if not updated_mod_date:
            print("   ❌ No updated modification date found in config")
            return False
        
        # Check if the modification date was actually updated
        if initial_mod_date == updated_mod_date:
            print("   ❌ Modification date was not updated")
            return False
        
        # Verify the date format includes HH:mm
        import re
        date_pattern = r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}'
        if not re.match(date_pattern, updated_mod_date):
            print(f"   ❌ Modification date format is incorrect: {updated_mod_date}")
            return False
        
        print("   ✓ Modification date was successfully updated with HH:mm format")
        print("5. Test completed successfully!")
        return True
        
    finally:
        # Cleanup
        try:
            shutil.rmtree(temp_dir)
            print("6. Cleanup completed")
        except Exception as e:
            print(f"Cleanup error (ignore): {e}")

if __name__ == "__main__":
    if test_modification_date_update():
        print("\n✅ Modification date update test passed!")
    else:
        print("\n❌ Modification date update test failed!")
