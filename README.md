# py-pricer

A Python library for insurance pricing that processes quote data, applies transformations, and calculates insurance prices based on user-defined rating logic.

## Overview

py-pricer provides a framework for insurance pricing with a clear separation between:
- **Library code** (`py_pricer` package): Core functionality that remains unchanged
- **User-editable content** (`algorithms` folder): Files that users customize for their specific pricing needs

This separation allows users to focus on their pricing logic while the library handles the infrastructure.

## Features

- Process insurance quotes from JSON or Parquet files
- Apply customizable data transformations
- Calculate prices using user-defined rating algorithms
- Interactive Streamlit dashboard to visualize data and results
- REST API for programmatic premium calculations

## Installation

```bash
# Install UV if not already installed
pip install uv

# Create and activate a virtual environment
uv venv
# Activate the environment (varies by platform)

# Install the py-pricer package
uv pip install py-pricer
```

## Getting Started

After installation, you need to initialize the `algorithms` folder with example files:

```python
import py_pricer
py_pricer.initialize()
```

This will download the example algorithms directory from GitHub, containing sample data, transformations, and rating logic.

## Running the Streamlit App

After installing py-pricer and initializing the algorithms folder, you can run the Streamlit app using any of these methods:

### Method 1: Using the console script (recommended)

After installation, you can run the app with a simple command:

```bash
py-pricer-app
```

This will automatically open your default web browser with the Streamlit dashboard. If the browser doesn't open automatically, you can access the app at http://localhost:8501.

### Method 2: Using the run_app.py script

The repository includes a script to run the Streamlit app. Download this script and run it:

```bash
# Download the script from GitHub
curl -o run_app.py https://raw.githubusercontent.com/PricingFrontier/py-pricer/main/run_app.py

# Make it executable
chmod +x run_app.py

# Run the app
python run_app.py
```

This will also open your browser automatically with the Streamlit dashboard.

### Method 3: Using Streamlit directly

You can run the app directly with Streamlit if you know the path to the app.py file:

```bash
# Find the path to the app.py file
APP_PATH=$(python -c "import os, py_pricer; print(os.path.join(os.path.dirname(py_pricer.__file__), 'app.py'))")

# Run Streamlit with the app.py file
streamlit run "$APP_PATH" --browser.serverAddress=localhost --server.headless=false
```

This ensures the browser opens and the server is not in headless mode.

## API Usage

The project includes a FastAPI-based REST API for programmatic premium calculations.

### Starting the API Server

```bash
python run_api.py
```

This will start the API server at http://localhost:8000. You can configure the host, port, and other options using command-line arguments. For example:

```bash
python run_api.py --host 127.0.0.1 --port 8000 --reload --log-level debug
```

### API Endpoints

1. **Calculate Premium for a Single Quote**

   ```
   POST /calculate_premium
   ```

   Example request:
   ```json
   {
     "IDpol": 1,
     "Exposure": 0.1,
     "VehPower": 5,
     "VehAge": 0,
     "DrivAge": 55,
     "BonusMalus": 50,
     "VehBrand": "B12",
     "VehGas": "Regular",
     "Area": "D",
     "Density": 1217,
     "Region": "Rhone-Alpes"
   }
   ```

   Example response:
   ```json
   {
     "premium": 175.0,
     "quote": {
       "IDpol": 1,
       "Exposure": 0.1,
       "VehPower": 5,
       "VehAge": 0,
       "DrivAge": 55,
       "BonusMalus": 50,
       "VehBrand": "B12",
       "VehGas": "Regular",
       "Area": "D",
       "Density": 1217,
       "Region": "Rhone-Alpes"
     },
     "factors": {
       "base_value": 175.0
     }
   }
   ```

2. **Calculate Premiums for Multiple Quotes (Batch)**

   ```
   POST /calculate_premiums_batch
   ```

   Example request:
   ```json
   {
     "quotes": [
       {
         "IDpol": 1,
         "Exposure": 0.1,
         "VehPower": 5,
         "VehAge": 0,
         "DrivAge": 55,
         "BonusMalus": 50,
         "VehBrand": "B12",
         "VehGas": "Regular",
         "Area": "D",
         "Density": 1217,
         "Region": "Rhone-Alpes"
       },
       {
         "IDpol": 3,
         "Exposure": 0.5,
         "VehPower": 6,
         "VehAge": 2,
         "DrivAge": 45,
         "BonusMalus": 60,
         "VehBrand": "B2",
         "VehGas": "Diesel",
         "Area": "B",
         "Density": 900,
         "Region": "Paris"
       }
     ]
   }
   ```

### API Documentation

FastAPI automatically generates interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Testing the API

A test script is included to demonstrate how to use the API:

```bash
python test_api.py
```

The test script:
- Uses real data files from the `algorithms/data` directory
- Demonstrates single quote and batch processing
- Shows how to handle API responses

You can also test the API with curl:

```bash
# Test a single quote
curl -X POST -H "Content-Type: application/json" -d @algorithms/data/1.json http://localhost:8000/calculate_premium

# Use JSON pretty-print to format the response
curl -X POST -H "Content-Type: application/json" -d @algorithms/data/1.json http://localhost:8000/calculate_premium | json_pp
```

## Project Structure

```
py-pricer/
├── py_pricer/                  # LIBRARY CODE (DO NOT MODIFY)
│   ├── __init__.py
│   ├── initializer.py          # Creates the algorithms folder with examples
│   ├── data_processor.py       # Data loading and processing
│   ├── transformer.py          # Transformation framework
│   ├── rating_engine.py        # Rating calculation engine
│   ├── app.py                  # Streamlit application
│   └── api.py                  # FastAPI application
├── algorithms/                 # USER-EDITABLE CONTENT
│   ├── data/                   # Your data files
│   │   └── input/              # Raw input data (JSON/parquet)
│   ├── rating_tables/          # Your rating tables
│   ├── transformations/        # Your transformation logic
│   └── rating/                 # Your rating algorithms
├── run_api.py                  # Script to run the API server
└── test_api.py                 # Script to test the API
```

## Workflow

1. The library code (`py_pricer`) provides the infrastructure and remains unchanged
2. Users customize their pricing models by editing files in the `algorithms` folder
3. The Streamlit app uses both components to process data and calculate prices
4. The API provides programmatic access to the pricing functionality

## License

[License information]
