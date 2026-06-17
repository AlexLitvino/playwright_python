import json
import os

from playwright.sync_api import sync_playwright
from pytest import fixture

from page_objects.application import App
import settings


@fixture(scope='session')
def get_playwright():
    with sync_playwright() as playwright:
        yield playwright


@fixture(scope='session')
def desktop_app(get_playwright, request):
    #app = App(get_playwright, base_url=settings.BASE_URL)
    base_url = request.config.getoption('--base-url')
    #base_url = request.config.getini('base-url')
    #app = App(get_playwright, base_url=base_url)
    app = App(get_playwright, base_url=base_url, **settings.BROWSER_OPTIONS)
    app.goto('/')
    yield app
    app.close()


@fixture(scope='session')
def desktop_app_auth(desktop_app, request):
    secure = request.config.getoption('--secure')
    config = load_config(secure)
    app = desktop_app
    app.goto('/login')
    #app.login('alice', 'Qamania123')
    #app.login(**settings.USER)
    app.login(**config)
    yield app


def pytest_addoption(parser):
    parser.addoption('--base-url', action='store', default='http://127.0.0.1:8000')
    #parser.addini('base-url', help='base url for site under test', default='http://127.0.0.1:8000')
    parser.addoption('--secure', action='store', default='secure.json')


# request.session.fspath.strpath - path to project root
def load_config(file: str) -> dict:
    config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
    with open(config_file) as cfg:
        return json.loads(cfg.read())