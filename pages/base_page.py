"""
Base page class providing common browser interaction methods
shared across all page objects.
"""

import logging
from playwright.sync_api import Page, expect

logger = logging.getLogger(__name__)


class BasePage:
    """
    Base class for all page objects.
    Encapsulates shared Playwright interactions and wait strategies.
    """

    BASE_URL = "https://books.toscrape.com"

    def __init__(self, page: Page) -> None:
        self.page = page

    def navigate(self, path: str = "/index.html") -> None:
        """Navigate to a given path relative to the base URL."""
        url = f"{self.BASE_URL}{path}"
        logger.info(f"Navigating to: {url}")
        self.page.goto(url, wait_until="domcontentloaded")

    def get_title(self) -> str:
        """Return the current page title."""
        return self.page.title()

    def get_url(self) -> str:
        """Return the current page URL."""
        return self.page.url

    def go_back(self) -> None:
        """Navigate back to the previous page."""
        logger.info("Navigating back")
        self.page.go_back(wait_until="domcontentloaded")

    def is_visible(self, selector: str) -> bool:
        """Check if an element matching the selector is visible."""
        return self.page.locator(selector).is_visible()