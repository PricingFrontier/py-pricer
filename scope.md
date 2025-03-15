# Insurance Pricing Library Scope

## Overview
A Python library for insurance pricing that processes quote data (JSON or Parquet format), applies transformations, and calculates insurance prices based on user-defined rating logic.

## Design Philosophy
The library follows a clear separation of concerns:
- **Library Code** (`py_pricer` package): Immutable core functionality that users can not modify
- **User-Editable Content** (`algorithms` folder): All customizable aspects that users will modify for their specific pricing needs

This separation allows users to focus exclusively on their pricing logic while the library provides all the infrastructure.

## Data Input
- **Supported Formats**:
  - Individual JSON files (each representing a single insurance quote)
  - Parquet files (each row representing a quote)
- **Example Data Structure** (from sample):
  - Quote attributes include: IDpol, VehPower, VehAge, DrivAge, BonusMalus, VehBrand, VehGas, Area, Density, Region

## Project Structure
```
py-pricer/
├── py_pricer/                          # LIBRARY CODE (NOT USER-EDITABLE)
│   ├── __init__.py                     # Package initialization
│   ├── config.py                       # Configuration settings
│   ├── initializer.py                  # Script to generate folder structure and example
│   ├── initializer_launcher.py         # Entry point for initializer
│   ├── api_launcher.py                 # Entry point for API
│   └── app_launcher.py                 # Entry point for Streamlit app
├── api/                                # API IMPLEMENTATION
│   ├── __init__.py                     # Package initialization
│   ├── api.py                          # FastAPI implementation
│   ├── run_api.py                      # Script to run the API server
│   ├── test_api.py                     # Script to test the API
│   └── README.md                       # API documentation
├── streamlit/                          # STREAMLIT APP IMPLEMENTATION
│   ├── app.py                          # Main Streamlit app implementation
│   ├── raw_data.py                     # Raw data viewing module
│   ├── banded_data.py                  # Banded categories viewing module
│   └── indexed_data.py                 # Indexed categories viewing module
├── algorithms/                         # USER-EDITABLE CONTENT
│   ├── README.md                       # Documentation for algorithms
│   ├── config.py                       # User configuration settings
│   ├── data/                           # User's data files (input data)
│   │   ├── additional/                 # Additional data files
│   │   │   └── claims.parquet          # Sample claims data
│   │   ├── batch/                      # Batch processing data
│   │   │   └── policies.parquet        # Sample policies data
│   │   └── individual/                 # Individual quote data
│   │       ├── 1.json                  # Sample quote 1
│   │       ├── 2.json                  # Sample quote 2
│   │       ├── 3.json                  # Sample quote 3
│   │       ├── 5.json                  # Sample quote 5
│   │       ├── 10.json                 # Sample quote 10
│   │       └── 11.json                 # Sample quote 11
│   ├── pipeline/                       # Data processing pipeline
│   │   ├── data_processor.py           # Data loading and processing functions
│   │   ├── utils.py                    # Utility functions for data loading and transformation
│   │   ├── additional_transforms.py    # Where the user can define additional data transformations
│   │   ├── category-index.json         # Index configuration for categorical factors 
│   │   ├── continuous-banding.json     # Banding configuration for continuous variables
│   │   └── __init__.py                 # Package initialization
│   └── rating/                         # User-defined rating algorithms
│       ├── __init__.py                 # Package initialization
│       ├── rating_engine.py            # Rating engine implementation
│       └── tables/                     # Rating tables for calculations
│           ├── __init__.py             # Package initialization
│           └── base-values.csv         # Base values for rating
├── logs/                               # Log files
│   └── py_pricer.log                   # Application log file
├── pyproject.toml                      # Package and UV configuration
├── requirements.txt                    # Dependencies
├── MANIFEST.in                         # Package manifest
├── LICENSE                             # License information
├── scope.md                            # Project scope documentation
├── current-state.md                    # Current state documentation
├── run_app.py                          # Script to run the Streamlit app
└── README.md                           # Usage documentation
```

## Core Functionality

