#!/usr/bin/env python
"""
Test script to demonstrate how to call the Insurance Premium API.

Usage:
    python test_api.py                    # Uses algorithms/data/1.json by default
    python test_api.py 5.json             # Uses algorithms/data/5.json
    python test_api.py path/to/quote.json # Uses a specific JSON file path
"""

import requests
import json
import sys
import os
from pathlib import Path

API_URL = "http://localhost:8000"

def test_single_quote(json_file_path=None):
    """Test calculating a premium for a single quote using a JSON file from algorithms/data.
    
    Args:
        json_file_path: Optional path to a specific JSON file to use. If not provided,
                        will use algorithms/data/1.json by default.
    """
    
    # Determine which JSON file to use
    if json_file_path is None:
        # Default to 1.json
        json_file_path = Path("algorithms/data/1.json")
    else:
        # If only a filename was provided, assume it's in algorithms/data
        json_file_path = Path(json_file_path)
        if not json_file_path.is_absolute() and "/" not in str(json_file_path):
            json_file_path = Path("algorithms/data") / json_file_path
    
    # Check if the file exists
    if not json_file_path.exists():
        print(f"Error: JSON file '{json_file_path}' not found.")
        print("Available JSON files in algorithms/data:")
        data_dir = Path("algorithms/data")
        if data_dir.exists():
            for file in data_dir.glob("*.json"):
                print(f"  - {file.name}")
        return
    
    # Load the JSON file
    try:
        with open(json_file_path, 'r') as f:
            quote = json.load(f)
    except Exception as e:
        print(f"Error loading {json_file_path}: {e}")
        return
    
    print(f"Using quote data from: {json_file_path}")
    
    # Call the API
    response = requests.post(f"{API_URL}/calculate_premium", json=quote)
    
    # Check the response
    if response.status_code == 200:
        result = response.json()
        print("Single Quote Test:")
        print(f"Premium: {result['premium']}")
        print(f"Factors: {result['factors']}")
        print()
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        print()

def main():
    """Run the API tests."""
    print(f"Testing Insurance Premium API at {API_URL}")
    print("-" * 50)
    
    # Check if the API is running
    try:
        response = requests.get(f"{API_URL}/")
        if response.status_code != 200:
            print(f"API is not running correctly. Response: {response.status_code}")
            return
    except requests.exceptions.ConnectionError:
        print(f"Error: Could not connect to API at {API_URL}")
        print("Make sure the API is running with 'python run_api.py'")
        return
    
    # Get the JSON file path from command line arguments if provided
    json_file_path = None
    if len(sys.argv) > 1:
        json_file_path = sys.argv[1]
    
    # Run the test with the specified or default JSON file
    test_single_quote(json_file_path)

if __name__ == "__main__":
    main() 