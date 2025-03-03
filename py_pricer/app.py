import os
import json
import streamlit as st
import polars as pl
from pathlib import Path
import transformer

def find_data_files(directory):
    """Find all JSON and Parquet files in the directory."""
    files = []
    for path in Path(directory).rglob('*'):
        if path.is_file() and path.suffix.lower() in ['.json', '.parquet']:
            files.append(str(path))
    return sorted(files)

def load_data(file_path):
    """Load data from either JSON or Parquet file."""
    file_extension = os.path.splitext(file_path)[1].lower()
    
    if file_extension == '.json':
        # Load JSON file
        with open(file_path, 'r') as f:
            data = json.load(f)
        # Convert to DataFrame - handle both single quote and list of quotes
        if isinstance(data, dict):
            df = pl.DataFrame([data])
        else:
            df = pl.DataFrame(data)
    elif file_extension == '.parquet':
        # Load Parquet file
        df = pl.read_parquet(file_path)
    else:
        st.error(f"Unsupported file format: {file_extension}")
        return None
    
    return df

def main():
    st.title("Insurance Pricing Library")
    
    # Create tabs for the different views
    tab1, tab2, tab3 = st.tabs(["Input Data", "Transformed Data", "Rating Calculation"])
    
    # Find data files in the parent directory's algorithms/data directory
    data_dir = "../algorithms/data"
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
                # Get the full path for the selected display name
                selected_file = file_mapping[selected_display_name]
                
                # Check if file selection has changed
                if selected_file != st.session_state.selected_file:
                    # Load and display data
                    df = load_data(selected_file)
                    st.session_state.selected_file = selected_file
                    st.session_state.dataframe = df
                    
                    # Apply transformations and store in session state
                    transformed_df, category_mappings = transformer.apply_category_indexing(df)
                    st.session_state.transformed_df = transformed_df
                    st.session_state.category_mappings = category_mappings
                    
                    # Debug information
                    st.sidebar.write("Debug Information:")
                    st.sidebar.write(f"Available columns: {df.columns}")
                    st.sidebar.write(f"Category mappings found: {list(category_mappings.keys())}")
                
                if st.session_state.dataframe is not None:
                    df = st.session_state.dataframe
                    st.write(f"Displaying data from: {selected_display_name}")
                    st.write(f"Number of rows: {df.height}")
                    st.write(f"Number of columns: {df.width}")
                    
                    # Display the dataframe
                    st.dataframe(df)
    
    with tab2:
        st.header("Transformed Data View")
        
        if st.session_state.transformed_df is not None:
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
                        st.dataframe(mapping_df)
                
                # Display the transformed dataframe
                st.subheader("Transformed Data")
                st.dataframe(df)
            else:
                st.info("No categorical columns found for indexing.")
                st.dataframe(df)
        else:
            st.info("Please select a data file in the 'Input Data' tab.")
        
    with tab3:
        st.header("Rating Calculation")
        st.info("This tab will show rating calculations. Currently in development.")

if __name__ == "__main__":
    main()
