"""
Data validation module for ensuring data quality and integrity.

This module provides functions to validate data quality, check for missing values,
verify data types, and perform custom validation rules.
"""

import logging
from typing import Dict, Any, Optional, List
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)


def validate_data(
    data: Dict[str, Any],
    required_columns: Optional[List[str]] = None,
    allow_missing: bool = False,
    strict_types: bool = True
) -> pd.DataFrame:
    """
    Validate and clean input data, returning a validated DataFrame.

    Performs comprehensive data validation including:
    - Data type consistency checks
    - Missing value detection
    - Required column verification
    - Basic data quality checks

    Args:
        data: Dictionary containing raw data to validate.
        required_columns: Optional list of column names that must be present.
        allow_missing: If True, allows missing values; otherwise raises error.
        strict_types: If True, enforces strict type checking.

    Returns:
        Validated and cleaned pandas DataFrame.

    Raises:
        ValueError: If validation checks fail (missing columns, type mismatches,
                    or missing values when not allowed).
        TypeError: If input data is not a dictionary.

    Example:
        >>> data = {'col1': [1, 2, 3], 'col2': ['a', 'b', 'c']}
        >>> df = validate_data(data, required_columns=['col1', 'col2'])
    """
    if not isinstance(data, dict):
        raise TypeError("Input data must be a dictionary")

    if not data:
        logger.warning("Empty data dictionary provided")
        return pd.DataFrame()

    try:
        df = pd.DataFrame(data)
    except Exception as e:
        logger.error(f"Failed to create DataFrame: {e}")
        raise ValueError(f"Invalid data structure: {e}") from e

    # Check required columns
    if required_columns:
        missing_cols = set(required_columns) - set(df.columns)
        if missing_cols:
            raise ValueError(
                f"Missing required columns: {', '.join(missing_cols)}"
            )

    # Data type checks
    if strict_types:
        for column in df.columns:
            inferred_type = df[column].infer_objects().dtype
            if df[column].dtype != inferred_type:
                logger.warning(
                    f"Type mismatch for column '{column}': "
                    f"expected {inferred_type}, got {df[column].dtype}"
                )
                if strict_types:
                    raise ValueError(
                        f"Data type mismatch for column: {column}"
                    )

    # Missing value checks
    missing_count = df.isnull().sum().sum()
    if missing_count > 0:
        if not allow_missing:
            raise ValueError(
                f"Missing values found in the data. "
                f"Total missing values: {missing_count}"
            )
        logger.warning(f"Found {missing_count} missing values in data")

    # Check for infinite values
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        if np.isinf(df[col]).any():
            logger.warning(f"Infinite values found in column: {col}")
            df[col] = df[col].replace([np.inf, -np.inf], np.nan)

    logger.info(f"Successfully validated data with {len(df)} rows and {len(df.columns)} columns")
    return df
