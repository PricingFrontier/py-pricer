"""
Rating module for the insurance pricing library.

This module provides standardized functions for calculating premiums based on quote data.
"""

import logging
import polars as pl
from typing import Dict, Any, List, Tuple

# Create a module-specific logger
logger = logging.getLogger('py_pricer.rating')

def _extract_premium_and_factors(df: pl.DataFrame, row_index: int) -> Tuple[float, Dict[str, float]]:
    """
    Extract premium and factors from a DataFrame row.
    
    Args:
        df: DataFrame with calculated premiums
        row_index: Index of the row to extract from
        
    Returns:
        Tuple of (premium, factors_dict)
    """
    # Use Premium column if available, otherwise use BaseValue
    if "Premium" in df.columns:
        premium = float(df[row_index, "Premium"])
    else:
        premium = float(df[row_index, "BaseValue"])
    
    # Collect all factors used in the calculation
    factors = {"base_value": float(df[row_index, "BaseValue"])}
    
    # Add any additional factors that might be in the DataFrame
    # For example, if there are columns that end with "Factor", include them
    for col in df.columns:
        if col.endswith("Factor") and col in df.columns:
            factors[col] = float(df[row_index, col])
    
    return premium, factors

def process_single_quote(process_quotes_func, quote_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Process a single insurance quote and calculate the premium.
    
    Args:
        process_quotes_func: Function that processes quotes (from the rating engine)
        quote_data: Dictionary containing the quote data
        
    Returns:
        Dictionary with premium and factors information
        
    Raises:
        ValueError: If premium calculation fails
    """
    try:
        # Process the quote using the provided function
        df = process_quotes_func([quote_data])
        
        # Extract the premium and factors
        premium, factors = _extract_premium_and_factors(df, 0)
        
        return {
            "premium": premium,
            "factors": factors
        }
    
    except Exception as e:
        logger.error(f"Error processing quote: {e}", exc_info=True)
        # Simplify error handling by just raising the original exception with context
        raise ValueError(f"Error calculating premium: {str(e)}") 