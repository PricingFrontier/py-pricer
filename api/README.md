# API Directory

This directory contains the FastAPI application and related components for the py-pricer package.

## Files

- `api.py`: The main FastAPI application that provides the API endpoints for insurance premium calculations.
- `api_launcher.py`: A launcher module that helps run the API server properly.
- `run_api.py`: A script to run the FastAPI application with Uvicorn.
- `test_api.py`: A script to test the API by sending requests to it.

## Usage

To run the API server:

```bash
python api/run_api.py
```

To test the API (make sure the server is running first):

```bash
python api/test_api.py
```

You can also specify a specific JSON file to use for testing:

```bash
python api/test_api.py 5.json
```

Or provide a full path to a JSON file:

```bash
python api/test_api.py path/to/quote.json
``` 