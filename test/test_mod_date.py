#!/usr/bin/env python3
"""
Test the modification date update functionality when saving.
"""

import sys
import os
import time
import json
import tempfile
import shutil
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from libs.terminal_editor import TerminalEditor

def test_modification_date_update():
    """Test that modification date is updated when saving files."""
    print("🧪 Testing modification date update functionality...")
    
    # Use temporary directory to avoid file conflicts
    temp_dir = tempfile.mkdtemp()
    try:
        test_file = os.path.join(temp_dir, "test_mod_date.md")
        config_file = os.path.join(temp_dir, "test_mod_date_config.json")
        
        # Ensure files don't exist
        if os.path.exists(test_file):
            os.remove(test_file)
        if os.path.exists(config_file):
            os.remove(config_file)
            
        editor = TerminalEditor()
        
        # Create new document
        print("1. Creating new document...")
        editor._create_new_document()
        
        # Save the document to create a project config
        print("2. Saving document for the first time...")
        result = editor._save_file(test_file)
        if not result:
            print("   ❌ Failed to save document")
            return False
        
        # Check if project config was created
        if not os.path.exists(config_file):
            print(f"   ❌ Project config file not created at {config_file}")
            return False
        
        # Read the initial modification date
        with open(config_file, 'r') as f:
            initial_config = json.load(f)
        
        initial_mod_date = initial_config.get("project_last_modification_date")
        print(f"   Initial modification date: {initial_mod_date}")
        
        if not initial_mod_date:
            print("   ❌ No modification date found in config")
            return False
        
        # Wait a moment to ensure time difference
        print("3. Waiting 2 seconds and then saving again...")
        time.sleep(2)
        
        # Save the document again (should not trigger overwrite prompt since current_file is set)
        result = editor._save_file()
        if not result:
            print("   ❌ Failed to save document second time")
            return False
        
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
        print("4. Test completed successfully!")
        return True
        
    finally:
        # Cleanup
        try:
            shutil.rmtree(temp_dir)
            print("5. Cleanup completed")
        except:
            pass

if __name__ == "__main__":
    if test_modification_date_update():
        print("\n✅ Modification date update test passed!")
    else:
        print("\n❌ Modification date update test failed!")
