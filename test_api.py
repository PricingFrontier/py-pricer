#!/usr/bin/env python
"""
Test script to demonstrate how to call the Insurance Premium API.
"""

import requests
import json
import sys
import os
from pathlib import Path

API_URL = "http://localhost:8000"

def test_single_quote():
    """Test calculating a premium for a single quote using a JSON file from algorithms/data."""
    
    # Find the first JSON file in the data directory
    data_dir = Path("algorithms/data")
    json_files = list(data_dir.glob("*.json"))
    
    if not json_files:
        print("No JSON files found in the data directory")
        return
    
    # Load the first JSON file
    first_json_file = json_files[0]
    try:
        with open(first_json_file, 'r') as f:
            quote = json.load(f)
    except Exception as e:
        print(f"Error loading {first_json_file}: {e}")
        return
    
    print(f"Using quote data from: {first_json_file}")
    
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

def test_batch_quotes():
    """Test calculating premiums for multiple quotes in a batch using all JSON files."""
    
    # Load sample data from the project
    json_files = []
    data_dir = Path("algorithms/data")
    
    # Find all JSON files in the data directory
    for file_path in data_dir.glob("*.json"):
        json_files.append(file_path)
    
    if not json_files:
        print("No JSON files found in the data directory")
        return
    
    print(f"Found {len(json_files)} JSON files to test in batch")
    
    # Load quotes from JSON files - use all available JSON files
    quotes = []
    for file_path in json_files:  # No limit on the number of files
        try:
            with open(file_path, 'r') as f:
                quote = json.load(f)
                quotes.append(quote)
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
    
    # Call the API
    response = requests.post(f"{API_URL}/calculate_premiums_batch", json={"quotes": quotes})
    
    # Check the response
    if response.status_code == 200:
        result = response.json()
        print("Batch Quote Test:")
        print(f"Number of results: {len(result['results'])}")
        for i, item in enumerate(result['results']):
            print(f"Quote {i+1} - Premium: {item['premium']}, Factors: {item['factors']}")
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
    
    # Run the tests
    test_single_quote()
    test_batch_quotes()

if __name__ == "__main__":
    main() 