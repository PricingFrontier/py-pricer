"""
Script to test the FastAPI application.

This script sends a test request to the API and displays the response.
"""

import requests
import json
import argparse
import sys
import os
import random
from pathlib import Path

def get_individual_dir():
    """
    Get the path to the individual directory.
    
    Returns:
        Path to the individual directory
    """
    return os.path.abspath(os.path.join(
        os.path.dirname(__file__), 
        '..', 
        'algorithms', 
        'data', 
        'individual'
    ))

def load_sample_quote(specific_file=None):
    """
    Load a sample quote from the individual directory.
    
    Args:
        specific_file: Specific JSON file to use (filename only, e.g., '1.json')
        
    Returns:
        Dictionary containing quote data
    """
    # Get the path to the individual directory
    individual_dir = get_individual_dir()
    
    if specific_file:
        # Use the specified file
        sample_file = os.path.join(individual_dir, specific_file)
        if not os.path.exists(sample_file):
            raise FileNotFoundError(f"File not found: {sample_file}")
        print(f"Using specified quote file: {sample_file}")
    else:
        # Get all JSON files in the directory
        json_files = list(Path(individual_dir).glob('*.json'))
        
        if not json_files:
            raise FileNotFoundError("No JSON files found in the individual directory")
        
        # Select a random JSON file
        sample_file = random.choice(json_files)
        print(f"Using random quote file: {sample_file}")
    
    # Load the JSON file
    with open(sample_file, 'r') as f:
        return json.load(f)

def test_api(host="127.0.0.1", port=8000, specific_file=None):
    """
    Test the API by sending a sample quote request.
    
    Args:
        host: API host
        port: API port
        specific_file: Specific JSON file to use (filename only, e.g., '1.json')
    """
    # API endpoint
    url = f"http://{host}:{port}/quote"
    
    try:
        # Load a sample quote from the individual directory
        sample_quote = load_sample_quote(specific_file)
        
        # Request payload
        payload = {
            "data": sample_quote
        }
        
        # Send the request
        print(f"Sending request to {url}...")
        response = requests.post(url, json=payload)
        
        # Check if the request was successful
        if response.status_code == 200:
            print("Request successful!")
            print("\nResponse:")
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"Request failed with status code {response.status_code}")
            print("\nError response:")
            print(json.dumps(response.json(), indent=2))
    except FileNotFoundError as e:
        print(f"Error: {str(e)}")
        print("Falling back to hardcoded sample quote...")
        
        # Fallback to hardcoded sample quote
        sample_quote = {
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
        
        # Request payload
        payload = {
            "data": sample_quote
        }
        
        # Send the request
        print(f"Sending request to {url}...")
        response = requests.post(url, json=payload)
        
        # Check if the request was successful
        if response.status_code == 200:
            print("Request successful!")
            print("\nResponse:")
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"Request failed with status code {response.status_code}")
            print("\nError response:")
            print(json.dumps(response.json(), indent=2))
    except Exception as e:
        print(f"Error: {str(e)}")

def list_available_files():
    """
    List all available JSON files in the individual directory.
    """
    individual_dir = get_individual_dir()
    json_files = list(Path(individual_dir).glob('*.json'))
    
    if not json_files:
        print("No JSON files found in the individual directory")
        return
    
    print("\nAvailable JSON files:")
    for file in sorted(json_files):
        print(f"  - {file.name}")

def main():
    """
    Main entry point for the test script.
    """
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Test the Insurance Pricing API")
    parser.add_argument(
        "--host", 
        type=str, 
        default="127.0.0.1", 
        help="API host"
    )
    parser.add_argument(
        "--port", 
        type=int, 
        default=8000, 
        help="API port"
    )
    parser.add_argument(
        "--file",
        type=str,
        help="Specific JSON file to use (filename only, e.g., '1.json')"
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List all available JSON files"
    )
    args = parser.parse_args()
    
    # List available files if requested
    if args.list:
        list_available_files()
        return
    
    # Run the test
    test_api(args.host, args.port, args.file)

if __name__ == "__main__":
    main() 