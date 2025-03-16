"""Utility function for loading rating tables from CSV files."""

import os
import polars as pl
from typing import List, Optional


def load_and_join_rating_table(
    df: pl.DataFrame,
    table_name: str,
    join_columns: List[str],
    tables_dir: Optional[str] = None
) -> pl.DataFrame:
    """
    Load a rating table from CSV and join it to the input dataframe.
    
    Args:
        df: Input Polars DataFrame to join the rating table to
        table_name: Name of the table file without the .csv extension
        join_columns: List of column names to join on
        tables_dir: Directory containing the rating tables. If None, defaults to 
                   algorithms/rating/tables
    
    Returns:
        Polars DataFrame with the rating table joined
    """
    if tables_dir is None:
        # Default to the standard tables directory
        tables_dir = os.path.join("algorithms", "rating", "tables")
    
    # Ensure the table name has the .csv extension
    if not table_name.endswith(".csv"):
        table_name = f"{table_name}.csv"
    
    file_path = os.path.join(tables_dir, table_name)
    
    # Load the CSV file into a Polars DataFrame
    rating_table = pl.read_csv(file_path)
    
    # Join the rating table to the input dataframe
    return df.join(rating_table, on=join_columns) 