"""
Data processing module for the insurance pricing library.

This module applies transformations to insurance quote data using configuration
from JSON files and custom transformation functions.
"""

import os
import polars as pl
from typing import Optional

from algorithms.pipeline.utils import (
    load_transformation_configs,
    apply_category_mapping,
    apply_continuous_banding
)
from algorithms.pipeline.additional_transforms import transform_data

def process_data(df: pl.DataFrame, config_dir: Optional[str] = None) -> pl.DataFrame:
    """
    Process data by applying all transformations.
    
    Args:
        df: Input DataFrame
        config_dir: Directory containing configuration files (default: algorithms/pipeline)
        
    Returns:
        Processed DataFrame with all transformations applied
    """
    # Load configuration files
    category_config, banding_config = load_transformation_configs(config_dir)
    
    # 1. Apply custom transformations from additional_transforms.py
    df = transform_data(df)
    
    # 2. Apply continuous banding
    df = apply_continuous_banding(df, banding_config)
    
    # 3. Apply category mapping
    df = apply_category_mapping(df, category_config)
    
    return df 