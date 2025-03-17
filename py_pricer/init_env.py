"""
Environment initialization script for the py_pricer package.

This module provides a command-line entry point for initializing the Python environment.
"""

import os
import sys
import subprocess
import argparse


def main():
    """
    Main entry point for the environment initialization.
    
    This function runs the prepare_local_env.sh script to set up the environment.
    """
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Initialize the py_pricer development environment")
    parser.add_argument(
        "--no-banner", 
        action="store_true", 
        help="Suppress the banner output"
    )
    args = parser.parse_args()
    
    # Get the script path (relative to the package root)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    package_root = os.path.dirname(current_dir)
    script_path = os.path.join(package_root, "prepare_local_env.sh")
    
    # Ensure the script is executable
    if not os.access(script_path, os.X_OK):
        try:
            os.chmod(script_path, 0o755)  # Make executable for user, read/execute for group/others
        except Exception as e:
            print(f"Warning: Could not make script executable: {e}")
    
    # Run the shell script
    try:
        subprocess.run([script_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: The initialization script failed with exit code {e.returncode}")
        sys.exit(e.returncode)
    except FileNotFoundError:
        print(f"Error: Could not find the initialization script at {script_path}")
        print("Make sure the prepare_local_env.sh script exists in the package root directory.")
        sys.exit(1)


if __name__ == "__main__":
    main() 