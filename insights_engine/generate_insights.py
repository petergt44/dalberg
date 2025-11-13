"""
This module generates actionable insights based on the processed data.
"""

import pandas as pd

def generate_insights(df: pd.DataFrame) -> dict:
    """
    Generates insights from the given DataFrame.

    Args:
        df: The input DataFrame.

    Returns:
        A dictionary containing the generated insights.
    """
    insights = {}
    insights['credit_access'] = calculate_credit_access_metrics(df)
    insights['food_security'] = analyze_agriculture_output(df) 
    insights['women_agency'] = assess_women_inclusion(df) 
    return insights

def calculate_credit_access_metrics(df: pd.DataFrame) -> dict:
    """
    Calculates credit access metrics.

    Args:
        df: The input DataFrame.

    Returns:
        A dictionary containing credit access metrics.
    """
    credit_access_metrics = {
        'credit_approval_rate': (df['credit_approved'] == 1).mean(),
        'average_loan_amount': df[df['credit_approved'] == 1]['loan_amount'].mean()
    }
    return credit_access_metrics

def analyze_agriculture_output(df: pd.DataFrame) -> dict:
    """
    Analyzes agriculture output and food security metrics.

    Args:
        df: The input DataFrame.

    Returns:
        A dictionary containing food security metrics.
    """
    # Check if required columns exist
    if 'agriculture_output' not in df.columns:
        return {'error': 'agriculture_output column not found'}
    
    food_security_metrics = {
        'total_agriculture_output': df['agriculture_output'].sum() if 'agriculture_output' in df.columns else 0,
        'average_output_per_household': df['agriculture_output'].mean() if 'agriculture_output' in df.columns else 0,
        'food_security_score': df['agriculture_output'].mean() / df['agriculture_output'].max() if 'agriculture_output' in df.columns and df['agriculture_output'].max() > 0 else 0
    }
    return food_security_metrics

def assess_women_inclusion(df: pd.DataFrame) -> dict:
    """
    Assesses women's inclusion and agency metrics.

    Args:
        df: The input DataFrame.

    Returns:
        A dictionary containing women's agency metrics.
    """
    # Check if required columns exist
    if 'gender' not in df.columns:
        return {'error': 'gender column not found'}
    
    women_data = df[df['gender'] == 0] if 'gender' in df.columns else pd.DataFrame()
    
    women_agency_metrics = {
        'women_participation_rate': (df['gender'] == 0).mean() if 'gender' in df.columns else 0,
        'women_decision_making_score': women_data['decision_making'].mean() if not women_data.empty and 'decision_making' in women_data.columns else 0,
        'women_leadership_rate': (women_data['is_leader'] == 1).mean() if not women_data.empty and 'is_leader' in women_data.columns else 0
    }
    return women_agency_metrics
