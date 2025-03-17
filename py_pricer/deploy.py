"""
Deployment script for the py_pricer package.

This module provides a command-line entry point for deploying the API to Azure.
"""

import os
import sys
import subprocess
import argparse


def main():
    """
    Main entry point for the deployment script.
    
    This function runs the deploy.sh script to deploy the API to Azure.
    """
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Deploy the py_pricer API to Azure")
    parser.add_argument(
        "--no-prompt", 
        action="store_true", 
        help="Skip confirmation prompts"
    )
    args = parser.parse_args()
    
    # Get the script path (relative to the package root)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    package_root = os.path.dirname(current_dir)
    script_path = os.path.join(package_root, "api", "deploy.sh")
    
    # Ensure the script is executable
    if not os.access(script_path, os.X_OK):
        try:
            os.chmod(script_path, 0o755)  # Make executable for user, read/execute for group/others
            print(f"Made deployment script executable: {script_path}")
        except Exception as e:
            print(f"Warning: Could not make script executable: {e}")
            print(f"You may need to run: chmod +x {script_path}")
    
    # Run the shell script
    try:
        print("Starting deployment process to Azure...")
        subprocess.run([script_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: The deployment script failed with exit code {e.returncode}")
        sys.exit(e.returncode)
    except FileNotFoundError:
        print(f"Error: Could not find the deployment script at {script_path}")
        print("Make sure the deploy.sh script exists in the api directory.")
        sys.exit(1)


if __name__ == "__main__":
    main() 