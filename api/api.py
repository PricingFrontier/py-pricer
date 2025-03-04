"""
FastAPI API for insurance pricing.

This module provides an API that accepts JSON input and returns premium calculations.
"""

import os
import logging
from typing import Dict, Any, List, Union, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

# Import the rating engine directly
from algorithms.rating.rating_engine import process_single_quote

# Create a module-specific logger
logger = logging.getLogger('py_pricer.api')

# Define pydantic models for request and response
class InsuranceQuote(BaseModel):
    IDpol: Optional[int] = None
    Exposure: float = Field(..., description="Exposure period in years")
    VehPower: int = Field(..., description="Vehicle power")
    VehAge: int = Field(..., description="Vehicle age in years")
    DrivAge: int = Field(..., description="Driver age in years")
    BonusMalus: int = Field(..., description="Bonus-Malus score (typically 50-350)")
    VehBrand: str = Field(..., description="Vehicle brand code")
    VehGas: str = Field(..., description="Fuel type (Regular/Diesel)")
    Area: str = Field(..., description="Area code")
    Density: float = Field(..., description="Population density")
    Region: str = Field(..., description="Geographic region")
    
    class Config:
        schema_extra = {
            "example": {
                "IDpol": 1,
                "Exposure": 0.1,
                "VehPower": 5,
                "VehAge": 0,
                "DrivAge": 55,
                "BonusMalus": 50,
                "VehBrand": "B12",
                "VehGas": "Regular",
                "Area": "D",
                "Density": 1217,
                "Region": "Rhone-Alpes"
            }
        }

class PremiumResponse(BaseModel):
    premium: float
    quote: InsuranceQuote
    factors: Dict[str, float] = Field(default_factory=dict)

# Removed InsuranceQuoteBatch and PremiumResponseBatch classes

# Create the FastAPI application
app = FastAPI(
    title="Insurance Premium API",
    description="API for calculating insurance premiums based on policy data",
    version="1.0.0"
)

@app.get("/")
async def root():
    return {"message": "Insurance Premium API is running"}

@app.post("/calculate_premium", response_model=PremiumResponse)
async def calculate_premium(quote: InsuranceQuote):
    """
    Calculate premium for a single insurance quote.
    
    This endpoint accepts a JSON object representing an insurance quote and returns the calculated premium.
    """
    try:
        # Process the quote using the rating engine
        result = process_single_quote(quote.dict())
        
        # Create response
        response = PremiumResponse(
            premium=result["premium"],
            quote=quote,
            factors=result["factors"]
        )
        
        return response
    
    except ValueError as e:
        logger.error(f"Error calculating premium: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error calculating premium: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error calculating premium: {str(e)}") 