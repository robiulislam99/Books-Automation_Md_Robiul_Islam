"""
TC-02: Random Book Navigation Validation
Verifies that clicking randomly selected books opens the correct detail page.
"""

import pytest
from pages.home_page import HomePage, BookSummary
from pages.book_detail_page import BookDetailPage


class TestBookNavigation:
    """Test suite validating navigation from homepage to book detail pages."""

    SAMPLE_SIZE = 5

    def test_random_book_navigation(
        self, home_page: HomePage, detail_page: BookDetailPage
    ) -> None:
        """
        Randomly select books, navigate to each detail page, and verify:
        - The detail page loads successfully.
        - The H1 title matches the title shown on the homepage.
        - The book information table is visible.
        """
        selected_books = home_page.select_random_books(self.SAMPLE_SIZE)
        assert len(selected_books) == self.SAMPLE_SIZE, (
            f"Expected {self.SAMPLE_SIZE} books but only found {len(selected_books)}"
        )

        for book in selected_books:
            # Navigate to the detail page
            home_page.click_book_by_index(book.element_index)

            # Validate detail page H1 matches homepage title
            detail_title = detail_page.get_h1_title()
            assert detail_title == book.title, (
                f"Title mismatch — Homepage: '{book.title}', "
                f"Detail page H1: '{detail_title}'"
            )

            # Validate book information section is present
            assert detail_page.book_info_is_visible(), (
                f"Book info table not visible for book: '{book.title}'"
            )

            # Return to homepage for the next iteration
            home_page.go_back()
            home_page.page.wait_for_load_state("domcontentloaded")