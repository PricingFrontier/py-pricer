"""
API package for the insurance pricing application.

This package contains the FastAPI application and related components.
"""

# Import the app directly to avoid circular imports
# We'll import launch_api lazily when needed

__all__ = ['app']

# Import the app after defining __all__ to avoid circular imports
from api.api import app 