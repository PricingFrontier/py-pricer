"""
Data processing module for the insurance pricing library.

This module provides functions to load and process insurance quote data
from various file formats (JSON, Parquet).
"""

import os
import json
import polars as pl
from pathlib import Path
from typing import Union, List, Dict, Any, Optional


def load_json(file_path: str) -> pl.DataFrame:
    """
    Load data from a JSON file.
    
    Args:
        file_path: Path to the JSON file
        
    Returns:
        DataFrame containing the data
    """
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    # Handle both single quote and list of quotes
    if isinstance(data, dict):
        return pl.DataFrame([data])
    else:
        return pl.DataFrame(data)


def load_parquet(file_path: str) -> pl.DataFrame:
    """
    Load data from a Parquet file.
    
    Args:
        file_path: Path to the Parquet file
        
    Returns:
        DataFrame containing the data
    """
    return pl.read_parquet(file_path)


def load_data(file_path: str) -> Optional[pl.DataFrame]:
    """
    Load data from a file based on its extension.
    
    Args:
        file_path: Path to the data file
        
    Returns:
        DataFrame containing the data or None if the format is not supported
    """
    file_extension = os.path.splitext(file_path)[1].lower()
    
    if file_extension == '.json':
        return load_json(file_path)
    elif file_extension == '.parquet':
        return load_parquet(file_path)
    else:
        print(f"Unsupported file format: {file_extension}")
        return None


def find_data_files(directory: str, formats: List[str] = None) -> List[str]:
    """
    Find all data files in a directory with specified formats.
    
    Args:
        directory: Directory to search in
        formats: List of file extensions to include (default: ['.json', '.parquet'])
        
    Returns:
        List of file paths
    """
    if formats is None:
        formats = ['.json', '.parquet']
    
    files = []
    for path in Path(directory).rglob('*'):
        if path.is_file() and path.suffix.lower() in formats:
            files.append(str(path))
    
    return sorted(files) 