"""
Utility helper functions used across the test suite.
"""

import logging
import time
import urllib3
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Suppress the InsecureRequestWarning for the sandbox site
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logger = logging.getLogger(__name__)

# Delay between each HTTP request to avoid overwhelming the server
REQUEST_DELAY_SECONDS = 0.5

# Retry configuration: retry up to 3 times on connection errors
RETRY_STRATEGY = Retry(
    total=3,
    backoff_factor=1,          # waits 1s, 2s, 4s between retries
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["GET"],
)


def _build_session() -> requests.Session:
    """
    Build a requests Session with retry strategy and a browser-like User-Agent.
    This prevents the server from identifying and blocking automated requests.
    """
    session = requests.Session()
    adapter = HTTPAdapter(max_retries=RETRY_STRATEGY)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    session.headers.update({
        "User-Agent": (
            "Mozilla/5.0 (X11; Linux x86_64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    })
    return session


def check_url_status(url: str, timeout: int = 15) -> int:
    """
    Send an HTTP GET request to a URL and return the status code.
    Includes retry logic and a small delay to avoid rate limiting.

    Args:
        url: The URL to check.
        timeout: Request timeout in seconds.

    Returns:
        The HTTP status code, or 0 if the request fails entirely.
    """
    time.sleep(REQUEST_DELAY_SECONDS)

    session = _build_session()
    try:
        response = session.get(url, timeout=timeout, allow_redirects=True, verify=False)
        logger.info(f"URL {url} returned status {response.status_code}")
        return response.status_code
    except requests.RequestException as exc:
        logger.warning(f"Request failed for {url}: {exc}")
        return 0
    finally:
        session.close()