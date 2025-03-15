"""
Raw data viewing module for the Streamlit application.

This module provides functionality for viewing raw insurance quote data.
"""

import streamlit as st
import polars as pl
import sys
import os

# Add the project root to the Python path if not already there
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from algorithms.config import get_primary_id
from algorithms.pipeline.utils import load_batch_data, load_individual_data

def show_raw_data_tab(df=None, data_source=None, on_data_source_change=None):
    """
    Display the raw data tab in the Streamlit application.
    
    Args:
        df: Pre-loaded Polars DataFrame (if None, will show an error)
        data_source: The source of the data ("Batch" or "Individual")
        on_data_source_change: Callback function to handle data source changes
    """
    # App title and description
    st.title("Raw Data Viewer")
    st.markdown("""
    This application allows you to view insurance quote data.
    """)

    # Data source selection in the Raw Data tab
    new_data_source = st.radio(
        "Select Data Source",
        ["Batch", "Individual"],
        horizontal=True,
        index=0 if data_source == "Batch" else 1
    )
    
    # If data source changed and callback is provided, call it
    if new_data_source != data_source and on_data_source_change:
        on_data_source_change(new_data_source)
        return  # Return early as we'll reload with the new data source
    
    # Show loading status
    if df is None:
        status = st.empty()
        status.info(f"Loading {new_data_source.lower()} data...")
    
    # Display data if provided
    if df is not None:
        # Show data info
        st.write(f"Loaded {df.height} rows and {df.width} columns")
        
        # Get the primary ID field
        primary_id = get_primary_id()
        
        # Display the dataframe with the primary ID as the index
        st.subheader("Data Viewer")
        st.dataframe(df, use_container_width=True, key=primary_id)
    else:
        st.error("No data available to display. Please check your data files.") 