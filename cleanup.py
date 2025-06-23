#!/usr/bin/env python3
"""
Cleanup script to remove old files after migration.
This script will remove the old src directory and other files
that are no longer needed after migrating to the new package structure.
"""

import os
import shutil
import sys
from pathlib import Path

def remove_old_src():
    """Remove the old src directory."""
    project_root = Path(__file__).parent.absolute()
    src_dir = project_root / "src"
    
    if not src_dir.exists():
        print("The src directory does not exist. Nothing to remove.")
        return
    
    print(f"Found old src directory at {src_dir}")
    
    # Ask for confirmation
    confirm = input("Are you sure you want to remove the old src directory? [y/N] ")
    if confirm.lower() != 'y':
        print("Aborted. The src directory was not removed.")
        return
    
    # Remove the directory
    print("Removing src directory...")
    try:
        shutil.rmtree(src_dir)
        print("✓ src directory removed successfully.")
    except Exception as e:
        print(f"Error removing src directory: {e}")
        return False
    
    return True

def move_html_files():
    """Move HTML files from root to output directory."""
    project_root = Path(__file__).parent.absolute()
    output_dir = project_root / "output"
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Get all HTML files in the root directory
    html_files = [f for f in os.listdir(project_root) if f.endswith('.html')]
    
    if not html_files:
        print("No HTML files found in the root directory.")
        return
    
    print(f"Found {len(html_files)} HTML files to move:")
    for html_file in html_files:
        print(f"  - {html_file}")
    
    # Ask for confirmation
    confirm = input("Move these files to the output directory? [y/N] ")
    if confirm.lower() != 'y':
        print("Aborted. No files were moved.")
        return
    
    # Move each file
    for html_file in html_files:
        src_path = project_root / html_file
        dst_path = output_dir / html_file
        
        print(f"Moving {html_file} to output directory...")
        try:
            shutil.move(src_path, dst_path)
        except Exception as e:
            print(f"Error moving {html_file}: {e}")
    
    print("✓ All HTML files moved successfully.")

def remove_obsolete_files():
    """Remove obsolete files that are no longer needed."""
    project_root = Path(__file__).parent.absolute()
    
    # List of obsolete files to remove
    obsolete_files = [
        "generate_graph.py",  # Old script that's been replaced
        "examples/search_example.py",  # Empty example file
        ".vscode/launch.json"  # Old VS Code configuration
    ]
    
    # Filter to only existing files
    existing_obsolete_files = [f for f in obsolete_files if (project_root / f).exists()]
    
    if not existing_obsolete_files:
        print("No obsolete files found to remove.")
        return
    
    print("Found the following obsolete files:")
    for file in existing_obsolete_files:
        print(f"  - {file}")
    
    # Ask for confirmation
    confirm = input("Remove these obsolete files? [y/N] ")
    if confirm.lower() != 'y':
        print("Aborted. No files were removed.")
        return
    
    # Remove each file
    for file in existing_obsolete_files:
        file_path = project_root / file
        print(f"Removing {file}...")
        try:
            if file_path.is_dir():
                shutil.rmtree(file_path)
            else:
                file_path.unlink()
            print(f"  ✓ {file} removed.")
        except Exception as e:
            print(f"  ✗ Error removing {file}: {e}")

def main():
    """Run the cleanup process."""
    print("IMDB Graph Project Cleanup")
    print("==========================")
    print("This script will clean up the project after migration to the new structure.")
    print("It will:")
    print("  1. Move any HTML files from the root directory to the output directory")
    print("  2. Remove obsolete files that are no longer needed")
    print("  3. Remove the old src directory")
    print()
    
    # Ask for confirmation
    confirm = input("Do you want to continue with the cleanup? [y/N] ")
    if confirm.lower() != 'y':
        print("Cleanup aborted.")
        return 1
    
    print("\n1. Moving HTML files...")
    move_html_files()
    
    print("\n2. Removing obsolete files...")
    remove_obsolete_files()
    
    print("\n3. Removing old src directory...")
    remove_old_src()
    
    print("\nCleanup completed!")
    print("\nThe project structure has been successfully reorganized.")
    print("You can now use the package with:")
    print("  python -m imdb_graph.main build")
    print("  python -m imdb_graph.main visualize")
    return 0

if __name__ == "__main__":
    sys.exit(main())
