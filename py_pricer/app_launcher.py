"""
Streamlit application launcher for the insurance pricing library.

This module provides a command-line entry point for launching the Streamlit app.
"""

import os
import sys
import subprocess
import argparse
import streamlit.web.cli as stcli


def main():
    """
    Main entry point for the Streamlit app launcher.
    
    This function parses command-line arguments and launches the Streamlit app.
    """
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Launch the Insurance Pricing UI")
    parser.add_argument(
        "--port", 
        type=int, 
        default=8501, 
        help="Port to run the Streamlit app on (default: 8501)"
    )
    parser.add_argument(
        "--browser", 
        action="store_true", 
        help="Open the app in a browser window"
    )
    args = parser.parse_args()
    
    # Get the path to the Streamlit app.py file
    app_script = os.path.abspath(os.path.join(
        os.path.dirname(__file__), 
        '..', 
        'streamlit', 
        'app.py'
    ))
    
    # Check if the script exists
    if not os.path.exists(app_script):
        print(f"Error: Could not find the Streamlit app at {app_script}")
        sys.exit(1)
    
    # Add the project root to the Python path
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    
    # Print startup message
    print(f"Starting Insurance Pricing UI on port {args.port}...")
    print(f"You can access the app at http://localhost:{args.port}")
    
    # Set up Streamlit arguments
    sys.argv = ["streamlit", "run", app_script]
    
    # Add port argument
    sys.argv.extend(["--server.port", str(args.port)])
    
    # Add headless option if browser is not requested
    if not args.browser:
        sys.argv.extend(["--server.headless", "true"])
    
    try:
        # Run the Streamlit app using Streamlit's CLI
        stcli.main()
    except KeyboardInterrupt:
        print("\nShutting down Insurance Pricing UI...")
    except Exception as e:
        print(f"Error launching the app: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main() 