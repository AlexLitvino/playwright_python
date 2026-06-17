from playwright.sync_api import Playwright, sync_playwright
from pytest import fixture

from page_objects.application import App


@fixture
def get_playwright():
    with sync_playwright() as playwright:
        yield playwright


@fixture
def desktop_app(get_playwright):
    app = App(get_playwright)
    yield app
    app.close()
