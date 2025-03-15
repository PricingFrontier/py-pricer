# Current State of the Insurance Pricing Library

This document describes the current state of the py-pricer project as of the latest update. It serves as a reference for understanding what has been implemented and how the different components work together.

## Overview

The py-pricer library is a Python-based insurance pricing tool that processes insurance quote data, applies transformations, and will eventually calculate prices based on user-defined rating logic. The project follows a modular architecture with a clear separation between library code and user-editable content.

## Implemented Components

### 1. Data Processing Pipeline

- **Data Loading**: 
  - Successfully loads data from both JSON files (individual quotes) and Parquet files (batch quotes)
  - Implemented in `algorithms/pipeline/utils.py` with functions `load_batch_data()` and `load_individual_data()`
  - Uses Polars for efficient data processing
  - Supports multiple file formats through a generic `load_directory_data()` function

- **Data Transformation**:
  - Applies transformations to raw data in a structured pipeline
  - Implemented in `algorithms/pipeline/data_processor.py` with the main function `process_data()`
  - Transformation steps:
    1. Custom transformations from `additional_transforms.py`
    2. Category mapping (converting categorical values to numeric indices)
    3. Continuous variable banding (grouping continuous variables into categories)

- **Configuration**:
  - User-defined configuration in `algorithms/config.py` for setting primary ID and other parameters
  - Transformation configurations:
    - `algorithms/pipeline/category-index.json`: Maps categorical values to numeric indices
    - `algorithms/pipeline/continuous-banding.json`: Defines bands for continuous variables

### 2. Streamlit Application

The Streamlit application provides a user interface for viewing and exploring the data. It's organized into multiple files for better maintainability:

- **Main Application** (`streamlit/app.py`):
  - Sets up the Streamlit interface with tabs
  - Manages data loading and transformation
  - Uses session state to maintain data between interactions
  - Handles data source changes

- **Raw Data Tab** (`streamlit/raw_data.py`):
  - Displays the original, unprocessed data
  - Provides data source selection (Batch or Individual)
  - Shows information about available data sources

- **Banded Data Tab** (`streamlit/banded_data.py`):
  - Shows continuous variables that have been banded into categories
  - Uses the configuration from `continuous-banding.json`
  - Displays only the banded columns for clarity

- **Indexed Data Tab** (`streamlit/indexed_data.py`):
  - Shows categorical variables that have been converted to numeric indices
  - Uses the configuration from `category-index.json`
  - Displays only the indexed columns for clarity

### 3. Data Flow

1. User selects a data source (Batch or Individual) in the Raw Data tab
2. The application loads the data using the appropriate function
3. The data is transformed using the `process_data()` function
4. Both raw and transformed data are stored in session state
5. Each tab displays its relevant portion of the data

## Current Limitations

1. **Rating Engine**: Not yet implemented. The application currently focuses on data viewing and transformation.
2. **API**: Basic structure exists but not fully implemented.
3. **Error Handling**: Basic error handling is in place, but could be improved for edge cases.
4. **Performance**: Large datasets might experience performance issues.

## Next Steps

1. **Rating Engine Implementation**:
   - Develop the rating engine to calculate premiums based on transformed data
   - Create a new tab in the Streamlit app to display rating results

2. **API Development**:
   - Complete the FastAPI implementation for programmatic access
   - Ensure consistency between API and UI calculations

3. **Enhanced Visualization**:
   - Add basic charts and graphs to visualize data distributions
   - Implement summary statistics for transformed data

4. **Documentation**:
   - Improve inline code documentation
   - Create comprehensive user guide

## Running the Application

To run the application:

```bash
python run_app.py
```

Then navigate to `http://localhost:8501` in your web browser.

## File Structure Reference

```
py-pricer/
├── streamlit/                          # STREAMLIT APP IMPLEMENTATION
│   ├── app.py                          # Main Streamlit app implementation
│   ├── raw_data.py                     # Raw data viewing module
│   ├── banded_data.py                  # Banded categories viewing module
│   └── indexed_data.py                 # Indexed categories viewing module
├── algorithms/
│   ├── config.py                       # User configuration settings
│   ├── data/                           # User's data files
│   │   ├── batch/                      # Batch processing data (Parquet)
│   │   └── individual/                 # Individual quote data (JSON)
│   └── pipeline/                       # Data processing pipeline
│       ├── data_processor.py           # Data processing functions
│       ├── utils.py                    # Utility functions (refactored)
│       ├── additional_transforms.py    # Custom transformations
│       ├── category-index.json         # Category to index mappings
│       ├── continuous-banding.json     # Continuous variable banding
│       └── __init__.py                 # Package initialization
└── run_app.py                          # Script to run the Streamlit app
```

## Key Configuration Files

### category-index.json

This file maps categorical variables to numeric indices. Example structure:

```json
{
    "VehBrand": {
        "B1": 1,
        "B2": 2,
        "B3": 3,
        ...
    },
    "VehGas": {
        "Regular": 1,
        "Diesel": 2
    },
    ...
}
```

### continuous-banding.json

This file defines how continuous variables are banded into categories. Example structure:

```json
{
    "DrivAge": {
        "bands": [
            {"min": 0, "max": 25, "label": "Under 25"},
            {"min": 25, "max": 40, "label": "25-39"},
            {"min": 40, "max": 60, "label": "40-59"},
            {"min": 60, "max": 999, "label": "60+"}
        ],
        "column_name": "DrivAgeBand",
        "min_inclusive": true,
        "max_exclusive": true
    },
    ...
}
```

## Recent Improvements

1. **Code Refactoring**:
   - Refactored `utils.py` to reduce redundancy and improve code organization
   - Created generic functions for common operations:
     - `load_directory_data()`: Unified function for loading data from directories
     - `get_data_directory()`: Helper for consistent path construction
   - Implemented dictionary-based dispatch for file type handling
   - Improved error handling with early returns

2. **Folder Restructuring**:
   - Consolidated transformation files into the `pipeline` folder
   - Moved configuration files (`category-index.json` and `continuous-banding.json`) to the pipeline folder
   - Updated all references to these files throughout the codebase
   - Streamlined the project structure for better organization

3. **Documentation Updates**:
   - Updated documentation to reflect the current state of the project
   - Improved inline code documentation with clearer docstrings
   - Ensured consistency between code and documentation 