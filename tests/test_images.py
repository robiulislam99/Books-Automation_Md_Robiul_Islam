"""
TC-05: Product Image Validation
Verifies product images have correct attributes across multiple pages.
"""

import pytest
from pages.home_page import HomePage


class TestProductImages:
    """
    Test suite that validates product images on the homepage
    and across up to 5 pages of pagination.
    """

    MAX_PAGES = 5

    def _validate_images_on_current_page(self, home_page: HomePage, page_num: int) -> list:
        """
        Check all product images on the current page.
        Returns a list of failure messages (empty list means all passed).
        """
        images = home_page.get_product_images()
        failures = []

        for idx, img in enumerate(images):
            label = f"Page {page_num}, Image {idx + 1}"

            if not img.is_visible():
                failures.append(f"{label}: image is not visible")
                continue

            src = img.get_attribute("src") or ""
            alt = img.get_attribute("alt") or ""
            cls = img.get_attribute("class") or ""

            if not src.strip():
                failures.append(f"{label}: 'src' attribute is empty")
            if not alt.strip():
                failures.append(f"{label}: 'alt' attribute is empty")
            if "thumbnail" not in cls:
                failures.append(
                    f"{label}: 'class' does not contain 'thumbnail' (got '{cls}')"
                )

        return failures

    def test_product_images_across_pages(self, home_page: HomePage) -> None:
        """
        Validate product image attributes on the homepage and up to
        MAX_PAGES pages of pagination. All images must be visible and
        have non-empty src, non-empty alt, and class containing 'thumbnail'.
        """
        all_failures = []

        for page_num in range(1, self.MAX_PAGES + 1):
            failures = self._validate_images_on_current_page(home_page, page_num)
            all_failures.extend(failures)

            if not home_page.has_next_page():
                break

            home_page.go_to_next_page()

        assert not all_failures, (
            f"{len(all_failures)} image validation failure(s):\n"
            + "\n".join(all_failures)
        )