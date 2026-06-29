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


# Screenshot + video attachment on every test 

@pytest.fixture(autouse=True)
def attach_artifacts(request, page: Page):
    """
    Autouse fixture that:
    - Takes a screenshot after every test and attaches it to Allure.
    - Attaches the recorded video to Allure after the test finishes.
    Runs for every test automatically.
    """
    yield  # test runs here

    test_name = request.node.name.replace(" ", "_").replace("[", "_").replace("]", "_")

    # Screenshot 
    screenshot_path = os.path.join(SCREENSHOTS_DIR, f"{test_name}.png")
    try:
        page.screenshot(path=screenshot_path, full_page=True)
        with open(screenshot_path, "rb") as f:
            allure.attach(
                f.read(),
                name=f"Screenshot – {test_name}",
                attachment_type=allure.attachment_type.PNG,
            )
    except Exception as exc:
        allure.attach(
            f"Could not capture screenshot: {exc}",
            name="Screenshot error",
            attachment_type=allure.attachment_type.TEXT,
        )

    # Video
    try:
        page.context.close()          # finalises the video file
        video_path = page.video.path()
        if video_path and os.path.exists(video_path):
            # Rename to a meaningful name
            named_video = os.path.join(VIDEOS_DIR, f"{test_name}.webm")
            os.replace(video_path, named_video)
            with open(named_video, "rb") as f:
                allure.attach(
                    f.read(),
                    name=f"Video – {test_name}",
                    attachment_type=allure.attachment_type.WEBM,
                )
    except Exception as exc:
        allure.attach(
            f"Could not attach video: {exc}",
            name="Video error",
            attachment_type=allure.attachment_type.TEXT,
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