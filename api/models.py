"""
Pydantic models for the API.

This module defines the data models used for API requests and responses.
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class QuoteRequest(BaseModel):
    """
    Model for a quote request.
    
    This is a flexible model that can accept any JSON data structure.
    The validation is minimal to allow for different data formats.
    """
    data: Dict[str, Any] = Field(
        ..., 
        description="Quote data in JSON format"
    )


class QuoteResponse(BaseModel):
    """
    Model for a quote response.
    
    This contains the original data plus the calculated premium fields.
    """
    quote_id: Optional[str] = Field(
        None, 
        description="Identifier for the quote"
    )
    premium_details: Dict[str, Any] = Field(
        ..., 
        description="Premium calculation details"
    )
    
    
class ErrorResponse(BaseModel):
    """
    Model for error responses.
    """
    error: str = Field(
        ..., 
        description="Error message"
    )
    details: Optional[Dict[str, Any]] = Field(
        None, 
        description="Additional error details"
    ) 