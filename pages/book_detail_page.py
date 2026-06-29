"""
Page Object for the Book Detail page.
Handles all interactions and data extraction from individual book pages.
"""

import logging
from playwright.sync_api import Page

from pages.base_page import BasePage

logger = logging.getLogger(__name__)


class BookDetailPage(BasePage):
    """
    Page Object for an individual book's detail page.
    Validates and extracts data from a single book's page.
    """

    # Selectors
    H1_TITLE = "h1"
    BOOK_INFO_TABLE = "table.table-striped"
    PRICE = "p.price_color"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def get_h1_title(self) -> str:
        """Return the text content of the H1 heading on the detail page."""
        title = self.page.locator(self.H1_TITLE).inner_text().strip()
        logger.info(f"Detail page H1 title: '{title}'")
        return title

    def get_price(self) -> str:
        """Return the price text from the detail page."""
        price = self.page.locator(self.PRICE).first.inner_text().strip()
        logger.info(f"Detail page price: '{price}'")
        return price

    def book_info_is_visible(self) -> bool:
        """Return True if the book information table is visible."""
        return self.is_visible(self.BOOK_INFO_TABLE)