"""
Banded data viewing module for the Streamlit application.

This module provides functionality for viewing insurance quote data with banded categories,
focusing on the columns created by category banding.
"""

import streamlit as st
import polars as pl
import sys
import os
import json

# Add the project root to the Python path if not already there
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from algorithms.config import get_primary_id

def load_banding_config():
    """
    Load the continuous banding configuration from JSON file.
    
    Returns:
        Dictionary containing the banding configuration or empty dict if loading fails
    """
    try:
        # Get the path to the continuous-banding.json file
        config_path = os.path.abspath(os.path.join(
            os.path.dirname(__file__), 
            '..', 
            'algorithms', 
            'pipeline', 
            'continuous-banding.json'
        ))
        
        # Load the configuration
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        return config
    except Exception as e:
        st.warning(f"Could not load banding configuration: {e}")
        return {}

def show_transformed_data_tab(df=None, data_source=None):
    """
    Display the banded data tab in the Streamlit application.
    
    Args:
        df: Pre-transformed Polars DataFrame (if None, will show an error)
        data_source: The source of the data ("Batch" or "Individual")
    """
    # Tab title
    st.title("Banded Categories")

    # Early return if no data is provided
    if df is None:
        st.error("No transformed data available to display.")
        return
    
    # Get the primary ID field
    primary_id = get_primary_id()
    
    # Load the banding configuration to identify the expected band columns
    banding_config = load_banding_config()
    
    # Early return if no configuration is available
    if not banding_config:
        st.warning("Could not load banding configuration or it's empty.")
        return
    
    # Get the expected band column names from the configuration
    expected_band_columns = []
    for column, config in banding_config.items():
        band_column = config.get("column_name", f"{column}Band")
        expected_band_columns.append(band_column)
    
    # Find the actual band columns in the dataframe
    actual_band_columns = [col for col in df.columns if col in expected_band_columns]
    
    # Early return if no banded columns are found
    if not actual_band_columns:
        st.warning("No banded columns found in the transformed data.")
        return
    
    # Determine columns to show
    columns_to_show = actual_band_columns
    if primary_id in df.columns:
        columns_to_show = [primary_id] + actual_band_columns
    
    # Create a new dataframe with only the selected columns
    banded_df = df.select(columns_to_show)
    
    # Display the dataframe with the primary ID as the key
    st.dataframe(banded_df, use_container_width=True, key=primary_id) 