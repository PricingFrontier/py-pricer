#!/usr/bin/env python
"""
Launcher module for the py-pricer FastAPI server.

This module provides a function to launch the FastAPI server properly
when called via the console script entry point.
"""

import os
import sys
import shutil
import logging
import importlib.util
from pathlib import Path

# Create a module-specific logger
logger = logging.getLogger('py_pricer.api_launcher')

def launch_api():
    """
    Launch the FastAPI server properly.
    
    This function is called by the console script entry point.
    It ensures that the API server is launched correctly with the proper arguments.
    """
    # First, check if we need to initialize the template files
    import py_pricer
    templates_dir = os.path.join(os.path.dirname(py_pricer.__file__), 'templates', 'api')
    cwd = os.getcwd()
    
    # Log information about how we're running
    print(f"API Launcher - Working directory: {cwd}")
    
    # Check if the run_api.py template exists in the current working directory
    run_api_path = os.path.join(cwd, "run_api.py")
    if not os.path.exists(run_api_path):
        # Copy the template if it exists
        template_path = os.path.join(templates_dir, "run_api.py")
        if os.path.exists(template_path):
            print(f"Copying API script template to: {run_api_path}")
            shutil.copy2(template_path, run_api_path)
            os.chmod(run_api_path, 0o755)  # Make executable
        else:
            print(f"Warning: Could not find API template at: {template_path}")
            print("You may need to install the package properly or run the initializer.")
            sys.exit(1)
    
    # Check if the algorithms directory exists in the current working directory
    algorithms_dir = os.path.join(cwd, "algorithms")
    if not os.path.exists(algorithms_dir):
        print(f"Warning: The algorithms directory was not found at: {algorithms_dir}")
        print("You may need to initialize it first with:")
        print("  import py_pricer")
        print("  py_pricer.initialize()")
    
    # Pass command line arguments to the run_api.py script
    # Extract all arguments after the script name
    args = sys.argv[1:]
    
    print(f"Launching API server using: {run_api_path}")
    print(f"With arguments: {' '.join(args) if args else '(none)'}")
    
    # Load the run_api.py module and call its main function
    try:
        spec = importlib.util.spec_from_file_location("run_api", run_api_path)
        run_api_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(run_api_module)
        
        # Call the main function if it exists
        if hasattr(run_api_module, "main"):
            sys.argv = [run_api_path] + args  # Replace sys.argv with our args
            run_api_module.main()
        else:
            print(f"Error: The run_api.py script does not have a main() function")
            sys.exit(1)
    except Exception as e:
        print(f"Error loading or running the API script: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # This allows the module to be run directly for testing
    launch_api() 