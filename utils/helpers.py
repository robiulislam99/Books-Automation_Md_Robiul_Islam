"""
Utility helper functions used across the test suite.
"""

import logging
import requests

logger = logging.getLogger(__name__)


def check_url_status(url: str, timeout: int = 10) -> int:
    """
    Send an HTTP GET request to a URL and return the status code.

    Args:
        url: The URL to check.
        timeout: Request timeout in seconds.

    Returns:
        The HTTP status code, or 0 if the request fails entirely.
    """
    try:
        response = requests.get(url, timeout=timeout, allow_redirects=True)
        logger.info(f"URL {url} returned status {response.status_code}")
        return response.status_code
    except requests.RequestException as exc:
        logger.warning(f"Request failed for {url}: {exc}")
        return 0