"""
API launcher for the insurance pricing library.

This module provides a command-line entry point for launching the FastAPI server.
"""

import os
import sys
import importlib.util
import uvicorn
import argparse


def main():
    """
    Main entry point for the API launcher.
    
    This function parses command-line arguments and launches the FastAPI server.
    """
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Launch the Insurance Pricing API")
    parser.add_argument(
        "--host", 
        type=str, 
        default="127.0.0.1", 
        help="Host to bind the server to (default: 127.0.0.1)"
    )
    parser.add_argument(
        "--port", 
        type=int, 
        default=8000, 
        help="Port to bind the server to (default: 8000)"
    )
    parser.add_argument(
        "--reload", 
        action="store_true", 
        help="Enable auto-reload for development"
    )
    args = parser.parse_args()
    
    # Get the path to the api.py file
    api_file = os.path.abspath(os.path.join(
        os.path.dirname(__file__), 
        '..', 
        'api', 
        'api.py'
    ))
    
    # Check if the file exists
    if not os.path.exists(api_file):
        print(f"Error: Could not find the API file at {api_file}")
        sys.exit(1)
    
    # Add the project root to the Python path
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    
    # Ensure the logs directory exists
    os.makedirs("logs", exist_ok=True)
    
    # Print startup message
    print(f"Starting Insurance Pricing API on {args.host}:{args.port}...")
    print(f"API documentation will be available at http://{args.host}:{args.port}/docs")
    
    try:
        # Start the server
        uvicorn.run(
            "api.api:app",
            host=args.host,
            port=args.port,
            reload=args.reload,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\nShutting down Insurance Pricing API...")
    except Exception as e:
        print(f"Error launching the API: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main() 