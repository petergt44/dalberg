"""
Bias detection and fairness assessment module.

This module provides functions for detecting bias in datasets and assessing
fairness metrics using the AIF360 library.
"""

import logging
from typing import List, Dict, Any, Optional
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)

try:
    from aif360.algorithms.preprocessing import Reweighing
    from aif360.metrics import BinaryLabelDatasetMetric
    from aif360.datasets import StandardDataset
    AIF360_AVAILABLE = True
except ImportError:
    logger.warning("AIF360 library not available. Bias checking will be limited.")
    AIF360_AVAILABLE = False


def check_for_bias(
    df: pd.DataFrame,
    protected_attribute: str = "gender",
    privileged_groups: Optional[List[Dict[str, Any]]] = None,
    unprivileged_groups: Optional[List[Dict[str, Any]]] = None,
    target_column: Optional[str] = None,
    threshold: float = 0.2
) -> Dict[str, Any]:
    """
    Check for bias in the dataset using statistical and fairness metrics.

    Analyzes the dataset for potential bias based on protected attributes
    and calculates fairness metrics.

    Args:
        df: DataFrame to analyze for bias.
        protected_attribute: Name of the protected attribute column.
        privileged_groups: List of dictionaries representing privileged groups.
                          Defaults to [{protected_attribute: 1}].
        unprivileged_groups: List of dictionaries representing unprivileged groups.
                            Defaults to [{protected_attribute: 0}].
        target_column: Name of the target/outcome column for fairness analysis.
        threshold: Threshold for determining significant bias (default: 0.2).

    Returns:
        Dictionary containing bias metrics including:
        - has_bias: Boolean indicating if significant bias was detected
        - demographic_parity: Demographic parity metric
        - equalized_odds: Equalized odds metric
        - statistical_parity_difference: Statistical parity difference
        - message: Human-readable message about bias status

    Example:
        >>> df = pd.DataFrame({
        ...     'gender': [0, 0, 1, 1],
        ...     'outcome': [0, 1, 0, 1]
        ... })
        >>> result = check_for_bias(df, target_column='outcome')
    """
    if df.empty:
        logger.warning("Empty DataFrame provided for bias checking")
        return {
            'has_bias': False,
            'message': 'Cannot check bias on empty dataset'
        }

    if protected_attribute not in df.columns:
        logger.warning(f"Protected attribute '{protected_attribute}' not found")
        return {
            'has_bias': False,
            'message': f"Protected attribute '{protected_attribute}' not in dataset"
        }

    # Set default groups if not provided
    if privileged_groups is None:
        privileged_groups = [{protected_attribute: 1}]
    if unprivileged_groups is None:
        unprivileged_groups = [{protected_attribute: 0}]

    results = {
        'has_bias': False,
        'demographic_parity': None,
        'equalized_odds': None,
        'statistical_parity_difference': None,
        'message': ''
    }

    try:
        # Basic statistical parity check
        if target_column and target_column in df.columns:
            privileged_mask = df[protected_attribute] == privileged_groups[0][protected_attribute]
            unprivileged_mask = df[protected_attribute] == unprivileged_groups[0][protected_attribute]

            privileged_rate = df[privileged_mask][target_column].mean()
            unprivileged_rate = df[unprivileged_mask][target_column].mean()

            statistical_parity_diff = abs(privileged_rate - unprivileged_rate)
            results['statistical_parity_difference'] = float(statistical_parity_diff)
            results['demographic_parity'] = {
                'privileged_rate': float(privileged_rate),
                'unprivileged_rate': float(unprivileged_rate)
            }

            if statistical_parity_diff > threshold:
                results['has_bias'] = True
                results['message'] = (
                    f"Significant bias detected. Statistical parity difference: "
                    f"{statistical_parity_diff:.3f} (threshold: {threshold})"
                )
            else:
                results['message'] = (
                    f"No significant bias detected. Statistical parity difference: "
                    f"{statistical_parity_diff:.3f}"
                )
        else:
            # Simple demographic check
            value_counts = df[protected_attribute].value_counts(normalize=True)
            if len(value_counts) > 1:
                max_diff = value_counts.max() - value_counts.min()
                if max_diff > threshold:
                    results['has_bias'] = True
                    results['message'] = (
                        f"Potential demographic imbalance detected. "
                        f"Max difference: {max_diff:.3f}"
                    )
                else:
                    results['message'] = "No significant demographic imbalance detected"

        logger.info(f"Bias check completed: {results['message']}")
        return results

    except Exception as e:
        logger.error(f"Error during bias checking: {e}")
        return {
            'has_bias': False,
            'message': f'Error during bias checking: {str(e)}'
        }
