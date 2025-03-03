#!/usr/bin/env python
"""
Launcher module for the py-pricer initializer.

This module provides a function to launch the initializer properly
when called via the console script entry point.
"""

import os
import sys
import logging
import argparse

# Create a module-specific logger
logger = logging.getLogger('py_pricer.initializer_launcher')

def launch_initializer():
    """
    Launch the py-pricer initializer.
    
    This function is called by the console script entry point.
    It ensures that the initializer is run with proper arguments.
    """
    # Import initializer here to avoid circular imports
    from py_pricer.initializer import initialize, setup_logging
    
    # Set up logging
    setup_logging()
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Initialize the py-pricer directory structure and example files.')
    parser.add_argument('--force', action='store_true', help='Force overwrite of existing files')
    args = parser.parse_args()
    
    # Log information
    print(f"Running py-pricer initializer")
    print(f"Working directory: {os.getcwd()}")
    
    try:
        # Run the initializer
        success = initialize(args.force)
        
        if success:
            print("\nInitialization completed successfully!")
            print(f"- 'algorithms' directory created/updated in: {os.getcwd()}")
            print("- API template scripts created in your working directory")
            print("\nNext steps:")
            print("1. Run the Streamlit app: py-pricer-app")
            print("2. Run the API server: py-pricer-api")
        else:
            print("\nInitialization skipped. The algorithms directory already exists.")
            print("Use --force to overwrite existing files: py-pricer-init --force")
        
        # Exit with appropriate status
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    # This allows the module to be run directly for testing
    launch_initializer() 