import os
import json
import streamlit as st
import polars as pl
import logging
from pathlib import Path
from py_pricer import transformer, get_data_dir, logger, get_rating_dir, get_algorithms_dir
from py_pricer.utils import find_files_by_extension, safe_load_json, safe_load_parquet
from py_pricer.config import STREAMLIT_PAGE_TITLE, STREAMLIT_PAGE_ICON, STREAMLIT_LAYOUT, SUPPORTED_DATA_FORMATS, MAX_ROWS_DISPLAY

# Import the rating engine - using a direct path approach instead
import sys
import importlib.util

# Create a module-specific logger
logger = logging.getLogger('py_pricer.app')

# Dynamically import the rating_engine module
def import_rating_engine():
    try:
        rating_dir = get_rating_dir()
        rating_engine_path = os.path.join(rating_dir, "rating_engine.py")
        
        if not os.path.exists(rating_engine_path):
            logger.error(f"Rating engine not found at: {rating_engine_path}")
            return None, None
            
        module_name = "rating_engine"
        spec = importlib.util.spec_from_file_location(module_name, rating_engine_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        logger.info(f"Successfully imported rating engine from {rating_engine_path}")
        return module.apply_base_rating, module.load_base_values
    except Exception as e:
        logger.error(f"Error importing rating engine: {e}", exc_info=True)
        return None, None

# Import the rating engine functions
apply_base_rating, load_base_values = import_rating_engine()

def find_data_files(directory):
    """Find all JSON and Parquet files in the directory."""
    return find_files_by_extension(directory, SUPPORTED_DATA_FORMATS)

def load_data(file_path):
    """Load data from either JSON or Parquet file."""
    file_extension = os.path.splitext(file_path)[1].lower()
    
    try:
        if file_extension == '.json':
            # Load JSON file
            data = safe_load_json(file_path)
            if data is None:
                return None
                
            # Convert to DataFrame - handle both single quote and list of quotes
            if isinstance(data, dict):
                df = pl.DataFrame([data])
            else:
                df = pl.DataFrame(data)
            logger.info(f"Successfully loaded JSON data from {file_path}")
        elif file_extension == '.parquet':
            # Load Parquet file
            df = safe_load_parquet(file_path)
            if df is None:
                return None
            logger.info(f"Successfully loaded Parquet data from {file_path}")
        else:
            error_msg = f"Unsupported file format: {file_extension}"
            logger.error(error_msg)
            st.error(error_msg)
            return None
        
        logger.info(f"Loaded data with {df.height} rows and {df.width} columns")
        return df
    except Exception as e:
        error_msg = f"Error loading data from {file_path}: {e}"
        logger.error(error_msg, exc_info=True)
        st.error(error_msg)
        return None

def main():
    try:
        # Configure Streamlit page
        st.set_page_config(
            page_title=STREAMLIT_PAGE_TITLE,
            page_icon=STREAMLIT_PAGE_ICON,
            layout=STREAMLIT_LAYOUT
        )
        
        # Title and introduction
        st.title("py-pricer Dashboard")
        st.write("Upload insurance quote data, apply transformations, and calculate premiums using the rating engine.")
        
        # Log the paths we're using to help with debugging
        algorithms_dir = get_algorithms_dir()
        data_dir = get_data_dir()
        logger.info(f"Using algorithms directory: {algorithms_dir}")
        logger.info(f"Using data directory: {data_dir}")
        logger.info(f"Current working directory: {os.getcwd()}")
        
        # Check if algorithms directory exists
        if not os.path.exists(algorithms_dir):
            st.error(
                "The algorithms directory was not found. Please run the initializer first:\n\n"
                "```python\n"
                "import py_pricer\n"
                "py_pricer.initialize()\n"
                "```"
            )
            return
        
        # Continue with the rest of the app
        # Create tabs for the different views
        tab1, tab2, tab3 = st.tabs(["Input Data", "Transformed Data", "Rating Calculation"])
        
        # Find data files in the algorithms/data directory using the utility function
        data_files = find_data_files(data_dir)
        
        # Debug info to see what's happening
        st.sidebar.write(f"Looking for data in: {os.path.abspath(data_dir)}")
        st.sidebar.write(f"Found {len(data_files)} data files")
        if data_files:
            st.sidebar.write("First few files:")
            for file in data_files[:3]:
                st.sidebar.write(f"- {file}")
        
        # Session state for storing the selected file and data
        if 'selected_file' not in st.session_state:
            st.session_state.selected_file = None
        if 'dataframe' not in st.session_state:
            st.session_state.dataframe = None
        if 'transformed_df' not in st.session_state:
            st.session_state.transformed_df = None
        if 'category_mappings' not in st.session_state:
            st.session_state.category_mappings = None
        if 'rated_df' not in st.session_state:
            st.session_state.rated_df = None
        if 'base_values_df' not in st.session_state:
            st.session_state.base_values_df = None
        
        # Create a mapping of display names (without prefix) to full file paths
        file_mapping = {}
        if data_files:
            file_mapping = {os.path.basename(file_path): file_path for file_path in data_files}
            display_names = sorted(file_mapping.keys())
        
        with tab1:
            st.header("Input Data View")
            
            if not data_files:
                st.warning("No data files found. Please add JSON or Parquet files to the data directory.")
            else:
                # Create file selector with just the filenames (no path prefix)
                selected_display_name = st.selectbox("Select a data file:", display_names)
                
                if selected_display_name:
                    try:
                        # Get the full path for the selected display name
                        selected_file = file_mapping[selected_display_name]
                        
                        # Check if file selection has changed
                        if selected_file != st.session_state.selected_file:
                            # Load and display data
                            df = load_data(selected_file)
                            if df is not None:
                                st.session_state.selected_file = selected_file
                                st.session_state.dataframe = df
                                
                                # Apply transformations and store in session state
                                try:
                                    transformed_df, category_mappings = transformer.apply_category_indexing(df)
                                    st.session_state.transformed_df = transformed_df
                                    st.session_state.category_mappings = category_mappings
                                    
                                    # Debug information
                                    st.sidebar.write("Debug Information:")
                                    st.sidebar.write(f"Available columns: {df.columns}")
                                    st.sidebar.write(f"Category mappings found: {list(category_mappings.keys())}")
                                except Exception as e:
                                    error_msg = f"Error applying transformations: {e}"
                                    logger.error(error_msg, exc_info=True)
                                    st.error(error_msg)
                        
                        if st.session_state.dataframe is not None:
                            df = st.session_state.dataframe
                            st.write(f"Displaying data from: {selected_display_name}")
                            st.write(f"Number of rows: {df.height}")
                            st.write(f"Number of columns: {df.width}")
                            
                            # Display the dataframe
                            st.dataframe(df, use_container_width=True)
                    except Exception as e:
                        error_msg = f"Error processing selected file: {e}"
                        logger.error(error_msg, exc_info=True)
                        st.error(error_msg)
        
        with tab2:
            st.header("Transformed Data View")
            
            if st.session_state.transformed_df is not None:
                try:
                    df = st.session_state.transformed_df
                    mappings = st.session_state.category_mappings
                    
                    st.write(f"Transformed data with category indexing applied")
                    st.write(f"Number of rows: {df.height}")
                    
                    # Show the transformations applied
                    if mappings and len(mappings) > 0:
                        st.subheader("Categorical Mappings Applied")
                        for col, mapping in mappings.items():
                            with st.expander(f"Mapping for '{col}'"):
                                mapping_df = pl.DataFrame({
                                    "Original Value": list(mapping.keys()),
                                    "Index Value": list(mapping.values())
                                })
                                st.dataframe(mapping_df, use_container_width=True)
                        
                        # Display the transformed dataframe
                        st.subheader("Transformed Data")
                        st.write(f"Number of rows: {df.height}")
                        st.write(f"Number of columns: {df.width}")
                        st.dataframe(df, use_container_width=True)
                        
                        # Apply base rating and store in session state
                        try:
                            if apply_base_rating is not None:
                                rated_df, base_values_df = apply_base_rating(df)
                                st.session_state.rated_df = rated_df
                                st.session_state.base_values_df = base_values_df
                            else:
                                logger.warning("Rating engine could not be loaded. Skipping base rating.")
                                st.warning("Rating engine could not be loaded. Skipping base rating.")
                        except Exception as e:
                            error_msg = f"Error applying base rating: {e}"
                            logger.error(error_msg, exc_info=True)
                            st.error(error_msg)
                    else:
                        st.info("No categorical columns found for indexing.")
                        st.dataframe(df, use_container_width=True)
                except Exception as e:
                    error_msg = f"Error displaying transformed data: {e}"
                    logger.error(error_msg, exc_info=True)
                    st.error(error_msg)
            else:
                st.info("Please select a data file in the 'Input Data' tab.")
            
        with tab3:
            st.header("Rating Calculation")
            
            if apply_base_rating is None:
                st.warning("Rating engine could not be loaded. Please check the logs for details.")
            elif st.session_state.rated_df is not None:
                try:
                    rated_df = st.session_state.rated_df
                    base_values_df = st.session_state.base_values_df
                    
                    st.subheader("Base Values Table")
                    if base_values_df is not None:
                        st.dataframe(base_values_df, use_container_width=True)
                    else:
                        st.warning("Base values table could not be loaded.")
                    
                    st.subheader("Applied Base Value")
                    if "BaseValue" in rated_df.columns:
                        # Extract only the Area and BaseValue columns
                        if "Area" in rated_df.columns:
                            base_value_display = rated_df.select(["Area", "BaseValue"])
                            st.write("Base values applied based on the Area column:")
                            st.dataframe(base_value_display, use_container_width=True)
                        else:
                            # If Area column is not available, just show the BaseValue
                            base_value_display = rated_df.select(["BaseValue"])
                            st.write("Applied base values:")
                            st.dataframe(base_value_display, use_container_width=True)
                    else:
                        st.warning("Base values could not be applied. Check if the Area column exists in the data.")
                except Exception as e:
                    error_msg = f"Error displaying rating calculations: {e}"
                    logger.error(error_msg, exc_info=True)
                    st.error(error_msg)
            else:
                st.info("Please select a data file in the 'Input Data' tab to see rating calculations.")
    except Exception as e:
        error_msg = f"An unexpected error occurred: {e}"
        logger.error(error_msg, exc_info=True)
        st.error(error_msg)

if __name__ == "__main__":
    # When run directly, just call main() and let Streamlit handle the execution
    # This is the simplest approach and avoids any recursive launching issues
    main()
else:
    # When imported as a module, the main function will be called by Streamlit
    pass
