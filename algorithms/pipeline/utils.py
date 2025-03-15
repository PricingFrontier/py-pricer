"""
Utility functions for the py-pricer package.

This module contains utility functions that are used across the package,
including data loading and processing functions.
"""

import os
import json
import polars as pl
from pathlib import Path
from typing import Optional, Dict, Any, List, Union, Tuple

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
    
    # Map file extensions to loader functions
    loaders = {
        '.json': load_json,
        '.parquet': load_parquet
    }
    
    # Get the appropriate loader function
    loader = loaders.get(file_extension)
    
    if loader:
        return loader(file_path)
    else:
        print(f"Unsupported file format: {file_extension}")
        return None

def load_config_json(file_path: str) -> Optional[Dict[str, Any]]:
    """
    Load a configuration JSON file.
    
    Args:
        file_path: Path to the JSON configuration file
        
    Returns:
        Loaded configuration as a dictionary or None if loading failed
    """
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        return data
    except Exception:
        return None

def load_transformation_configs(config_dir: Optional[str] = None) -> Tuple[Dict[str, Dict[str, int]], Dict[str, Dict[str, Any]]]:
    """
    Load category index and continuous banding configuration files.
    
    Args:
        config_dir: Directory containing configuration files (default: algorithms/pipeline)
        
    Returns:
        Tuple of (category_config, banding_config)
    """
    if config_dir is None:
        # Get the directory of the pipeline module
        base_dir = os.path.dirname(os.path.abspath(__file__))
        config_dir = base_dir
    
    # Load configuration files
    category_index_path = os.path.join(config_dir, "category-index.json")
    continuous_banding_path = os.path.join(config_dir, "continuous-banding.json")
    
    category_config = load_config_json(category_index_path) or {}
    banding_config = load_config_json(continuous_banding_path) or {}
    
    return category_config, banding_config

def apply_category_mapping(df: pl.DataFrame, category_config: Dict[str, Dict[str, int]]) -> pl.DataFrame:
    """
    Apply category mapping to convert categorical values to their numeric indices.
    
    Args:
        df: Input DataFrame
        category_config: Dictionary mapping column names to their category-index mappings
        
    Returns:
        DataFrame with mapped categorical columns
    """
    df = df.clone()
    
    for column, mapping in category_config.items():
        # Skip columns not in the dataframe
        if column not in df.columns:
            continue
            
        # Create a new column with the mapped values
        mapped_column = f"{column}_Index"
        
        # Use replace_strict which is the recommended way to map values in Polars
        df = df.with_columns(
            pl.col(column).replace_strict(mapping, default=None).alias(mapped_column)
        )
    
    return df

def apply_continuous_banding(df: pl.DataFrame, banding_config: Dict[str, Dict[str, Any]]) -> pl.DataFrame:
    """
    Apply banding to continuous variables based on configuration.
    
    Args:
        df: Input DataFrame
        banding_config: Dictionary with banding configuration for continuous variables
        
    Returns:
        DataFrame with added band columns
    """
    df = df.clone()
    
    for column, config in banding_config.items():
        # Skip columns not in the dataframe
        if column not in df.columns:
            continue
        
        bands = config.get("bands", [])
        # Skip if no bands defined
        if not bands:
            continue
            
        output_column = config.get("column_name", f"{column}Band")
        min_inclusive = config.get("min_inclusive", True)
        max_exclusive = config.get("max_exclusive", True)
        
        # Create expressions for each band
        when_then_exprs = []
        
        for band in bands:
            min_val = band.get("min")
            max_val = band.get("max")
            label = band.get("label")
            
            # Build condition based on inclusivity settings
            if min_inclusive and max_exclusive:
                condition = (pl.col(column) >= min_val) & (pl.col(column) < max_val)
            elif min_inclusive and not max_exclusive:
                condition = (pl.col(column) >= min_val) & (pl.col(column) <= max_val)
            elif not min_inclusive and max_exclusive:
                condition = (pl.col(column) > min_val) & (pl.col(column) < max_val)
            else:  # not min_inclusive and not max_exclusive
                condition = (pl.col(column) > min_val) & (pl.col(column) <= max_val)
            
            # Use pl.lit() to ensure the label is treated as a literal value, not a column reference
            when_then_exprs.append((condition, pl.lit(label)))
        
        # Skip if no expressions were created
        if not when_then_exprs:
            continue
            
        # Start with the first condition
        expr = pl.when(when_then_exprs[0][0]).then(when_then_exprs[0][1])
        
        # Add all remaining conditions except the last one
        for condition, label in when_then_exprs[1:-1]:
            expr = expr.when(condition).then(label)
        
        # Add the otherwise clause
        if len(when_then_exprs) > 1:
            expr = expr.otherwise(when_then_exprs[-1][1])
        else:
            expr = expr.otherwise(pl.lit(None))
        
        # Apply the expression to create the new column
        df = df.with_columns(expr.alias(output_column))
    
    return df

