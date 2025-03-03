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

After installation, you need to initialize the `algorithms` folder with example files. You can do this using the command-line tool:

```bash
py-pricer-init
```

Or if you want to force overwrite existing files:

```bash
py-pricer-init --force
```

You can also initialize programmatically:

```python
import py_pricer
py_pricer.initialize()
```

This will download the example algorithms directory from GitHub, containing sample data, transformations, and rating logic. The initializer will also copy useful template scripts to your working directory, including scripts for running and testing the API.

## Running the Streamlit App

After installing py-pricer and initializing the algorithms folder, you can run the Streamlit app using the console script:

```bash
py-pricer-app
```

If you encounter issues with the console script, you can also run the app directly:

```bash
python -c "from py_pricer.app_launcher import launch_app; launch_app()"
```

This will automatically open your default web browser with the Streamlit dashboard. If the browser doesn't open automatically, you can access the app at http://localhost:8501.

## API Usage

The project includes a FastAPI-based REST API for programmatic premium calculations. The API provides a way to integrate the pricing logic into other applications or services.

### Setting Up the API

When you install the py_pricer package and run the initializer, it automatically creates two API scripts in your working directory:

```bash
# First, initialize the package
python -m py_pricer.initializer

# This creates:
# - run_api.py: Script to run the API server
# - test_api.py: Script to test the API
```

These scripts are designed to work with both development and production environments, with automatic path resolution for resources like sample data.

### Starting the API Server

To start the API server, you can use the console script provided by the package:

```bash
py-pricer-api
```

This will automatically check for a run_api.py script in your current directory, creating one from the template if it doesn't exist, and then run it with default settings.

You can also pass command-line arguments to customize the API server:

```bash
py-pricer-api --host 0.0.0.0 --port 8080 --log-level debug
```

If you prefer, you can also run the API script directly:

```bash
python run_api.py
```

This will start the API server at http://localhost:8000. You can configure the host, port, and other options using command-line arguments. For example:

```bash
python run_api.py --host 127.0.0.1 --port 8000 --reload --log-level debug
```

### Customizing the API

One of the key features of the py_pricer API is that it's designed to be customizable. Since the API scripts are copied to your working directory, you can modify them to suit your specific needs:

- Customize API endpoints
- Add authentication
- Modify request/response models
- Add new features or integrations

The API scripts are designed to continue working correctly with the py_pricer package, using its path resolution capabilities to find the algorithms directory and other resources.

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
2. Initialize the environment using `py-pricer-init` to set up the algorithms folder and API templates
3. Users customize their pricing models by editing files in the `algorithms` folder
4. The Streamlit app (`py-pricer-app`) uses both components to process data and calculate prices
5. The API (`py-pricer-api`) provides programmatic access to the pricing functionality

## License

[License information]

## Troubleshooting

### Common Issues

#### "Command not found" errors with console scripts

If you see `py-pricer-app: command not found`, `py-pricer-api: command not found`, or `py-pricer-init: command not found` when trying to run the console scripts, it might be because:

1. The virtual environment is not activated
2. The package was not installed in development mode
3. Your Python environment's bin directory is not in your PATH

Try running the applications directly:

```bash
# For the Streamlit app (make sure your virtual environment is activated first)
python -c "from py_pricer.app_launcher import launch_app; launch_app()"

# For the API server
python -c "from py_pricer.api_launcher import launch_api; launch_api()"

# For the initializer
python -c "from py_pricer.initializer_launcher import launch_initializer; launch_initializer()"
```

#### API server won't start

If you have issues starting the API server, check the following:

1. Make sure you've activated your virtual environment
2. Ensure the required packages (FastAPI, Uvicorn) are installed
3. Try running with debug logging:
   ```bash
   python run_api.py --log-level debug
   ```

#### Can't find data or algorithms

If the app can't find the data or algorithms directory:

1. Make sure you've run the initializer:
   ```python
   import py_pricer
   py_pricer.initialize()
   ```
2. Check that the algorithms directory exists in your working directory
3. If you're in a development environment, try specifying the path manually
