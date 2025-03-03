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

## Installation

```bash
# Install UV if not already installed
pip install uv

# Create and activate a virtual environment
uv venv
# Activate the environment (varies by platform)

# Install the library
uv pip install py-pricer
```

## Getting Started

1. Initialize the project structure with examples:
   ```bash
   python -m py_pricer.initializer
   ```

2. Run the Streamlit app to see the example in action:
   ```bash
   python -m py_pricer.app
   ```

3. Customize the pricing model by editing files in the `algorithms` folder:
   - `algorithms/data/input/`: Replace with your own quote data
   - `algorithms/rating_tables/`: Modify rating tables for your pricing factors
   - `algorithms/transformations/`: Customize data transformation logic
   - `algorithms/rating/`: Implement your specific rating algorithms

## Project Structure

```
py-pricer/
├── py_pricer/                  # LIBRARY CODE (DO NOT MODIFY)
│   ├── __init__.py
│   ├── initializer.py          # Creates the algorithms folder with examples
│   ├── data_processor.py       # Data loading and processing
│   ├── transformer.py          # Transformation framework
│   ├── rating_engine.py        # Rating calculation engine
│   └── app.py                  # Streamlit application
├── algorithms/                 # USER-EDITABLE CONTENT
│   ├── data/                   # Your data files
│   │   └── input/              # Raw input data (JSON/parquet)
│   ├── rating_tables/          # Your rating tables
│   ├── transformations/        # Your transformation logic
│   └── rating/                 # Your rating algorithms
```

## Workflow

1. The library code (`py_pricer`) provides the infrastructure and remains unchanged
2. Users customize their pricing models by editing files in the `algorithms` folder
3. The Streamlit app uses both components to process data and calculate prices

## License

[License information]
