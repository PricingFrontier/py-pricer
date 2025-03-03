#!/usr/bin/env python
"""
Initializer module for py_pricer.

This script creates the algorithms directory structure by downloading example files
from the GitHub repository.

Usage:
    python -m py_pricer.initializer [--force]

Options:
    --force     Overwrite existing files (use with caution)
"""

import os
import sys
import shutil
import logging
import argparse
import tempfile
import zipfile
from pathlib import Path
import urllib.request

# Initialize logger
logger = logging.getLogger('py_pricer.initializer')

# GitHub repository information
GITHUB_REPO_URL = "https://github.com/PricingFrontier/py-pricer"
GITHUB_BRANCH = "main"
GITHUB_ARCHIVE_URL = f"{GITHUB_REPO_URL}/archive/refs/heads/{GITHUB_BRANCH}.zip"
ALGORITHMS_DIR_NAME = "algorithms"

def download_algorithms_from_github(force=False):
    """
    Download the algorithms directory from the GitHub repository.
    
    Args:
        force: Whether to force overwrite existing files
        
    Returns:
        Path to the downloaded algorithms directory
        
    Raises:
        Exception: If the download or extraction fails
    """
    logger.info(f"Downloading files from GitHub: {GITHUB_ARCHIVE_URL}")
    
    # Create a temporary directory for the download
    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            # Download the repository ZIP archive
            zip_path = os.path.join(temp_dir, "repo.zip")
            urllib.request.urlretrieve(GITHUB_ARCHIVE_URL, zip_path)
            
            logger.info(f"Repository archive downloaded to: {zip_path}")
            
            # Extract the ZIP archive
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
            
            # Find the extracted directory name
            repo_name = f"py-pricer-{GITHUB_BRANCH}"
            repo_dir = os.path.join(temp_dir, repo_name)
            
            if not os.path.exists(repo_dir):
                raise FileNotFoundError(f"Repository directory not found: {repo_dir}")
            
            # Find the algorithms directory
            algorithms_dir = os.path.join(repo_dir, ALGORITHMS_DIR_NAME)
            
            if not os.path.exists(algorithms_dir):
                raise FileNotFoundError(f"Algorithms directory not found: {algorithms_dir}")
            
            # Get the current working directory
            cwd = os.getcwd()
            
            # Create the target algorithms directory
            target_dir = os.path.join(cwd, ALGORITHMS_DIR_NAME)
            
            # Check if the target directory already exists
            if os.path.exists(target_dir):
                if force:
                    logger.info(f"Removing existing algorithms directory: {target_dir}")
                    shutil.rmtree(target_dir)
                else:
                    logger.warning(f"Algorithms directory already exists: {target_dir}")
                    logger.warning("Use --force to overwrite existing files")
                    return None
            
            # Copy the algorithms directory to the target location
            shutil.copytree(algorithms_dir, target_dir)
            
            logger.info(f"Successfully downloaded algorithms directory to: {target_dir}")
            return target_dir
            
        except urllib.error.URLError as e:
            error_msg = f"Network error when downloading from GitHub: {e}"
            logger.error(error_msg)
            raise RuntimeError(error_msg)
        
        except zipfile.BadZipFile:
            error_msg = "Downloaded file is not a valid ZIP archive"
            logger.error(error_msg)
            raise RuntimeError(error_msg)
            
        except FileNotFoundError as e:
            error_msg = f"File not found: {e}"
            logger.error(error_msg)
            raise
            
        except Exception as e:
            error_msg = f"Error downloading algorithms from GitHub: {e}"
            logger.error(error_msg)
            raise RuntimeError(error_msg)

def initialize(force=False):
    """
    Initialize the directory structure and example files by downloading from GitHub.
    
    Args:
        force: Whether to force overwrite existing files
        
    Returns:
        True if initialization was successful
        
    Raises:
        RuntimeError: If the download or extraction fails
    """
    try:
        algorithms_dir = download_algorithms_from_github(force)
        if algorithms_dir:
            logger.info(f"Initialization complete. Example files have been downloaded from GitHub to: {algorithms_dir}")
            return True
        
        # If we get here without returning True, it means the algorithms directory already exists
        # and force=False
        logger.warning("The algorithms directory already exists. Use --force to overwrite existing files.")
        return False
            
    except Exception as e:
        error_msg = f"Initialization failed: {e}"
        logger.error(error_msg)
        raise RuntimeError(error_msg)

def setup_logging():
    """Set up logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

def main():
    """Main entry point for the initializer."""
    # Set up logging
    setup_logging()
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Initialize the py-pricer directory structure and example files.')
    parser.add_argument('--force', action='store_true', help='Force overwrite of existing files')
    args = parser.parse_args()
    
    try:
        # Initialize the directory structure and example files
        success = initialize(args.force)
        
        # Exit with appropriate status
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