### 1. Initialization
- User installs the library via UV
- User runs an initialization script that generates the `algorithms` folder structure
- **Barebones Example**: The initializer will create a complete working example including:
  - Sample input data in both JSON and Parquet formats
  - Example rating tables (e.g., base rates, factor tables)
  - Sample transformation scripts (e.g., age bands, territory mapping)
  - Basic rating algorithm implementation
  - This example will serve as both documentation and a starting template for users

### 2. Data Processing
- Load data from JSON files or Parquet
- Validate basic data structure
- Prepare data for transformation phase

### 3. Data Transformation
- Apply user-defined transformations from `algorithms/pipeline/additional_transforms.py`
- Map raw data to standardized format for rating
- Calculate derived fields needed for rating
- Apply banding to continuous variables based on configuration in `algorithms/pipeline/continuous-banding.json`
- Convert categorical variables to numeric indices based on configuration in `algorithms/pipeline/category-index.json`

### 4. Rating Engine
- Apply rating logic from `algorithms/rating/`
- Calculate premiums based on transformed data and rating tables in `algorithms/rating_tables/`
- Support for multiple rating algorithms

### 5. Streamlit Application
- **Data Source Selection**
  - Choose between batch data (Parquet) and individual data (JSON)
  - Dynamically load and transform data based on selection
  
- **Tab 1: Raw Data View**
  - Display raw input data in tabular format
  - Data source selection interface
  - Information about available data sources
  
- **Tab 2: Banded Data View**
  - Display continuous variables that have been banded into categories
  - Show only the banded columns based on continuous-banding.json configuration
  - Use primary ID as the index for better readability
  
- **Tab 3: Indexed Data View**
  - Display categorical variables that have been converted to numeric indices
  - Show only the indexed columns based on category-index.json configuration
  - Use primary ID as the index for better readability

### 6. API Integration
- **FastAPI Implementation**
  - REST API for programmatic access to pricing functionality
  - Single quote processing endpoint
  - Batch processing for multiple quotes
  - JSON input and output format
  - Swagger UI for interactive API documentation

- **API Features**
  - Input validation using Pydantic models
  - Consistent pricing with the UI application
  - Error handling and appropriate HTTP responses
  - Integration with the existing transformation and rating modules

## Implementation Details

### Technology Stack
- **Core Language**: Python 3.8+
- **Data Processing**: Polars
- **File Formats**: JSON, Parquet (via pyarrow)
- **UI**: Streamlit
- **API**: FastAPI with Uvicorn
- **Package Manager**: UV
- **Testing**: Pytest

### Simplicity Focus
- Minimal dependencies
- Simple, functional code structure
- Limited error handling (focus on happy path)
- Straightforward configuration
- Minimal validation
- Basic documentation

## User Workflow
1. Install UV if not already installed: `pip install uv`
2. Create and activate a virtual environment with UV: `uv venv`
3. Install the library with UV: `uv pip install py-pricer`
4. Initialize the project structure with example: `python -m py_pricer.initializer`
5. Run the Streamlit app to see the example in action: `python run_app.py`
6. Run the API server to enable programmatic access: `python run_api.py`
7. Test the API to understand its functionality: `python test_api.py`
8. Customize the example by editing files in the `algorithms` folder:
   - Replacing sample data in `algorithms/data/`
   - Modifying rating tables in `algorithms/rating/tables/`
   - Adapting transformation logic in `algorithms/pipeline/additional_transforms.py`
   - Updating configuration files in `algorithms/pipeline/`
   - Updating rating algorithms in `algorithms/rating/`
9. Rerun the app and API to see your customizations

## Development Workflow
1. Library developers work on the `py_pricer` package to improve core functionality
2. Users never modify the library code, only the contents of the `algorithms` folder
3. This separation enables library updates without breaking user customizations

## Out of Scope
- Advanced error handling and validation
- Production-level security features
- User authentication and access control
- Advanced data visualization
- Complex statistical modeling
- Database integration
- Multi-user support
- Detailed logging and monitoring
- Deployment configurations 