#!/usr/bin/env python
"""
Launcher module for the py-pricer Streamlit app.

This module provides a function to launch the Streamlit app properly
when called via the console script entry point.
"""

import os
import sys
import logging

# Create a module-specific logger
logger = logging.getLogger('py_pricer.app_launcher')

def launch_app():
    """
    Launch the Streamlit app properly.
    
    This function is called by the console script entry point.
    It ensures that Streamlit is launched correctly with the proper arguments.
    """
    # Find the app.py file in the installed package
    import py_pricer
    app_path = os.path.join(os.path.dirname(py_pricer.__file__), 'app.py')
    
    if not os.path.exists(app_path):
        print(f"Error: Could not find app.py at {app_path}")
        print("Please ensure the py-pricer package is properly installed.")
        sys.exit(1)
    
    # Log information about how we're running
    print(f"Running Streamlit app from: {app_path}")
    print(f"Working directory: {os.getcwd()}")
    
    # Check if the algorithms directory exists in the current working directory
    algorithms_dir = os.path.join(os.getcwd(), "algorithms")
    if not os.path.exists(algorithms_dir):
        print(f"Warning: The algorithms directory was not found at: {algorithms_dir}")
        print("You may need to initialize it first with:")
        print("  import py_pricer")
        print("  py_pricer.initialize()")
    
    # Use os.execvp to replace the current process with streamlit
    # This avoids any recursive launching issues completely
    streamlit_cmd = "streamlit"
    args = [streamlit_cmd, "run", app_path, "--browser.serverAddress=localhost", "--server.headless=false"]
    
    print(f"Executing: {' '.join(args)}")
    
    # Replace the current process with streamlit
    # This is the key to avoiding recursive launching
    os.execvp(streamlit_cmd, args)
    
    # We will never reach this point if execvp succeeds
    print("Error: Failed to launch Streamlit")
    sys.exit(1)

if __name__ == "__main__":
    # This allows the module to be run directly for testing
    launch_app() 