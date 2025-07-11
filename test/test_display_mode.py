#!/usr/bin/env python3
"""
Test script to verify display mode saving and loading functionality.
"""

import os
import sys
import tempfile

# Add libs to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from project import ProjectConfig, create_project_config, load_project_config

def test_display_mode_functionality():
    """Test display mode saving and loading in project configuration."""
    
    print("🧪 Testing Display Mode Functionality...")
    
    # Create a temporary markdown file for testing
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        f.write("# Test Document\n\nThis is a test.")
        temp_md_path = f.name
    
    try:
        # Test 1: Create new project configuration with default display mode
        print("\n1. Testing new project creation with default display mode...")
        config_name = os.path.splitext(os.path.basename(temp_md_path))[0] + "_config"
        project_config = create_project_config(temp_md_path, config_name)
        
        if not project_config:
            print("❌ Failed to create project configuration")
            return False
        
        # Check default display mode
        display_mode = project_config.get_display_mode()
        print(f"   Default display mode: {display_mode}")
        if display_mode != "compact":
            print("❌ Default display mode should be 'compact'")
            return False
        print("✓ Default display mode is correct")
        
        # Test 2: Change display mode and save
        print("\n2. Testing display mode change and save...")
        project_config.set_display_mode("full")
        new_mode = project_config.get_display_mode()
        print(f"   Changed display mode to: {new_mode}")
        if new_mode != "full":
            print("❌ Display mode change failed")
            return False
        
        # Save the configuration
        if not project_config.save_project():
            print("❌ Failed to save project configuration")
            return False
        print("✓ Display mode changed and saved successfully")
        
        # Test 3: Load configuration and verify display mode persistence
        print("\n3. Testing display mode persistence after reload...")
        config_path = project_config.config_file_path
        
        # Create new instance and load from file
        loaded_config = load_project_config(config_path)
        if not loaded_config:
            print("❌ Failed to load project configuration")
            return False
        
        loaded_mode = loaded_config.get_display_mode()
        print(f"   Loaded display mode: {loaded_mode}")
        if loaded_mode != "full":
            print("❌ Display mode was not persisted correctly")
            return False
        print("✓ Display mode persisted correctly after reload")
        
        # Test 4: Test editor settings structure
        print("\n4. Testing editor settings structure...")
        editor_settings = loaded_config.get_editor_settings()
        print(f"   Editor settings: {editor_settings}")
        
        if not isinstance(editor_settings, dict):
            print("❌ Editor settings should be a dictionary")
            return False
        
        if "display_mode" not in editor_settings:
            print("❌ Display mode should be in editor settings")
            return False
        
        if editor_settings["display_mode"] != "full":
            print("❌ Display mode in editor settings is incorrect")
            return False
        
        print("✓ Editor settings structure is correct")
        
        # Test 5: Test changing back to compact
        print("\n5. Testing change back to compact mode...")
        loaded_config.set_display_mode("compact")
        if loaded_config.get_display_mode() != "compact":
            print("❌ Failed to change display mode back to compact")
            return False
        
        if loaded_config.save_project():
            print("✓ Successfully changed back to compact mode and saved")
        else:
            print("❌ Failed to save compact mode setting")
            return False
        
        print("\n🎉 All display mode tests passed!")
        return True
        
    finally:
        # Cleanup
        try:
            os.unlink(temp_md_path)
            if 'project_config' in locals():
                config_path = project_config.config_file_path
                if os.path.exists(config_path):
                    os.unlink(config_path)
        except:
            pass

if __name__ == "__main__":
    success = test_display_mode_functionality()
    if success:
        print("\n✅ Display mode functionality test completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Display mode functionality test failed!")
        sys.exit(1)
