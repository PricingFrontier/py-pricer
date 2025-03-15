"""
Indexed data viewing module for the Streamlit application.

This module provides functionality for viewing insurance quote data with indexed categories,
focusing on the columns created by category indexing.
"""

import streamlit as st
import polars as pl
import sys
import os
import json

# Add the project root to the Python path if not already there
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from algorithms.config import get_primary_id

def load_index_config():
    """
    Load the category index configuration from JSON file.
    
    Returns:
        Dictionary containing the category index configuration or empty dict if loading fails
    """
    try:
        # Get the path to the category-index.json file
        config_path = os.path.abspath(os.path.join(
            os.path.dirname(__file__), 
            '..', 
            'algorithms', 
            'pipeline', 
            'category-index.json'
        ))
        
        # Load the configuration
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        return config
    except Exception as e:
        st.warning(f"Could not load category index configuration: {e}")
        return {}

def show_indexed_data_tab(df=None, data_source=None):
    """
    Display the indexed data tab in the Streamlit application.
    
    Args:
        df: Pre-transformed Polars DataFrame (if None, will show an error)
        data_source: The source of the data ("Batch" or "Individual")
    """
    # Tab title
    st.title("Indexed Categories")

    # Early return if no data is provided
    if df is None:
        st.error("No transformed data available to display.")
        return
    
    # Get the primary ID field
    primary_id = get_primary_id()
    
    # Load the index configuration to identify the expected index columns
    index_config = load_index_config()
    
    # Early return if no configuration is available
    if not index_config:
        st.warning("Could not load category index configuration or it's empty.")
        return
    
    # Get the expected index column names from the configuration
    expected_index_columns = [f"{column}_Index" for column in index_config.keys()]
    
    # Find the actual index columns in the dataframe
    actual_index_columns = [col for col in df.columns if col in expected_index_columns]
    
    # Early return if no indexed columns are found
    if not actual_index_columns:
        st.warning("No indexed columns found in the transformed data.")
        return
    
    # Determine columns to show
    columns_to_show = actual_index_columns
    if primary_id in df.columns:
        columns_to_show = [primary_id] + actual_index_columns
    
    # Create a new dataframe with only the selected columns
    indexed_df = df.select(columns_to_show)
    
    # Display the dataframe with the primary ID as the key
    st.dataframe(indexed_df, use_container_width=True, key=primary_id) 