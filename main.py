"""
Main entry point for the Python Terminal CLI.
"""
import sys
import os

# Add the current directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from interfaces.cli import main

if __name__ == "__main__":
    main()