"""
Utility functions for the py-pricer package.

This module contains utility functions that are used across the package.
"""

import os
import json
import polars as pl
from pathlib import Path
import logging
from typing import Optional, Dict, Any, List, Union

logger = logging.getLogger('py_pricer.utils')

def safe_load_json(file_path: str) -> Optional[Dict[str, Any]]:
    """
    Safely load a JSON file with error handling.
    
    Args:
        file_path: Path to the JSON file
        
    Returns:
        Loaded JSON data as a dictionary or None if loading failed
    """
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        logger.info(f"Successfully loaded JSON from {file_path}")
        return data
    except FileNotFoundError:
        logger.error(f"JSON file not found: {file_path}")
        return None
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON from {file_path}: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error loading JSON from {file_path}: {e}", exc_info=True)
        return None

def safe_load_parquet(file_path: str) -> Optional[pl.DataFrame]:
    """
    Safely load a Parquet file with error handling.
    
    Args:
        file_path: Path to the Parquet file
        
    Returns:
        Loaded Parquet data as a Polars DataFrame or None if loading failed
    """
    try:
        df = pl.read_parquet(file_path)
        logger.info(f"Successfully loaded Parquet from {file_path}")
        return df
    except FileNotFoundError:
        logger.error(f"Parquet file not found: {file_path}")
        return None
    except Exception as e:
        logger.error(f"Error loading Parquet from {file_path}: {e}", exc_info=True)
        return None

def find_files_by_extension(directory: str, extensions: List[str]) -> List[str]:
    """
    Find all files with specified extensions in a directory (recursively).
    
    Args:
        directory: Directory to search in
        extensions: List of file extensions to look for (e.g., ['.json', '.parquet'])
        
    Returns:
        List of file paths matching the extensions
    """
    try:
        files = []
        for path in Path(directory).rglob('*'):
            if path.is_file() and path.suffix.lower() in extensions:
                files.append(str(path))
        logger.info(f"Found {len(files)} files with extensions {extensions} in {directory}")
        return sorted(files)
    except Exception as e:
        logger.error(f"Error finding files in {directory}: {e}", exc_info=True)
        return []

def ensure_directory_exists(directory: str) -> bool:
    """
    Ensure a directory exists, creating it if necessary.
    
    Args:
        directory: Directory path to ensure exists
        
    Returns:
        True if the directory exists or was created, False otherwise
    """
    try:
        os.makedirs(directory, exist_ok=True)
        logger.info(f"Ensured directory exists: {directory}")
        return True
    except Exception as e:
        logger.error(f"Error ensuring directory exists {directory}: {e}", exc_info=True)
        return False

def load_config_json(file_path: str) -> Optional[Dict[str, Any]]:
    """
    Load a JSON configuration file with error handling.
    
    Args:
        file_path: Path to the JSON configuration file
        
    Returns:
        Loaded configuration as a dictionary or None if loading failed
    """
    try:
        with open(file_path, 'r') as f:
            config = json.load(f)
        logger.info(f"Successfully loaded configuration from {file_path}")
        return config
    except FileNotFoundError:
        logger.error(f"Configuration file not found: {file_path}")
        return None
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON configuration from {file_path}: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error loading configuration from {file_path}: {e}", exc_info=True)
        return None 