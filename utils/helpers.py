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
REQUEST_DELAY_SECONDS = 1.5

# Retry configuration
RETRY_STRATEGY = Retry(
    total=5,
    backoff_factor=2,          # waits 2s, 4s, 8s, 16s between retries
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["GET"],
    raise_on_status=False,
)


def _build_session() -> requests.Session:
    """
    Build a requests Session with retry strategy and a browser-like User-Agent.
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
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
    })
    return session


def check_url_status(url: str, timeout: int = 15) -> int:
    """
    Send an HTTP GET request to a URL and return the status code.
    Retries up to 3 times on ConnectionResetError before giving up.

    Args:
        url: The URL to check.
        timeout: Request timeout in seconds.

    Returns:
        The HTTP status code, or 0 if all attempts fail.
    """
    time.sleep(REQUEST_DELAY_SECONDS)

    session = _build_session()
    max_attempts = 3

    for attempt in range(1, max_attempts + 1):
        try:
            response = session.get(url, timeout=timeout, allow_redirects=True, verify=False)
            logger.info(f"URL {url} returned status {response.status_code}")
            return response.status_code
        except requests.exceptions.ConnectionError as exc:
            logger.warning(f"Attempt {attempt}/{max_attempts} - Connection error for {url}: {exc}")
            if attempt < max_attempts:
                wait = attempt * 3      # 3s, 6s, 9s
                logger.info(f"Retrying in {wait}s...")
                time.sleep(wait)
        except requests.RequestException as exc:
            logger.warning(f"Request failed for {url}: {exc}")
            break
        finally:
            session.close()

    logger.error(f"All attempts failed for {url}")
    return 0