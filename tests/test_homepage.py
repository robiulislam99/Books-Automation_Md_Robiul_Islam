"""
TC-01: Homepage Validation
Verifies that the homepage loads correctly and displays expected content.
"""

import pytest
from pages.home_page import HomePage


class TestHomepageValidation:
    """Test suite for homepage structural and content validation."""

    EXPECTED_URL = "https://books.toscrape.com/index.html"
    EXPECTED_TITLE_FRAGMENT = "Books to Scrape"

    def test_page_url_is_correct(self, home_page: HomePage) -> None:
        """Verify the loaded URL matches the expected homepage URL."""
        actual_url = home_page.get_url()
        assert actual_url == self.EXPECTED_URL, (
            f"Expected URL '{self.EXPECTED_URL}', got '{actual_url}'"
        )

    def test_page_title_contains_expected_text(self, home_page: HomePage) -> None:
        """Verify the page title contains the expected site name."""
        actual_title = home_page.get_title()
        assert self.EXPECTED_TITLE_FRAGMENT in actual_title, (
            f"Expected title to contain '{self.EXPECTED_TITLE_FRAGMENT}', "
            f"got '{actual_title}'"
        )

    def test_all_visible_headings_are_present(self, home_page: HomePage) -> None:
        """Verify that at least one head# ---------------------------------------------------------------------------ing exists on the homepage."""
        headings = home_page.get_all_headings()
        assert len(headings) > 0, "No visible headings found on the homepage"

    def test_all_heading_texts_are_non_empty(self, home_page: HomePage) -> None:
        """Verify that every visible heading contains non-empty text."""
        headings = home_page.get_all_headings()
        for text in headings:
            assert text.strip() != "", f"Found a heading with empty text: '{text}'"

    def test_books_section_is_visible(self, home_page: HomePage) -> None:
        """Verify the books section container is rendered on the page."""
        assert home_page.books_section_is_visible(), (
            "Books section is not visible on the homepage"
        )

    def test_books_section_contains_at_least_one_book(self, home_page: HomePage) -> None:
        """Verify the homepage lists at least one book."""
        count = home_page.book_count()
        assert count > 0, "No book items found on the homepage"