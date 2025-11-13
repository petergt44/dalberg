"""
Data transformation and preprocessing module.

This module provides functions for cleaning, transforming, and preprocessing
data to prepare it for analysis or machine learning.
"""

import logging
from typing import Optional, List, Dict, Any
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)


def preprocess_data(
    df: pd.DataFrame,
    handle_missing: str = 'ffill',
    date_columns: Optional[List[str]] = None,
    numeric_columns: Optional[List[str]] = None,
    drop_duplicates: bool = True
) -> pd.DataFrame:
    """
    Preprocess DataFrame by handling missing values and performing transformations.

    Performs data cleaning operations including:
    - Missing value imputation
    - Date column conversion
    - Duplicate removal
    - Data type optimization

    Args:
        df: Input DataFrame to preprocess.
        handle_missing: Strategy for handling missing values.
                       Options: 'ffill' (forward fill), 'bfill' (backward fill),
                       'mean' (numeric mean), 'median' (numeric median),
                       'drop' (remove rows with missing values).
        date_columns: Optional list of column names to convert to datetime.
        numeric_columns: Optional list of column names to ensure are numeric.
        drop_duplicates: If True, removes duplicate rows.

    Returns:
        Preprocessed DataFrame.

    Raises:
        ValueError: If handle_missing strategy is invalid.
        TypeError: If input is not a DataFrame.

    Example:
        >>> df = pd.DataFrame({'date': ['2023-01-01', '2023-01-02'],
        ...                     'value': [1, None]})
        >>> processed = preprocess_data(df, date_columns=['date'])
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Input must be a pandas DataFrame")

    if df.empty:
        logger.warning("Empty DataFrame provided")
        return df

    df = df.copy()  # Avoid modifying original DataFrame

    # Handle missing values
    if handle_missing == 'ffill':
        df = df.ffill()
    elif handle_missing == 'bfill':
        df = df.bfill()
    elif handle_missing == 'mean':
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
    elif handle_missing == 'median':
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
    elif handle_missing == 'drop':
        df = df.dropna()
    else:
        raise ValueError(
            f"Invalid handle_missing strategy: {handle_missing}. "
            f"Choose from: 'ffill', 'bfill', 'mean', 'median', 'drop'"
        )

    # Convert date columns
    if date_columns:
        for col in date_columns:
            if col in df.columns:
                try:
                    df[col] = pd.to_datetime(df[col], errors='coerce')
                    logger.info(f"Converted column '{col}' to datetime")
                except Exception as e:
                    logger.warning(f"Failed to convert '{col}' to datetime: {e}")

    # Ensure numeric columns are numeric
    if numeric_columns:
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')

    # Remove duplicates
    if drop_duplicates:
        initial_len = len(df)
        df = df.drop_duplicates()
        removed = initial_len - len(df)
        if removed > 0:
            logger.info(f"Removed {removed} duplicate rows")

    logger.info(f"Preprocessing complete. Final shape: {df.shape}")
    return df
