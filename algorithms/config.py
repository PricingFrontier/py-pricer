"""
Project configuration for the insurance pricing library.

This module contains configuration settings that are used across the project.
"""

# Data configuration
DATA_CONFIG = {
    # Primary identifier field used as index in pandas DataFrames for display
    "primary_id": "IDpol"
}

def get_primary_id():
    """
    Get the primary ID field name from the configuration.
    
    Returns:
        String containing the primary ID field name
    """
    return DATA_CONFIG["primary_id"] 