#!/usr/bin/env python3
"""
Install the IMDB Graph package in development mode.
"""

import subprocess
import sys
import os
from pathlib import Path

def main():
    """Install the package in development mode."""
    # Get the project root directory
    project_root = Path(__file__).parent.absolute()
    
    # Print info
    print(f"Installing IMDB Graph package from {project_root}")
    
    # Install requirements
    print("Installing requirements...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                   cwd=project_root, check=True)
    
    # Install package in development mode
    print("Installing package in development mode...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-e", "."], 
                   cwd=project_root, check=True)
    
    print("\nInstallation complete!")
    print("\nYou can now use the package with:")
    print("  python -m imdb_graph.main build")
    print("  python -m imdb_graph.main visualize")
    print("\nOr using the console scripts:")
    print("  imdb-graph-build")
    print("  imdb-graph-visualize")

if __name__ == "__main__":
    main()