def find_data_files(directory: str, formats: List[str] = None) -> List[str]:
    """
    Find all data files in a directory with specified formats.
    
    Args:
        directory: Directory to search in
        formats: List of file extensions to include (default: ['.json', '.parquet', '.csv'])
        
    Returns:
        List of file paths
    """
    if formats is None:
        # Use the same formats as supported by our loaders
        formats = ['.json', '.parquet', '.csv']
    
    return find_files_by_extension(directory, formats)

def find_files_by_extension(directory: str, extensions: List[str]) -> List[str]:
    """
    Find all files with specified extensions in a directory (recursively).
    
    Args:
        directory: Directory to search in
        extensions: List of file extensions to look for (e.g., ['.json', '.parquet'])
        
    Returns:
        List of file paths matching the extensions
    """
    files = []
    for path in Path(directory).rglob('*'):
        if path.is_file() and path.suffix.lower() in extensions:
            files.append(str(path))
    return sorted(files)

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
        return True
    except Exception:
        return False

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
        
        # Early return if file doesn't exist
        if not os.path.exists(complete_path):
            return None
        
        # Load the CSV file
        return pl.read_csv(complete_path)
    except Exception:
        return None

def get_data_directory(data_type: str) -> str:
    """
    Get the path to a data directory.
    
    Args:
        data_type: Type of data directory ('batch', 'individual', etc.)
        
    Returns:
        Absolute path to the data directory
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    return os.path.join(base_dir, "algorithms", "data", data_type)

def load_directory_data(data_type: str, file_extension: str, combine: bool = False) -> Optional[pl.DataFrame]:
    """
    Load data from files in a specific data directory.
    
    Args:
        data_type: Type of data directory ('batch', 'individual', etc.)
        file_extension: File extension to look for ('.json', '.parquet', etc.)
        combine: Whether to combine multiple files (True) or just load the first one (False)
        
    Returns:
        DataFrame containing the data or None if loading fails
    """
    try:
        # Get the data directory
        data_dir = get_data_directory(data_type)
        
        # Find files with the specified extension
        files = find_files_by_extension(data_dir, [file_extension])
        
        # Early return if no files found
        if not files:
            print(f"No {file_extension} files found in the {data_type} directory")
            return None
        
        # Map file extensions to loader functions
        loaders = {
            '.json': load_json,
            '.parquet': load_parquet,
            '.csv': pl.read_csv
        }
        
        # Get the appropriate loader function
        loader = loaders.get(file_extension.lower())
        if not loader:
            print(f"Unsupported file format: {file_extension}")
            return None
        
        if combine:
            # Load and combine all files
            dfs = []
            for file_path in files:
                df = loader(file_path)
                if df is not None:
                    dfs.append(df)
            
            # Early return if no dataframes were loaded
            if not dfs:
                return None
            
            # Combine all dataframes
            return pl.concat(dfs)
        else:
            # Load just the first file
            return loader(files[0])
            
    except Exception as e:
        print(f"Error loading {data_type} data: {e}")
        return None

def load_batch_data() -> Optional[pl.DataFrame]:
    """
    Load batch data from the parquet file in the algorithms/data/batch directory.
    
    Returns:
        DataFrame containing the batch data or None if loading fails
    """
    return load_directory_data('batch', '.parquet', combine=False)

def load_individual_data() -> Optional[pl.DataFrame]:
    """
    Load individual data from JSON files in the algorithms/data/individual directory.
    
    Returns:
        DataFrame containing the combined individual data or None if loading fails
    """
    return load_directory_data('individual', '.json', combine=True) 