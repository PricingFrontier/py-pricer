"""
FastAPI API for insurance pricing.

This module provides an API that accepts JSON input and returns premium calculations.
"""

import os
import json
import polars as pl
from typing import Dict, Any, List, Union, Optional
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from py_pricer import transformer, get_data_dir, logger, get_rating_dir
from py_pricer.utils import safe_load_json
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
            return None, None
            
        module_name = "rating_engine"
        spec = importlib.util.spec_from_file_location(module_name, rating_engine_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        logger.info(f"Successfully imported rating engine from {rating_engine_path}")
        return module.apply_base_rating, module.load_base_values
    except Exception as e:
        logger.error(f"Error importing rating engine: {e}", exc_info=True)
        return None, None

# Import the rating engine functions
apply_base_rating, load_base_values = import_rating_engine()

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
        # Convert to DataFrame
        df = pl.DataFrame([quote.dict()])
        
        # Apply category indexing (transformations)
        df, _ = transformer.apply_category_indexing(df)
        
        # Apply base rating
        df, base_values = apply_base_rating(df)
        
        if "BaseValue" not in df.columns:
            raise HTTPException(status_code=500, detail="Failed to calculate base premium")
        
        # In a real application, you would apply more complex rating factors here
        # For now, just use the base value as the premium
        premium = df[0, "BaseValue"]
        
        # Create response
        response = PremiumResponse(
            premium=float(premium),
            quote=quote,
            factors={"base_value": float(premium)}
        )
        
        return response
    
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
        quotes = request.quotes
        if not quotes:
            raise HTTPException(status_code=400, detail="No quotes provided")
            
        # Convert to DataFrame
        df = pl.DataFrame([q.dict() for q in quotes])
        
        # Apply category indexing (transformations)
        df, _ = transformer.apply_category_indexing(df)
        
        # Apply base rating
        df, base_values = apply_base_rating(df)
        
        if "BaseValue" not in df.columns:
            raise HTTPException(status_code=500, detail="Failed to calculate base premiums")
        
        # Create responses
        results = []
        for i, quote in enumerate(quotes):
            premium = df[i, "BaseValue"]
            response = PremiumResponse(
                premium=float(premium),
                quote=quote,
                factors={"base_value": float(premium)}
            )
            results.append(response)
        
        return PremiumResponseBatch(results=results)
    
    except Exception as e:
        logger.error(f"Error calculating premiums in batch: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error calculating premiums: {str(e)}") 