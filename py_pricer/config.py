"""
Configuration settings for the py-pricer package.

This module contains configuration settings that can be adjusted
to customize the behavior of the package.
"""

import os
import logging
from pathlib import Path

# Logging configuration
LOG_LEVEL = logging.INFO
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

# File extensions
SUPPORTED_DATA_FORMATS = ['.json', '.parquet']

# Configuration files
CATEGORY_INDEX_FILE = "category-index.json"
CONTINUOUS_BANDING_FILE = "continuous-banding.json"

# Streamlit configuration
STREAMLIT_PAGE_TITLE = "Insurance Pricing Library"
STREAMLIT_PAGE_ICON = "📊"
STREAMLIT_LAYOUT = "wide"

# Data processing configuration
MAX_ROWS_DISPLAY = 1000  # Maximum number of rows to display in the UI
CATEGORICAL_THRESHOLD = 10  # Maximum number of unique values for a column to be considered categorical

# Default paths (these can be overridden by environment variables)
def get_default_paths():
    """Get default paths, allowing for environment variable overrides."""
    from py_pricer import get_project_root, get_algorithms_dir, get_data_dir, get_transformations_dir, get_rating_dir
    
    # Default paths
    paths = {
        'PROJECT_ROOT': get_project_root(),
        'ALGORITHMS_DIR': get_algorithms_dir(),
        'DATA_DIR': get_data_dir(),
        'TRANSFORMATIONS_DIR': get_transformations_dir(),
        'RATING_DIR': get_rating_dir(),
    }
    
    # Override with environment variables if set
    for key in paths:
        env_var = f"PY_PRICER_{key}"
        if env_var in os.environ:
            paths[key] = os.environ[env_var]
    
    return paths

# Load paths
PATHS = get_default_paths() 