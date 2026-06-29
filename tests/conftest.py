"""
Shared pytest fixtures for the Books to Scrape automation suite.
Provides browser, page, and page-object fixtures with
screenshot/video capture, trace recording, and Allure attachment.
"""

import os
import shutil
import time
import pytest
import allure
from playwright.sync_api import Page

from pages.home_page import HomePage
from pages.book_detail_page import BookDetailPage

# Output directories
SCREENSHOTS_DIR = "screenshots"
VIDEOS_DIR      = "videos"
TRACES_DIR      = "traces"

os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
os.makedirs(VIDEOS_DIR, exist_ok=True)
os.makedirs(TRACES_DIR, exist_ok=True)


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
    1. Starts Playwright trace recording before the test.
    2. Takes a screenshot after the test body finishes.
    3. Stops and saves the trace file.
    4. Closes the browser context so Playwright finalises the video file.
    5. Attaches screenshot, video, and trace to Allure report.
    """

    test_name = _safe_name(request.node.name)

    # 1. Start trace recording
    try:
        context.tracing.start(
            screenshots=True,
            snapshots=True,
            sources=True,
        )
    except Exception as exc:
        allure.attach(
            f"Could not start trace: {exc}",
            name="Trace start error",
            attachment_type=allure.attachment_type.TEXT,
        )

    yield  # test runs here

    # 2. Screenshot (before context closes)
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

    # 3. Stop trace and save
    trace_path = os.path.join(TRACES_DIR, f"{test_name}.zip")
    try:
        context.tracing.stop(path=trace_path)
        if os.path.exists(trace_path) and os.path.getsize(trace_path) > 0:
            with open(trace_path, "rb") as f:
                allure.attach(
                    f.read(),
                    name=f"Trace – {test_name}",
                    attachment_type="application/zip",
                    extension=".zip",
                )
    except Exception as exc:
        allure.attach(
            f"Could not save trace: {exc}",
            name="Trace error",
            attachment_type=allure.attachment_type.TEXT,
        )

    # 4. Save video path BEFORE closing context
    video_src = None
    try:
        if page.video:
            video_src = page.video.path()
    except Exception:
        pass

    # 5. Close context → Playwright finalises the .webm file
    try:
        context.close()
    except Exception:
        pass

    # 6. Attach video AFTER context is closed
    if video_src:
        try:
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