"""
Example transformation module.

This module contains example transformations that can be applied to input data.
"""

import polars as pl
import logging

# Create a module-specific logger
logger = logging.getLogger('transformations.transform')

def age_band(df):
    """
    Create age bands from the DrivAge column.
    
    Args:
        df: Input DataFrame with a DrivAge column
        
    Returns:
        DataFrame with a new DrivAgeBand column
    """
    try:
        if "DrivAge" not in df.columns:
            logger.warning("DrivAge column not found. Cannot create age bands.")
            return df
            
        # Create age bands
        df = df.with_columns(
            pl.when(pl.col("DrivAge") < 25)
            .then(pl.lit("Under 25"))
            .when(pl.col("DrivAge") < 40)
            .then(pl.lit("25-39"))
            .when(pl.col("DrivAge") < 60)
            .then(pl.lit("40-59"))
            .otherwise(pl.lit("60+"))
            .alias("DrivAgeBand")
        )
        
        logger.info(f"Created age bands for {df.height} rows")
        return df
    except Exception as e:
        logger.error(f"Error creating age bands: {e}")
        return df

def power_group(df):
    """
    Create power groups from the VehPower column.
    
    Args:
        df: Input DataFrame with a VehPower column
        
    Returns:
        DataFrame with a new PowerGroup column
    """
    try:
        if "VehPower" not in df.columns:
            logger.warning("VehPower column not found. Cannot create power groups.")
            return df
            
        # Create power groups
        df = df.with_columns(
            pl.when(pl.col("VehPower") < 5)
            .then(pl.lit("Low"))
            .when(pl.col("VehPower") < 8)
            .then(pl.lit("Medium"))
            .otherwise(pl.lit("High"))
            .alias("PowerGroup")
        )
        
        logger.info(f"Created power groups for {df.height} rows")
        return df
    except Exception as e:
        logger.error(f"Error creating power groups: {e}")
        return df

def apply_transformations(df):
    """
    Apply all transformations to the input data.
    
    Args:
        df: Input DataFrame
        
    Returns:
        Transformed DataFrame
    """
    logger.info("Applying transformations...")
    
    # Apply age bands
    df = age_band(df)
    
    # Apply power groups
    df = power_group(df)
    
    logger.info("Transformations completed")
    return df
