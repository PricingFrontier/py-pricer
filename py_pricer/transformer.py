"""
Transformer module for the insurance pricing library.

This module handles data transformations by loading and applying
user-defined transformation scripts from the algorithms/transformations directory.
"""

import os
import importlib.util
import sys
import polars as pl
from typing import Optional, List, Dict, Union


def load_transformation_module(transform_file="transform.py"):
    """
    Load the transformation module from the algorithms/transformations directory.
    
    Args:
        transform_file: Name of the transformation file to load
    
    Returns:
        Loaded module or None if not found
    """
    transform_path = os.path.join("algorithms", "transformations", transform_file)
    
    if not os.path.exists(transform_path):
        print(f"Transformation file not found: {transform_path}")
        return None
    
    try:
        # Load the module from file path
        spec = importlib.util.spec_from_file_location("transformations.transform", transform_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules["transformations.transform"] = module
        spec.loader.exec_module(module)
        return module
    except Exception as e:
        print(f"Error loading transformation module: {e}")
        return None


def load_factor_config():
    """
    Load the factor configuration from the algorithms/transformations/factor-config.py file.
    
    Returns:
        Dictionary of factor mappings or empty dict if not found
    """
    config_path = os.path.join("..", "algorithms", "transformations", "factor-config.py")
    print(f"Looking for factor config at: {os.path.abspath(config_path)}")
    
    if not os.path.exists(config_path):
        print(f"Factor config file not found at: {os.path.abspath(config_path)}")
        return {}
    
    try:
        # Load the module from file path
        spec = importlib.util.spec_from_file_location("transformations.factor_config", config_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules["transformations.factor_config"] = module
        spec.loader.exec_module(module)
        
        # Check if the module has the category_indexing function
        if hasattr(module, "category_indexing"):
            mappings = module.category_indexing()
            print(f"Successfully loaded factor mappings for columns: {list(mappings.keys())}")
            return mappings
        else:
            print("Factor config module does not have a category_indexing function.")
            return {}
    except Exception as e:
        print(f"Error loading factor config module: {e}")
        return {}


def apply_transformations(df: pl.DataFrame) -> Optional[pl.DataFrame]:
    """
    Apply transformations to the input data using the user-defined transformation script.
    
    Args:
        df: Raw input data as a Polars DataFrame
    
    Returns:
        Transformed data as a Polars DataFrame or None if transformation failed
    """
    # Load the transformation module
    transform_module = load_transformation_module()
    
    if transform_module is None:
        print("No transformation module found. Returning original data.")
        return df
    
    # Check if the module has a transform_data function
    if not hasattr(transform_module, "transform_data"):
        print("Transformation module does not have a transform_data function. Returning original data.")
        return df
    
    try:
        # Apply the transformation
        transformed_df = transform_module.transform_data(df)
        return transformed_df
    except Exception as e:
        print(f"Error applying transformations: {e}")
        return None


def get_categorical_columns(df: pl.DataFrame) -> List[str]:
    """
    Identify potential categorical columns in a DataFrame.
    
    A column is considered categorical if:
    - It has string data type
    - It's an integer column with less than 10 unique values
    
    Args:
        df: Input DataFrame
    
    Returns:
        List of column names that are likely categorical
    """
    categorical_columns = []
    
    for col in df.columns:
        dtype = df[col].dtype
        
        # Check if column is string type
        if dtype == pl.Utf8 or dtype == pl.String:
            categorical_columns.append(col)
        # Check if column is integer with few unique values
        elif dtype in [pl.Int8, pl.Int16, pl.Int32, pl.Int64, pl.UInt8, pl.UInt16, pl.UInt32, pl.UInt64]:
            n_unique = df[col].unique().len()
            if n_unique < 10 and n_unique > 1:  # More than 1 to exclude constant columns
                categorical_columns.append(col)
    
    return categorical_columns


def apply_category_indexing(df: pl.DataFrame, columns: Optional[List[str]] = None) -> tuple[pl.DataFrame, Dict[str, Dict[Union[str, int], int]]]:
    """
    Apply category indexing transformation to convert categorical columns to numeric indices.
    Uses only predefined mappings from factor-config.py.
    
    Args:
        df: Input DataFrame
        columns: Optional list of columns to convert. If None, uses all columns from factor config.
    
    Returns:
        Tuple of (transformed DataFrame, category mappings dict)
        The mappings dict is structured as {column_name: {original_value: index_value}}
    """
    # Load predefined factor configurations
    factor_config = load_factor_config()
    
    if not factor_config:
        print("No factor configurations found. Skipping category indexing.")
        return df, {}
    
    if not columns:
        # If no columns specified, use all columns from factor_config
        columns = list(factor_config.keys())
    
    result_df = df.clone()
    category_mappings = {}
    
    for col in columns:
        if col in df.columns and col in factor_config:
            value_to_index = factor_config[col]
            category_mappings[col] = value_to_index
            
            # Create list of original values and replacement values for the replace method
            original_values = list(value_to_index.keys())
            replacement_values = list(value_to_index.values())
            
            # Replace values with indices using replace
            result_df = result_df.with_columns(
                pl.col(col).replace(original_values, replacement_values).alias(f"{col}_indexed")
            )
    
    return result_df, category_mappings 