"""
FastAPI API for insurance pricing.

This module provides an API that accepts JSON input and returns premium calculations.
"""

import os
import logging
from typing import Dict, Any, List, Union, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from py_pricer import get_rating_dir
import importlib.util

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

class InsuranceQuoteBatch(BaseModel):
    quotes: List[InsuranceQuote]

class PremiumResponseBatch(BaseModel):
    results: List[PremiumResponse]

# Dynamically import the rating_engine module
def import_rating_engine():
    try:
        rating_dir = get_rating_dir()
        rating_engine_path = os.path.join(rating_dir, "rating_engine.py")
        
        if not os.path.exists(rating_engine_path):
            logger.error(f"Rating engine not found at: {rating_engine_path}")
            return None
            
        module_name = "rating_engine"
        spec = importlib.util.spec_from_file_location(module_name, rating_engine_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        logger.info(f"Successfully imported rating engine from {rating_engine_path}")
        return module
    except Exception as e:
        logger.error(f"Error importing rating engine: {e}", exc_info=True)
        return None

# Import the rating_engine module
rating_engine = import_rating_engine()

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
        if rating_engine is None:
            raise HTTPException(status_code=500, detail="Rating engine not available")
        
        # Process the quote using the rating engine
        result = rating_engine.process_single_quote(quote.dict())
        
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

@app.post("/calculate_premiums_batch", response_model=PremiumResponseBatch)
async def calculate_premiums_batch(request: InsuranceQuoteBatch):
    """
    Calculate premiums for multiple insurance quotes in a batch.
    
    This endpoint accepts a list of insurance quotes and returns a list of calculated premiums.
    """
    try:
        if rating_engine is None:
            raise HTTPException(status_code=500, detail="Rating engine not available")
        
        quotes = request.quotes
        if not quotes:
            raise HTTPException(status_code=400, detail="No quotes provided")
        
        # Process the quotes using the rating engine
        results_data = rating_engine.process_batch_quotes([q.dict() for q in quotes])
        
        # Create responses
        results = []
        for i, quote in enumerate(quotes):
            response = PremiumResponse(
                premium=results_data[i]["premium"],
                quote=quote,
                factors=results_data[i]["factors"]
            )
            results.append(response)
        
        return PremiumResponseBatch(results=results)
    
    except ValueError as e:
        logger.error(f"Error calculating premiums: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error calculating premiums in batch: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error calculating premiums: {str(e)}") 