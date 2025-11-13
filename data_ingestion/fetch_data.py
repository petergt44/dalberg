"""
This module provides functions for fetching data from various sources.
"""

import requests
import logging
from typing import Optional

logger = logging.getLogger(__name__)

def fetch_data_from_api(url: str, api_key: str, timeout: int = 30) -> Optional[dict]:
    """
    Fetches data from a REST API.

    Args:
        url: The URL of the API endpoint.
        api_key: The API key for authentication.

    Returns:
        A dictionary containing the fetched data.

    Raises:
        requests.exceptions.RequestException: If an error occurs during the API request.
    """
    headers = {"Authorization": f"Bearer {api_key}"}
    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json()
    except requests.exceptions.Timeout:
        logger.error(f"Request timeout for URL: {url}")
        raise
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP error {e.response.status_code} for URL: {url}")
        raise
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching data from API: {e}")
        raise
