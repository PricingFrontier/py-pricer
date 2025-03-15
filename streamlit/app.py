"""
Streamlit application for the insurance pricing library.

This is the main entry point for the Streamlit application.
"""

import streamlit as st
import os
import sys

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the tab modules
from raw_data import show_raw_data_tab
from banded_data import show_transformed_data_tab
from indexed_data import show_indexed_data_tab
from algorithms.pipeline.utils import load_batch_data, load_individual_data
from algorithms.pipeline.data_processor import process_data

# Set page config
st.set_page_config(
    page_title="Insurance Pricing App",
    page_icon="📊",
    layout="wide"
)

# Initialize session state for data source if it doesn't exist
if 'data_source' not in st.session_state:
    st.session_state.data_source = "Batch"
    st.session_state.raw_df = None
    st.session_state.transformed_df = None

# Function to handle data source changes
def change_data_source(new_source):
    st.session_state.data_source = new_source
    st.session_state.raw_df = None
    st.session_state.transformed_df = None
    st.rerun()

# Load data if not already loaded
if st.session_state.raw_df is None:
    data_source = st.session_state.data_source
    
    # Load data based on selection
    if data_source == "Batch":
        st.session_state.raw_df = load_batch_data()
    else:  # Individual
        st.session_state.raw_df = load_individual_data()
    
    # Transform data if loaded successfully
    if st.session_state.raw_df is not None:
        st.session_state.transformed_df = process_data(st.session_state.raw_df)

# Create tabs
tab1, tab2, tab3 = st.tabs(["Raw Data", "Banded Data", "Indexed Data"])

# Show the appropriate content in each tab
with tab1:
    show_raw_data_tab(
        st.session_state.raw_df, 
        st.session_state.data_source,
        on_data_source_change=change_data_source
    )
    
with tab2:
    show_transformed_data_tab(
        st.session_state.transformed_df, 
        st.session_state.data_source
    )
    
with tab3:
    show_indexed_data_tab(
        st.session_state.transformed_df,
        st.session_state.data_source
    ) 