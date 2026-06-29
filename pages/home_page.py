"""
Page Object for the Books to Scrape homepage.
Handles all interactions and data extraction from the homepage.
"""

import logging
import random
from dataclasses import dataclass
from typing import List
from playwright.sync_api import Page

from pages.base_page import BasePage

logger = logging.getLogger(__name__)


@dataclass
class BookSummary:
    """Represents a book as shown on the homepage listing."""
    title: str
    price: str
    element_index: int


class HomePage(BasePage):
    """
    Page Object for the homepage (catalogue listing).
    Provides methods to inspect and interact with the book catalogue.
    """

    # Selectors
    BOOK_ITEMS = "article.product_pod"
    BOOK_TITLE = "h3 > a"
    BOOK_PRICE = "p.price_color"
    NEXT_BUTTON = "li.next > a"
    HEADINGS = "h1, h2, h3, h4, h5, h6"
    BOOKS_SECTION = "section"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def load(self) -> None:
        """Navigate to the homepage."""
        self.navigate("/index.html")

    def get_all_headings(self) -> List[str]:
        """Return a list of text content from all visible headings on the page."""
        headings = self.page.locator(self.HEADINGS).all()
        texts = []
        for h in headings:
            if h.is_visible():
                text = h.inner_text().strip()
                texts.append(text)
        logger.info(f"Found {len(texts)} visible headings")
        return texts

    def get_all_books(self) -> List[BookSummary]:
        """Return a list of BookSummary objects for every book on the current page."""
        books = []
        items = self.page.locator(self.BOOK_ITEMS).all()
        for idx, item in enumerate(items):
            title_el = item.locator(self.BOOK_TITLE)
            price_el = item.locator(self.BOOK_PRICE)
            # The full title is stored in the 'title' attribute of the <a> tag
            title = title_el.get_attribute("title") or title_el.inner_text().strip()
            price = price_el.inner_text().strip()
            books.append(BookSummary(title=title, price=price, element_index=idx))
        logger.info(f"Collected {len(books)} books from current page")
        return books

    def select_random_books(self, count: int = 5) -> List[BookSummary]:
        """Return a random sample of books from the current page."""
        all_books = self.get_all_books()
        sample = random.sample(all_books, min(count, len(all_books)))
        logger.info(f"Randomly selected {len(sample)} books")
        return sample

    def click_book_by_index(self, index: int) -> None:
        """Click a book article element by its position index on the page."""
        logger.info(f"Clicking book at index {index}")
        book = self.page.locator(self.BOOK_ITEMS).nth(index)
        book.locator(self.BOOK_TITLE).click()
        self.page.wait_for_load_state("domcontentloaded")

    def books_section_is_visible(self) -> bool:
        """Check whether the books section container is visible."""
        return self.is_visible(self.BOOKS_SECTION)

    def book_count(self) -> int:
        """Return the number of book items currently visible on the page."""
        return self.page.locator(self.BOOK_ITEMS).count()

    def has_next_page(self) -> bool:
        """Return True if a Next pagination button exists."""
        return self.page.locator(self.NEXT_BUTTON).count() > 0

    def go_to_next_page(self) -> None:
        """Click the Next button to load the next page of books."""
        logger.info("Clicking Next page button")
        self.page.locator(self.NEXT_BUTTON).click()
        self.page.wait_for_load_state("domcontentloaded")

    def get_all_links(self) -> List[str]:
        """Collect all unique href values from anchor tags on the homepage."""
        anchors = self.page.locator("a").all()
        hrefs = set()
        for anchor in anchors:
            href = anchor.get_attribute("href")
            if href and href.strip() and not href.startswith("#"):
                # Resolve relative URLs
                if href.startswith("http"):
                    hrefs.add(href)
                else:
                    hrefs.add(f"{self.BASE_URL}/{href.lstrip('/')}")
        logger.info(f"Collected {len(hrefs)} unique links")
        return list(hrefs)

    def get_product_images(self):
        """Return all product image locators on the current page."""
        return self.page.locator("article.product_pod img").all()