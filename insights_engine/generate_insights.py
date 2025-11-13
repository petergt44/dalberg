"""
Insights generation module for creating actionable insights from processed data.

This module provides functions to analyze data and generate insights related to
credit access, food security, and women's agency metrics.
"""

import logging
from typing import Dict, Any, Optional
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)


def generate_insights(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Generate comprehensive insights from processed DataFrame.

    Analyzes the dataset and generates insights across multiple domains:
    - Credit access metrics
    - Food security indicators
    - Women's agency and inclusion metrics

    Args:
        df: Input DataFrame containing processed data.

    Returns:
        Dictionary containing insights for each domain with the following keys:
        - credit_access: Credit access metrics
        - food_security: Food security analysis
        - women_agency: Women's inclusion metrics

    Raises:
        ValueError: If DataFrame is empty or invalid.

    Example:
        >>> df = pd.DataFrame({
        ...     'credit_approved': [1, 0, 1],
        ...     'loan_amount': [1000, 0, 2000]
        ... })
        >>> insights = generate_insights(df)
    """
    if df.empty:
        logger.warning("Empty DataFrame provided for insights generation")
        raise ValueError("Cannot generate insights from empty DataFrame")

    if not isinstance(df, pd.DataFrame):
        raise TypeError("Input must be a pandas DataFrame")

    logger.info(f"Generating insights from DataFrame with {len(df)} rows")
    insights = {
        'credit_access': calculate_credit_access_metrics(df),
        'food_security': analyze_agriculture_output(df),
        'women_agency': assess_women_inclusion(df)
    }
    logger.info("Insights generation completed successfully")
    return insights

def calculate_credit_access_metrics(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Calculate credit access metrics from the dataset.

    Computes various metrics related to credit access including approval rates,
    average loan amounts, and credit distribution statistics.

    Args:
        df: DataFrame containing credit-related data with columns:
            - credit_approved: Binary indicator (1=approved, 0=rejected)
            - loan_amount: Amount of loan requested/approved

    Returns:
        Dictionary containing credit access metrics:
        - credit_approval_rate: Percentage of approved applications
        - average_loan_amount: Mean loan amount for approved applications
        - total_applications: Total number of credit applications
        - total_approved: Number of approved applications
        - rejection_rate: Percentage of rejected applications

    Example:
        >>> df = pd.DataFrame({
        ...     'credit_approved': [1, 0, 1, 1],
        ...     'loan_amount': [1000, 0, 2000, 1500]
        ... })
        >>> metrics = calculate_credit_access_metrics(df)
    """
    if 'credit_approved' not in df.columns:
        logger.warning("'credit_approved' column not found")
        return {'error': 'credit_approved column not found'}

    if 'loan_amount' not in df.columns:
        logger.warning("'loan_amount' column not found")
        return {'error': 'loan_amount column not found'}

    total_applications = len(df)
    approved_mask = df['credit_approved'] == 1
    approved_count = approved_mask.sum()
    rejected_count = total_applications - approved_count

    approved_loans = df[approved_mask]['loan_amount']
    average_loan = float(approved_loans.mean()) if approved_count > 0 else 0.0

    metrics = {
        'credit_approval_rate': float(approved_count / total_applications) if total_applications > 0 else 0.0,
        'average_loan_amount': average_loan,
        'total_applications': int(total_applications),
        'total_approved': int(approved_count),
        'total_rejected': int(rejected_count),
        'rejection_rate': float(rejected_count / total_applications) if total_applications > 0 else 0.0
    }

    logger.info(f"Credit access metrics calculated: {approved_count}/{total_applications} approved")
    return metrics

def analyze_agriculture_output(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Analyze agriculture output and food security metrics.

    Computes metrics related to agricultural productivity and food security
    indicators from the dataset.

    Args:
        df: DataFrame containing agriculture-related data with column:
            - agriculture_output: Agricultural output values

    Returns:
        Dictionary containing food security metrics:
        - total_agriculture_output: Sum of all agriculture output
        - average_output_per_household: Mean agriculture output
        - food_security_score: Normalized food security score (0-1)
        - median_output: Median agriculture output
        - output_std: Standard deviation of output

    Example:
        >>> df = pd.DataFrame({'agriculture_output': [100, 200, 150, 180]})
        >>> metrics = analyze_agriculture_output(df)
    """
    if 'agriculture_output' not in df.columns:
        logger.warning("'agriculture_output' column not found")
        return {'error': 'agriculture_output column not found'}

    output_col = df['agriculture_output']
    total_output = float(output_col.sum())
    mean_output = float(output_col.mean())
    median_output = float(output_col.median())
    std_output = float(output_col.std())
    max_output = float(output_col.max())

    # Calculate normalized food security score
    food_security_score = (
        mean_output / max_output if max_output > 0 else 0.0
    )

    metrics = {
        'total_agriculture_output': total_output,
        'average_output_per_household': mean_output,
        'median_output_per_household': median_output,
        'output_std': std_output,
        'food_security_score': food_security_score,
        'household_count': int(len(df))
    }

    logger.info(f"Agriculture analysis completed: {len(df)} households analyzed")
    return metrics


def assess_women_inclusion(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Assess women's inclusion and agency metrics in the dataset.

    Analyzes gender distribution and women's participation across various
    indicators including decision-making and leadership roles.

    Args:
        df: DataFrame containing gender and participation data with columns:
            - gender: Gender indicator (0=women, 1=men, or similar encoding)
            - decision_making: Optional decision-making score
            - is_leader: Optional leadership indicator

    Returns:
        Dictionary containing women's agency metrics:
        - women_participation_rate: Proportion of women in dataset
        - women_decision_making_score: Average decision-making score for women
        - women_leadership_rate: Proportion of women in leadership roles
        - total_women: Total number of women in dataset
        - total_participants: Total number of participants

    Example:
        >>> df = pd.DataFrame({
        ...     'gender': [0, 0, 1, 1],
        ...     'decision_making': [5, 4, 3, 2],
        ...     'is_leader': [1, 0, 1, 0]
        ... })
        >>> metrics = assess_women_inclusion(df)
    """
    if 'gender' not in df.columns:
        logger.warning("'gender' column not found")
        return {'error': 'gender column not found'}

    total_participants = len(df)
    women_mask = df['gender'] == 0
    women_data = df[women_mask]
    women_count = women_mask.sum()
    men_count = total_participants - women_count

    women_participation_rate = (
        float(women_count / total_participants) if total_participants > 0 else 0.0
    )

    metrics = {
        'women_participation_rate': women_participation_rate,
        'total_women': int(women_count),
        'total_men': int(men_count),
        'total_participants': int(total_participants),
        'gender_balance_score': (
            1.0 - abs(women_participation_rate - 0.5) * 2
        )  # Score closer to 1 = more balanced
    }

    # Add optional metrics if columns exist
    if not women_data.empty:
        if 'decision_making' in women_data.columns:
            metrics['women_decision_making_score'] = float(
                women_data['decision_making'].mean()
            )

        if 'is_leader' in women_data.columns:
            leader_count = (women_data['is_leader'] == 1).sum()
            metrics['women_leadership_rate'] = (
                float(leader_count / women_count) if women_count > 0 else 0.0
            )
            metrics['women_leaders_count'] = int(leader_count)

    logger.info(
        f"Women inclusion assessment: {women_count}/{total_participants} women "
        f"({women_participation_rate:.1%})"
    )
    return metrics
