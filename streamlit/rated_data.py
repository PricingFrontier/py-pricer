"""
Rated data viewing module for the Streamlit application.

This module provides functionality for viewing insurance quote data with calculated premiums,
focusing on the columns created by the rating engine.
"""

import streamlit as st
import polars as pl
import sys
import os

# Add the project root to the Python path if not already there
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from algorithms.config import get_primary_id

def show_rated_data_tab(df=None, data_source=None, original_df=None):
    """
    Display the rated data tab in the Streamlit application.
    
    Args:
        df: Rated Polars DataFrame (if None, will show an error)
        data_source: The source of the data ("Batch" or "Individual")
        original_df: The original transformed DataFrame before rating was applied
    """
    # Tab title
    st.title("Rating Results")

    # Early return if no data is provided
    if df is None:
        st.error("No rated data available to display.")
        return
    
    # Get the primary ID field
    primary_id = get_primary_id()
    
    # Automatically detect columns added by the rating engine
    # by comparing with the original transformed dataframe
    if original_df is not None:
        # Find columns that exist in rated df but not in original df
        rating_columns = [col for col in df.columns if col not in original_df.columns]
    else:
        # If original_df is not available, we can't detect rating columns
        st.warning("Original transformed data not available. Cannot detect rating columns.")
        return
    
    # Early return if no rating columns are found
    if not rating_columns:
        st.warning("No rating columns found in the data. Rating may not have been applied.")
        return
    
    # Determine columns to show - only primary key and rating columns
    columns_to_show = rating_columns
    if primary_id in df.columns:
        columns_to_show = [primary_id] + columns_to_show
    
    # Create a new dataframe with only the selected columns
    rated_df = df.select(columns_to_show)
    
    # Display the dataframe with the primary ID as the key
    st.dataframe(rated_df, use_container_width=True, key=primary_id) 