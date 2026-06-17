from playwright.sync_api import sync_playwright
from pytest import fixture

from page_objects.application import App


@fixture
def get_playwright():
    with sync_playwright() as playwright:
        yield playwright


@fixture
def desktop_app(get_playwright):
    app = App(get_playwright, base_url='http://127.0.0.1:8000')
    app.goto('/')
    yield app
    app.close()


@fixture
def desktop_app_auth(desktop_app):
    app = desktop_app
    app.goto('/login')
    app.login('alice', 'Qamania123')
    yield app
