"""
Transformer module for the insurance pricing library.

This module handles data transformations by loading and applying
user-defined transformation scripts from the algorithms/transformations directory.
"""

import os
import importlib.util
import sys
import polars as pl
import logging
from typing import Optional, List, Dict, Union, Tuple
import json

# For Python 3.8 compatibility
try:
    from typing import TypedDict, Protocol
except ImportError:
    from typing_extensions import TypedDict, Protocol

from py_pricer import get_transformations_dir, logger
from py_pricer.config import CATEGORICAL_THRESHOLD, CATEGORY_INDEX_FILE
from py_pricer.utils import load_config_json

# Create a module-specific logger
logger = logging.getLogger('py_pricer.transformer')


def load_transformation_module(transform_file="transform.py"):
    """
    Load the transformation module from the algorithms/transformations directory.
    
    Args:
        transform_file: Name of the transformation file to load
    
    Returns:
        Loaded module or None if not found
    """
    transformations_dir = get_transformations_dir()
    transform_path = os.path.join(transformations_dir, transform_file)
    
    if not os.path.exists(transform_path):
        logger.warning(f"Transformation file not found: {transform_path}")
        return None
    
    try:
        # Load the module from file path
        spec = importlib.util.spec_from_file_location("transformations.transform", transform_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules["transformations.transform"] = module
        spec.loader.exec_module(module)
        logger.info(f"Successfully loaded transformation module from {transform_path}")
        return module
    except Exception as e:
        logger.error(f"Error loading transformation module: {e}", exc_info=True)
        return None


def load_factor_config():
    """
    Load the factor configuration from the algorithms/transformations/category-index.json file.
    
    Returns:
        Dictionary of factor mappings or empty dict if not found
    """
    transformations_dir = get_transformations_dir()
    config_path = os.path.join(transformations_dir, CATEGORY_INDEX_FILE)
    logger.info(f"Looking for category index at: {config_path}")
    
    mappings = load_config_json(config_path)
    
    if mappings:
        logger.info(f"Successfully loaded category mappings for columns: {list(mappings.keys())}")
        return mappings
    else:
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
        logger.info("No transformation module found. Returning original data.")
        return df
    
    # Check if the module has a transform_data function
    if not hasattr(transform_module, "transform_data"):
        logger.warning("Transformation module does not have a transform_data function. Returning original data.")
        return df
    
    try:
        # Apply the transformation
        transformed_df = transform_module.transform_data(df)
        logger.info("Successfully applied transformations")
        return transformed_df
    except Exception as e:
        logger.error(f"Error applying transformations: {e}", exc_info=True)
        return None


def get_categorical_columns(df: pl.DataFrame) -> List[str]:
    """
    Identify potential categorical columns in a DataFrame.
    
    A column is considered categorical if:
    - It has string data type
    - It's an integer column with less than CATEGORICAL_THRESHOLD unique values
    
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
            if n_unique < CATEGORICAL_THRESHOLD and n_unique > 1:  # More than 1 to exclude constant columns
                categorical_columns.append(col)
    
    return categorical_columns


def apply_category_indexing(df: pl.DataFrame, columns: Optional[List[str]] = None) -> Tuple[pl.DataFrame, Dict[str, Dict[Union[str, int], int]]]:
    """
    Apply category indexing transformation to convert categorical columns to numeric indices.
    Uses predefined mappings from category-index.json.
    
    Args:
        df: Input DataFrame
        columns: Optional list of columns to convert. If None, uses all columns from category index.
    
    Returns:
        Tuple of (transformed DataFrame, category mappings dict)
        The mappings dict is structured as {column_name: {original_value: index_value}}
    """
    # Load predefined category index
    category_index = load_factor_config()
    
    if not category_index:
        logger.info("No category index found. Skipping category indexing.")
        return df, {}
    
    if not columns:
        # If no columns specified, use all columns from category_index
        columns = list(category_index.keys())
    
    result_df = df.clone()
    category_mappings = {}
    
    for col in columns:
        if col in df.columns and col in category_index:
            value_to_index = category_index[col]
            category_mappings[col] = value_to_index
            
            # Create list of original values and replacement values for the replace method
            original_values = list(value_to_index.keys())
            replacement_values = list(value_to_index.values())
            
            try:
                # Replace values with indices using replace
                result_df = result_df.with_columns(
                    pl.col(col).replace(original_values, replacement_values).alias(f"{col}_indexed")
                )
                logger.debug(f"Applied category indexing to column: {col}")
            except Exception as e:
                logger.error(f"Error applying category indexing to column {col}: {e}", exc_info=True)
        elif col not in df.columns:
            logger.warning(f"Column {col} not found in DataFrame. Skipping category indexing for this column.")
        elif col not in category_index:
            logger.warning(f"No mapping found for column {col} in category index. Skipping category indexing for this column.")
    
    logger.info(f"Category indexing applied to {len(category_mappings)} columns")
    return result_df, category_mappings 