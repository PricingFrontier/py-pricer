"""
Utility functions for the API.

This module provides helper functions for processing quote data.
"""

import polars as pl
from typing import Dict, Any, List, Optional
import json
from algorithms.pipeline.data_processor import process_data
from algorithms.rating.rating_engine import rate_policies
from algorithms.config import get_primary_id


def json_to_dataframe(json_data: Dict[str, Any]) -> pl.DataFrame:
    """
    Convert JSON data to a Polars DataFrame.
    
    Args:
        json_data: Dictionary containing quote data
        
    Returns:
        Polars DataFrame with the quote data
    """
    # Convert the JSON data to a DataFrame with a single row
    return pl.DataFrame([json_data])


def extract_premium_details(df: pl.DataFrame, original_df: pl.DataFrame) -> Dict[str, Any]:
    """
    Extract premium calculation details from the rated DataFrame.
    
    Args:
        df: Rated DataFrame with premium calculations
        original_df: Original DataFrame before rating was applied
        
    Returns:
        Dictionary containing premium calculation details
    """
    # Find columns added by the rating engine
    rating_columns = [col for col in df.columns if col not in original_df.columns]
    
    # Extract the values from the first row (since we're processing a single quote)
    premium_details = {}
    for col in rating_columns:
        premium_details[col] = df[0, col]
    
    return premium_details


def process_quote(json_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Process a quote through the transformation pipeline and rating engine.
    
    Args:
        json_data: Dictionary containing quote data
        
    Returns:
        Dictionary containing the quote ID and premium details
    """
    # Convert JSON to DataFrame
    df = json_to_dataframe(json_data)
    
    # Get the primary ID field
    primary_id = get_primary_id()
    
    # Extract the quote ID if available
    primary_id_value = None
    if primary_id in df.columns:
        primary_id_value = str(df[0, primary_id])
    
    # Process the data through the transformation pipeline
    transformed_df = process_data(df)
    
    # Apply rating
    rated_df = rate_policies(transformed_df)
    
    # Extract premium details
    premium_details = extract_premium_details(rated_df, transformed_df)
    
    # Return the results
    return {
        primary_id: primary_id_value,
        "premium_details": premium_details
    } 