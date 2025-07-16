#!/usr/bin/env python3
"""
Comprehensive Test Suite Validation

This script validates that all components of the Requirement Editor are working
correctly after the test reorganization.

Author: Attila Gallai <attila@tux-net.hu>
License: MIT License (see LICENSE.txt)
"""

import os
import sys
from pathlib import Path

# Add parent directory to Python path to access libs
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from libs.project import create_project_config, load_project_config
from libs.parse_req_md import ReadMDFile, ClassifyParts
from libs.gen_html_doc import GenerateHTML


def test_complete_workflow():
    """Test the complete workflow from markdown to HTML with project config."""
    
    print("=" * 70)
    print("COMPREHENSIVE WORKFLOW TEST")
    print("=" * 70)
    
    # Test data paths
    test_data_dir = Path(__file__).parent / "data"
    test_input_md = test_data_dir / "test_input.md"
    config_file = test_data_dir / "workflow_test_config.json"
    
    try:
        # Step 1: Test project configuration
        print("\n1. Testing Project Configuration Creation...")
        project = create_project_config(str(test_input_md), "workflow_test")
        
        if project:
            print("✓ Project configuration created successfully")
            # Config file is created in the same directory as the input markdown file
            if config_file.exists():
                print(f"✓ Config file exists at: {config_file}")
            else:
                print("✗ Config file not found in expected location")
                return False
        else:
            print("✗ Failed to create project configuration")
            return False
        
        # Step 2: Test markdown reading
        print("\n2. Testing Markdown File Reading...")
        md_content = ReadMDFile(str(test_input_md))
        
        if md_content:
            print(f"✓ Successfully read {len(md_content)} characters from markdown file")
        else:
            print("✗ Failed to read markdown file")
            return False
        
        # Step 3: Test content classification
        print("\n3. Testing Content Classification...")
        classified_parts = ClassifyParts(md_content)
        
        if classified_parts:
            print(f"✓ Successfully classified {len(classified_parts)} parts")
            
            # Count different types
            types_count = {}
            for part in classified_parts:
                part_type = part.get('type', 'UNKNOWN')
                types_count[part_type] = types_count.get(part_type, 0) + 1
            
            print("   Content breakdown:")
            for part_type, count in types_count.items():
                print(f"   - {part_type}: {count}")
        else:
            print("✗ Failed to classify markdown content")
            return False
        
        # Step 4: Test HTML generation
        print("\n4. Testing HTML Generation...")
        html_content = GenerateHTML(classified_parts)
        
        if html_content and len(html_content) > 1000:  # Reasonable size check
            print(f"✓ Successfully generated HTML ({len(html_content)} characters)")
            
            # Check for key HTML elements
            required_elements = [
                '<!DOCTYPE html>',
                '<html',  # Allow for attributes like <html lang="en">
                '<head>',
                '<body>',
                'expand-btn',
                'collapse-btn',
                'toggle-btn',
                'print-btn'
            ]
            
            missing_elements = []
            for element in required_elements:
                if element not in html_content:
                    missing_elements.append(element)
            
            if not missing_elements:
                print("✓ All required HTML elements present")
            else:
                print(f"⚠ Missing HTML elements: {missing_elements}")
        else:
            print("✗ Failed to generate valid HTML content")
            return False
        
        # Step 5: Test project loading
        print("\n5. Testing Project Configuration Loading...")
        loaded_project = load_project_config(str(config_file))
        
        if loaded_project:
            print("✓ Successfully loaded project configuration")
            
            # Verify data integrity
            original_input = project.get_input_file_path()
            loaded_input = loaded_project.get_input_file_path()
            
            if original_input == loaded_input:
                print("✓ Project data integrity verified")
            else:
                print(f"✗ Data mismatch: {original_input} != {loaded_input}")
                return False
        else:
            print("✗ Failed to load project configuration")
            return False
        
        # Step 6: Test Terminal Editor Integration Points
        print("\n6. Testing Terminal Editor Integration Points...")
        
        # Test that we can import terminal editor modules
        try:
            from libs.terminal_editor import TerminalEditor
            print("✓ Terminal editor module imports successfully")
            
            # Test that terminal editor can be instantiated with project config support
            editor = TerminalEditor()
            if hasattr(editor, 'project_config'):
                print("✓ Terminal editor has project_config attribute")
            else:
                print("✗ Terminal editor missing project_config attribute")
                return False
                
            # Test that the required project config methods exist
            required_methods = ['_load_project_config', '_save_project_config', '_show_project_info']
            for method in required_methods:
                if hasattr(editor, method):
                    print(f"✓ Terminal editor has {method} method")
                else:
                    print(f"✗ Terminal editor missing {method} method")
                    return False
            
        except ImportError as e:
            print(f"✗ Failed to import terminal editor: {e}")
            return False
        except Exception as e:
            print(f"✗ Error testing terminal editor integration: {e}")
            return False

        print("\n" + "=" * 70)
        print("🎉 ALL WORKFLOW TESTS PASSED SUCCESSFULLY!")
        print("=" * 70)
        
        return True
        
    except Exception as e:
        print(f"\n✗ WORKFLOW TEST FAILED: {e}")
        return False
    
    finally:
        # Clean up
        if config_file.exists():
            config_file.unlink()
            print(f"\n🧹 Cleaned up test file: {config_file}")


def test_file_structure():
    """Verify that all required files and directories exist."""
    
    print("\n" + "=" * 70)
    print("FILE STRUCTURE VALIDATION")
    print("=" * 70)
    
    project_root = Path(__file__).parent.parent
    
    required_files = [
        "main.py",
        "LICENSE",
        "README.md",
        "libs/parse_req_md.py",
        "libs/gen_html_doc.py", 
        "libs/project.py",
        "docs/README.md",
        "docs/main.md",
        "docs/parse_req_md.md",
        "docs/gen_html_doc.md",
        "docs/project.md",
        "test/test_runner.py",
        "test/test_project_config.py",
        "test/README.md",
        "test/data/test_input.md"
    ]
    
    missing_files = []
    existing_files = []
    
    for file_path in required_files:
        full_path = project_root / file_path
        if full_path.exists():
            existing_files.append(file_path)
            print(f"✓ {file_path}")
        else:
            missing_files.append(file_path)
            print(f"✗ {file_path}")
    
    print(f"\nSummary: {len(existing_files)}/{len(required_files)} files present")
    
    if missing_files:
        print(f"Missing files: {missing_files}")
        return False
    else:
        print("✓ All required files present!")
        return True


if __name__ == "__main__":
    print("Starting Comprehensive Test Suite...")
    
    # Run file structure validation
    structure_ok = test_file_structure()
    
    # Run workflow test
    workflow_ok = test_complete_workflow()
    
    # Final result
    print("\n" + "=" * 70)
    print("FINAL TEST RESULTS")
    print("=" * 70)
    
    if structure_ok and workflow_ok:
        print("🎉 ALL TESTS PASSED - SYSTEM FULLY FUNCTIONAL!")
        sys.exit(0)
    else:
        print("❌ SOME TESTS FAILED - PLEASE CHECK OUTPUT ABOVE")
        sys.exit(1)
