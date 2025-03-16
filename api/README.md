# Insurance Pricing API

This API provides endpoints for processing insurance quotes and calculating premiums.

## Overview

The API is built using FastAPI and follows a RESTful design. It processes insurance quote data through the same transformation pipeline and rating engine used by the Streamlit application.

## Endpoints

### Health Check

```
GET /health
```

Returns the health status of the API.

### Process Quote

```
POST /quote
```

Processes a quote through the transformation pipeline and rating engine, returning the calculated premium details.

#### Request Format

```json
{
  "data": {
    "IDpol": 1,
    "VehPower": 5,
    "VehAge": 2,
    "DrivAge": 30,
    "BonusMalus": 50,
    "VehBrand": "B1",
    "VehGas": "Regular",
    "Area": "A",
    "Density": 800,
    "Region": "R1"
  }
}
```

#### Response Format

```json
{
  "quote_id": "1",
  "premium_details": {
    "base_premium": 200,
    "premium_after_veh_age": 260,
    "final_premium": 312
  }
}
```

## Running the API

To run the API server:

```bash
python -m api.run_api
```

Optional arguments:
- `--host`: Host to bind the server to (default: 127.0.0.1)
- `--port`: Port to bind the server to (default: 8000)
- `--reload`: Enable auto-reload for development

## Testing the API

To test the API with a sample quote:

```bash
python -m api.test_api
```

Optional arguments:
- `--host`: API host (default: 127.0.0.1)
- `--port`: API port (default: 8000)

## API Documentation

When the API is running, you can access the auto-generated documentation at:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Error Handling

The API returns appropriate HTTP status codes and error messages:

- 200: Successful request
- 400: Bad request (e.g., invalid data format)
- 500: Internal server error

Error responses include an error message and optional details. 