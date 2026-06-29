"""
TC-04: Broken Link Validation
Verifies that all hyperlinks on the homepage return HTTP 200.
"""

import pytest
from pages.home_page import HomePage
from utils.helpers import check_url_status


class TestBrokenLinks:
    """Test suite that checks every anchor link on the homepage for HTTP 200."""

    def test_no_broken_links_on_homepage(self, home_page: HomePage) -> None:
        """
        Collect all unique URLs from the homepage anchor tags,
        send HTTP GET requests, and assert every URL returns status 200.
        """
        urls = home_page.get_all_links()
        assert len(urls) > 0, "No links were found on the homepage"

        broken = []
        for url in urls:
            status = check_url_status(url)
            if status != 200:
                broken.append(f"URL '{url}' returned status {status}")

        assert not broken, (
            f"{len(broken)} broken link(s) found:\n" + "\n".join(broken)
        )