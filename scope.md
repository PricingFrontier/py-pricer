# Insurance Pricing Library Scope

## Overview
A Python library for insurance pricing that processes quote data (JSON or Parquet format), applies transformations, and calculates insurance prices based on user-defined rating logic.

## Design Philosophy
The library follows a clear separation of concerns:
- **Library Code** (`py_pricer` package): Immutable core functionality that users should not modify
- **User-Editable Content** (`algorithms` folder): All customizable aspects that users will modify for their specific pricing needs

This separation allows users to focus exclusively on their pricing logic while the library provides all the infrastructure.

## Data Input
- **Supported Formats**:
  - Individual JSON files (each representing a single insurance quote)
  - Multiple JSON files (collection of quotes)
  - Parquet files (each row representing a quote)
- **Example Data Structure** (from sample):
  - Quote attributes include: IDpol, Exposure, VehPower, VehAge, DrivAge, BonusMalus, VehBrand, VehGas, Area, Density, Region

## Project Structure
```
py-pricer/
├── py_pricer/                  # LIBRARY CODE (NOT USER-EDITABLE)
│   ├── __init__.py
│   ├── initializer.py          # Script to generate folder structure and example
│   ├── data_processor.py       # Data loading and processing functions
│   ├── transformer.py          # Data transformation logic
│   ├── rating_engine.py        # Price calculation logic
│   ├── app.py                  # Streamlit app implementation
│   └── api.py                  # FastAPI API implementation
├── algorithms/                 # USER-EDITABLE CONTENT
│   ├── data/                   # User's data files (input data)
│   │   └── input/              # Raw input data (JSON/parquet)
│   ├── rating_tables/          # Rating tables for calculations
│   ├── transformations/        # User-defined data transformation logic
│   └── rating/                 # User-defined rating algorithms
├── tests/                      # Test cases
├── run_api.py                  # Script to run the API server
├── test_api.py                 # Script to test the API
├── pyproject.toml              # Package and UV configuration
├── requirements.txt            # Dependencies
└── README.md                   # Usage documentation
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
- Apply user-defined transformations from `algorithms/transformations/`
- Map raw data to standardized format for rating
- Calculate derived fields needed for rating

### 4. Rating Engine
- Apply rating logic from `algorithms/rating/`
- Calculate premiums based on transformed data and rating tables in `algorithms/rating_tables/`
- Support for multiple rating algorithms

### 5. Streamlit Application
- **Tab 1: Input Data View**
  - Display raw input data in tabular format
  - Basic filtering and searching functionality
  
- **Tab 2: Transformed Data View**
  - Display data after transformation phase
  - Highlight derived fields and transformations applied
  
- **Tab 3: Rating Calculation**
  - Display final pricing calculations
  - Show intermediate steps in the rating process
  - Basic visualization of pricing components

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
5. Run the Streamlit app to see the example in action: `python -m py_pricer.app`
6. Run the API server to enable programmatic access: `python run_api.py`
7. Test the API to understand its functionality: `python test_api.py`
8. Customize the example by editing files in the `algorithms` folder:
   - Replacing sample data in `algorithms/data/input/`
   - Modifying rating tables in `algorithms/rating_tables/`
   - Adapting transformation logic in `algorithms/transformations/`
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