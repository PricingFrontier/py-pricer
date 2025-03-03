"""
py_pricer - A Python library for insurance pricing

This package provides tools for processing insurance quotes, 
applying transformations, and calculating prices.
"""

import os
import sys
import logging
from pathlib import Path

# Create a basic logger for initial setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Create a logger for the package
logger = logging.getLogger('py_pricer')

# Utility functions for path resolution
def get_project_root():
    """Get the absolute path to the project root directory."""
    # Get the directory of the py_pricer package
    package_dir = os.path.dirname(os.path.abspath(__file__))
    # The project root is one level up from the package directory
    return os.path.dirname(package_dir)

def get_algorithms_dir():
    """Get the absolute path to the algorithms directory."""
    return os.path.join(get_project_root(), "algorithms")

def get_data_dir():
    """Get the absolute path to the data directory."""
    return os.path.join(get_algorithms_dir(), "data")

def get_transformations_dir():
    """Get the absolute path to the transformations directory."""
    return os.path.join(get_algorithms_dir(), "transformations")

def get_rating_dir():
    """Get the absolute path to the rating directory."""
    return os.path.join(get_algorithms_dir(), "rating")

# Version information
__version__ = "0.1.0"

# Import submodules to make them available when importing the package
from py_pricer import transformer
from py_pricer import utils
from py_pricer import config
from py_pricer import initializer

# Set up advanced logging configuration
try:
    from py_pricer.logging_config import init_logging
    init_logging()
except ImportError:
    logger.warning("Advanced logging configuration not available. Using basic configuration.")

# Convenience function to initialize the project
def initialize(force=False):
    """
    Initialize the py_pricer directory structure and example files by downloading from GitHub.
    
    Args:
        force: Whether to force overwrite existing files
        
    Returns:
        True if initialization was successful
        
    Raises:
        RuntimeError: If initialization fails (e.g., download error)
    """
    from py_pricer.initializer import initialize as init_func
    return init_func(force)

# Define what's available when using "from py_pricer import *"
__all__ = [
    'transformer',
    'utils',
    'config',
    'initializer',
    'get_project_root',
    'get_algorithms_dir',
    'get_data_dir',
    'get_transformations_dir',
    'get_rating_dir',
    'logger',
    '__version__',
    'initialize',
]
