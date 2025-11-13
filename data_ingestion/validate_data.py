"""
This module provides functions for validating data quality.
"""

import pandas as pd

def validate_data(data: dict) -> pd.DataFrame:
    """
    Validates the given data and returns a cleaned DataFrame.

    Args:
        data: A dictionary containing the raw data.

    Returns:
        A pandas DataFrame containing the validated data.

    Raises:
        ValueError: If any validation checks fail.
    """
    df = pd.DataFrame(data)

    # Data type checks
    for column in df.columns:
        if df[column].dtype != df[column].infer_objects().dtype:
            raise ValueError(f"Data type mismatch for column: {column}")

    # Missing value checks
    if df.isnull().values.any():
        raise ValueError("Missing values found in the data.")

    # Custom validation rules (e.g., range checks, uniqueness checks)
    # ...

    return df
