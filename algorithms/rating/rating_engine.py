"""Rating engine for calculating insurance premiums."""

import polars as pl
from algorithms.rating.utils.table_loader import load_and_join_rating_table


def calculate_premium(df: pl.DataFrame) -> pl.DataFrame:
    """
    Calculate insurance premiums based on rating factors.
    
    Args:
        df: Input DataFrame containing policy data
        
    Returns:
        DataFrame with premium calculations added
    """
    # Step 1: Join the Area rating table
    df = load_and_join_rating_table(df, "Area", ["Area"])
    
    # Step 2: Join the VehAge rating table
    df = load_and_join_rating_table(df, "VehAge_rating", ["VehAgeBand"])
    
    # Step 3: Join the VehPower_x_DrivAge rating table
    df = load_and_join_rating_table(df, "VehPower_x_DrivAge", ["VehPowerBand", "DrivAgeBand"])
    
    # Step 4: Calculate the base premium
    df = df.with_columns(
        base_premium=pl.col("Area_base")
    )
    
    # Step 5: Apply the vehicle age factor
    df = df.with_columns(
        premium_after_veh_age=pl.col("base_premium") * pl.col("VehAge_rating")
    )
    
    # Step 6: Apply the vehicle power and driver age factor
    df = df.with_columns(
        final_premium=pl.col("premium_after_veh_age") * pl.col("VehPower_x_DrivAge_rating")
    )
    
    # Round the final premium to 2 decimal places
    df = df.with_columns(
        final_premium=pl.col("final_premium").round(2)
    )
    
    return df


def rate_policies(df: pl.DataFrame) -> pl.DataFrame:
    """
    Main entry point for the rating engine.
    
    Args:
        input_df: Input DataFrame containing policy data
        
    Returns:
        DataFrame with calculated premiums
    """
    
    # Calculate premiums
    rated_df = calculate_premium(df)
    
    # Return the rated DataFrame
    return rated_df
