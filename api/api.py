"""
FastAPI application for the insurance pricing library.

This module provides a REST API for processing insurance quotes.
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import logging
import traceback
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import models and utilities
from api.models import QuoteRequest, QuoteResponse, ErrorResponse
from api.utils import process_quote

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(os.path.join('logs', 'api.log'))
    ]
)
logger = logging.getLogger(__name__)

# Create the FastAPI application
app = FastAPI(
    title="Insurance Pricing API",
    description="API for processing insurance quotes and calculating premiums",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Global exception handler for the API.
    
    Args:
        request: The request that caused the exception
        exc: The exception that was raised
        
    Returns:
        JSONResponse with error details
    """
    logger.error(f"Unhandled exception: {str(exc)}")
    logger.error(traceback.format_exc())
    
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="Internal server error",
            details={"message": str(exc)}
        ).dict()
    )

# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint.
    
    Returns:
        Dictionary with status information
    """
    return {"status": "healthy"}

# Quote processing endpoint
@app.post("/quote", response_model=QuoteResponse, tags=["Quotes"])
async def process_quote_request(request: QuoteRequest):
    """
    Process a quote request.
    
    Args:
        request: QuoteRequest object containing quote data
        
    Returns:
        QuoteResponse object with premium details
    """
    try:
        # Process the quote
        result = process_quote(request.data)
        
        # Return the response
        return QuoteResponse(
            quote_id=result["quote_id"],
            premium_details=result["premium_details"]
        )
    except Exception as e:
        logger.error(f"Error processing quote: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=400,
            detail=f"Error processing quote: {str(e)}"
        ) 