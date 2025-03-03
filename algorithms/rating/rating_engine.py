"""
Simple rating engine for insurance pricing.

This module loads base values from a CSV file and applies them to input data.
"""

import os
import polars as pl
import logging

# Create a module-specific logger
logger = logging.getLogger('py_pricer.rating_engine')

def load_base_values():
    """
    Load base values from the CSV file in the tables directory.
    
    Returns:
        A DataFrame containing the base values or None if loading fails
    """
    try:
        # Path to the base values CSV file
        base_values_path = os.path.join(os.path.dirname(__file__), "tables", "base-values.csv")
        
        # Check if the file exists
        if not os.path.exists(base_values_path):
            logger.error(f"Base values file not found at: {base_values_path}")
            return None
        
        # Load the CSV file
        df = pl.read_csv(base_values_path)
        logger.info(f"Successfully loaded base values from {base_values_path}")
        logger.info(f"Base values loaded: {df.height} rows")
        
        return df
    except Exception as e:
        logger.error(f"Error loading base values: {e}")
        return None

def apply_base_rating(df):
    """
    Apply base values to the input data based on the Area column.
    
    Args:
        df: Input DataFrame with an 'Area' column
        
    Returns:
        - DataFrame with base values applied as a new 'BaseValue' column
        - Base values table or None if loading fails
    """
    try:
        # Check if the Area column exists
        if "Area" not in df.columns:
            logger.warning("Area column not found in input data. Cannot apply base rating.")
            return df, None
        
        # Load base values
        base_values_df = load_base_values()
        if base_values_df is None:
            logger.warning("Failed to load base values. Skipping base rating.")
            return df, None
        
        # Convert base values to lists for the replace method
        area_values = base_values_df["Area"].to_list()
        base_values = base_values_df["Base"].to_list()
        
        # Create a new column with the base value
        result_df = df.with_columns(
            pl.col("Area").replace(area_values, base_values).alias("BaseValue")
        )
        
        logger.info(f"Applied base values to {df.height} rows")
        return result_df, base_values_df
    except Exception as e:
        logger.error(f"Error applying base rating: {e}")
        return df, None

def calculate_premium(df):
    """
    Calculate the final premium based on base values and other factors.
    
    Args:
        df: Input DataFrame with a 'BaseValue' column
        
    Returns:
        DataFrame with a new 'Premium' column
    """
    try:
        # Check if the BaseValue column exists
        if "BaseValue" not in df.columns:
            logger.warning("BaseValue column not found. Cannot calculate premium.")
            return df
        
        # Apply a simple factor based on PowerGroup if it exists
        if "PowerGroup" in df.columns:
            power_factors = {
                "Low": 0.8,
                "Medium": 1.0,
                "High": 1.2
            }
            
            # Get the unique values of PowerGroup
            power_groups = df["PowerGroup"].unique().to_list()
            
            # Create factors list matching the power_groups list
            factors = [power_factors.get(pg, 1.0) for pg in power_groups]
            
            # Apply the power group factor
            df = df.with_columns(
                (pl.col("BaseValue") * pl.col("PowerGroup").replace(power_groups, factors)).alias("Premium")
            )
        else:
            # No PowerGroup, just use the base value as the premium
            df = df.with_columns(
                pl.col("BaseValue").alias("Premium")
            )
        
        logger.info(f"Calculated premiums for {df.height} rows")
        return df
    except Exception as e:
        logger.error(f"Error calculating premium: {e}")
        return df
