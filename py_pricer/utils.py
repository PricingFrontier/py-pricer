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
    Load a configuration JSON file.
    
    This is a specialized version of safe_load_json specifically for config files.
    It provides more detailed logging and handling for configuration.
    
    Args:
        file_path: Path to the JSON configuration file
        
    Returns:
        Loaded configuration as a dictionary or None if loading failed
    """
    result = safe_load_json(file_path)
    if result is None:
        logger.warning(f"Failed to load configuration from {file_path}")
    else:
        logger.info(f"Loaded configuration with {len(result)} items from {file_path}")
    return result

def load_csv_table(file_path: str, base_dir: Optional[str] = None) -> Optional[pl.DataFrame]:
    """
    Load a CSV file from the specified path.
    
    Args:
        file_path: Path to the CSV file or relative filename
        base_dir: Base directory to use if file_path is not absolute. Default is None (use file_path as is).
    
    Returns:
        A DataFrame containing the CSV data or None if loading fails
    """
    try:
        # Determine the complete path
        complete_path = file_path
        if not os.path.isabs(file_path) and base_dir is not None:
            complete_path = os.path.join(base_dir, file_path)
        
        # Check if the file exists
        if not os.path.exists(complete_path):
            logger.error(f"CSV file not found at: {complete_path}")
            return None
        
        # Load the CSV file
        df = pl.read_csv(complete_path)
        logger.info(f"Successfully loaded CSV from {complete_path}")
        logger.info(f"Data loaded: {df.height} rows, {df.width} columns")
        
        return df
    except Exception as e:
        logger.error(f"Error loading CSV {file_path}: {e}")
        return None 