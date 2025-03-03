#!/usr/bin/env python
"""
Script to run the FastAPI application with Uvicorn.
"""

import uvicorn
import logging
import argparse
from py_pricer.logging_config import setup_logging

def main():
    parser = argparse.ArgumentParser(description="Run the Insurance Premium API")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host to bind the server to")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind the server to")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload")
    parser.add_argument("--log-level", type=str, default="info", 
                        choices=["debug", "info", "warning", "error", "critical"],
                        help="Logging level")
    
    args = parser.parse_args()
    
    # Set up logging
    setup_logging()
    
    # Configure Uvicorn server
    uvicorn_config = {
        "app": "py_pricer.api:app",
        "host": args.host,
        "port": args.port,
        "reload": args.reload,
        "log_level": args.log_level,
    }
    
    # Run the server
    uvicorn.run(**uvicorn_config)

if __name__ == "__main__":
    main() 