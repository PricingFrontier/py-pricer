#!/usr/bin/env python3
"""
Launcher script for the Streamlit application.

This script runs the Streamlit app for the insurance pricing library.
"""

import os
import subprocess
import sys

def run_streamlit_app():
    """Run the Streamlit app."""
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Path to the Streamlit app
    app_path = os.path.join(script_dir, "streamlit", "app.py")
    
    # Check if the app file exists
    if not os.path.exists(app_path):
        print(f"Error: Streamlit app not found at {app_path}")
        sys.exit(1)
    
    # Run the Streamlit app with headless option to prevent browser opening
    print(f"Starting Streamlit app from {app_path}")
    subprocess.run(["streamlit", "run", app_path, "--server.headless", "true"])

if __name__ == "__main__":
    run_streamlit_app() 