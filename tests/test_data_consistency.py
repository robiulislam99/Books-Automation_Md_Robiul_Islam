"""
TC-03: Book Data Consistency Validation
Verifies that title and price shown on the homepage match the detail page.
"""

import pytest
from pages.home_page import HomePage
from pages.book_detail_page import BookDetailPage


class TestDataConsistency:
    """Test suite for data consistency between homepage and detail pages."""

    SAMPLE_SIZE = 5

    def test_title_and_price_consistency(
        self, home_page: HomePage, detail_page: BookDetailPage
    ) -> None:
        """
        For each of 5 randomly selected books, verify that:
        - The title on the homepage matches the title on the detail page.
        - The price on the homepage matches the price on the detail page.
        """
        selected_books = home_page.select_random_books(self.SAMPLE_SIZE)
        mismatches = []

        for book in selected_books:
            home_page.click_book_by_index(book.element_index)

            detail_title = detail_page.get_h1_title()
            detail_price = detail_page.get_price()

            if detail_title != book.title:
                mismatches.append(
                    f"TITLE mismatch for '{book.title}': "
                    f"detail page shows '{detail_title}'"
                )

            if detail_price != book.price:
                mismatches.append(
                    f"PRICE mismatch for '{book.title}': "
                    f"homepage shows '{book.price}', "
                    f"detail page shows '{detail_price}'"
                )

            home_page.go_back()
            home_page.page.wait_for_load_state("domcontentloaded")

        assert not mismatches, (
            f"Data consistency failures found:\n" + "\n".join(mismatches)
        )