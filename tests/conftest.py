"""
Shared pytest fixtures for the Books to Scrape automation suite.
Provides browser, page, and page-object fixtures with
screenshot/video capture and Allure attachment.
"""

import os
import pytest
import allure
from playwright.sync_api import Page

from pages.home_page import HomePage
from pages.book_detail_page import BookDetailPage

# Output directories 
SCREENSHOTS_DIR = "screenshots"
VIDEOS_DIR      = "videos"

os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
os.makedirs(VIDEOS_DIR, exist_ok=True)


# Browser context: enable video recording

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """
    Override default browser context to enable video recording
    and set a consistent viewport.
    """
    return {
        **browser_context_args,
        "viewport"           : {"width": 1280, "height": 800},
        "ignore_https_errors": True,
        "record_video_dir"   : VIDEOS_DIR,
        "record_video_size"  : {"width": 1280, "height": 800},
    }


# Screenshot capture

@pytest.fixture(autouse=True)
def attach_screenshot(request, page: Page):
    """
    Autouse fixture that takes a full-page screenshot after every test
    and attaches it to the Allure report.
    """
    yield  # test runs here

    test_name = _safe_name(request.node.name)
    screenshot_path = os.path.join(SCREENSHOTS_DIR, f"{test_name}.png")

    try:
        page.screenshot(path=screenshot_path, full_page=True)
        allure.attach.file(
            screenshot_path,
            name=f"Screenshot – {test_name}",
            attachment_type=allure.attachment_type.PNG,
        )
    except Exception as exc:
        allure.attach(
            f"Could not capture screenshot: {exc}",
            name="Screenshot error",
            attachment_type=allure.attachment_type.TEXT,
        )


# Video capture 

@pytest.fixture(autouse=True)
def attach_video(request, page: Page):
    """
    Autouse fixture that waits for the video file to be finalised
    after the browser context closes, then attaches it to Allure.
    Video is only available after the context is fully closed —
    this fixture hooks into the teardown phase to handle that correctly.
    """
    yield  # test runs here

    test_name = _safe_name(request.node.name)

    def _attach():
        try:
            video = page.video
            if video is None:
                return
            video_src = video.path()
            if not video_src or not os.path.exists(video_src):
                return
            named_video = os.path.join(VIDEOS_DIR, f"{test_name}.webm")
            os.replace(video_src, named_video)
            allure.attach.file(
                named_video,
                name=f"Video – {test_name}",
                attachment_type=allure.attachment_type.WEBM,
            )
        except Exception as exc:
            allure.attach(
                f"Could not attach video: {exc}",
                name="Video error",
                attachment_type=allure.attachment_type.TEXT,
            )

    # Register the video attachment to run after context closes
    request.addfinalizer(_attach)


# Helper

def _safe_name(name: str) -> str:
    """Sanitise test name for use as a filename."""
    return (
        name.replace(" ", "_")
            .replace("[", "_")
            .replace("]", "_")
            .replace("/", "_")
    )


# Page object fixtures

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