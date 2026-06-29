"""
Shared pytest fixtures for the Books to Scrape automation suite.
Provides browser, page, and page-object fixtures with
screenshot/video capture and Allure attachment.
"""

import os
import shutil
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


# Main artifact fixture

@pytest.fixture(autouse=True)
def attach_artifacts(request, page: Page, context):
    """
    Autouse fixture that:
    1. Takes a screenshot after the test body finishes.
    2. Closes the browser context so Playwright finalises the video file.
    3. Attaches the fully written video file to Allure.

    Using `context` fixture directly lets us close it at the right time
    without conflicting with pytest-playwright's internal teardown.
    """
    yield  # test runs here

    test_name = _safe_name(request.node.name)

    # 1. Screenshot (before context closes)
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

    # 2. Save video path BEFORE closing context
    video_src = None
    try:
        if page.video:
            video_src = page.video.path()
    except Exception:
        pass

    # 3. Close context → Playwright finalises the .webm file
    try:
        context.close()
    except Exception:
        pass

    # 4. Attach video AFTER context is closed
    if video_src:
        try:
            # Wait briefly for file to be fully written
            import time
            time.sleep(1)

            if os.path.exists(video_src) and os.path.getsize(video_src) > 0:
                named_video = os.path.join(VIDEOS_DIR, f"{test_name}.webm")
                shutil.copy2(video_src, named_video)
                allure.attach.file(
                    named_video,
                    name=f"Video – {test_name}",
                    attachment_type=allure.attachment_type.WEBM,
                )
            else:
                allure.attach(
                    f"Video file empty or missing: {video_src}",
                    name="Video error",
                    attachment_type=allure.attachment_type.TEXT,
                )
        except Exception as exc:
            allure.attach(
                f"Could not attach video: {exc}",
                name="Video error",
                attachment_type=allure.attachment_type.TEXT,
            )


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