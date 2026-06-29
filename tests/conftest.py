"""
Shared pytest fixtures for the Books to Scrape automation suite.
Provides browser, page, and page-object fixtures reused across all tests.
"""

import pytest
from playwright.sync_api import Page, sync_playwright

from pages.home_page import HomePage
from pages.book_detail_page import BookDetailPage


# Browser / Page fixtures

@pytest.fixture(scope="session")
def browser_context_args():
    """Override default browser context arguments."""
    return {
        "viewport": {"width": 1280, "height": 800},
        "ignore_https_errors": True,
    }


@pytest.fixture()
def home_page(page: Page) -> HomePage:
    """Return a HomePage instance with the homepage already loaded."""
    hp = HomePage(page)
    hp.load()
    return hp


@pytest.fixture()
def detail_page(page: Page) -> BookDetailPage:
    """Return a BookDetailPage instance (navigation handled per-test)."""
    return BookDetailPage(page)