import json
import os

from playwright.sync_api import sync_playwright
import pytest
from pytest import fixture

from page_objects.application import App
import settings


@fixture(scope='session')
def get_playwright():
    with sync_playwright() as playwright:
        yield playwright


@fixture(scope='session', params=['chromium', 'firefox', 'webkit'], ids=['chromium', 'firefox', 'webkit'])
def get_browser(get_playwright, request):
    #browser = request.config.getoption('--browser')
    browser = request.param
    os.environ['PWBROWSER'] = browser
    headless = request.config.getini('headless')
    if headless == 'True':
        headless = True
    else:
        headless = False

    if browser == 'chromium':
        bro = get_playwright.chromium.launch(headless=headless)
    elif browser == 'firefox':
        bro = get_playwright.firefox.launch(headless=headless)
    elif browser == 'webkit':
        bro = get_playwright.webkit.launch(headless=headless)
    else:
        assert False, 'Unsupported browser type'
    yield bro
    bro.close()
    del os.environ['PWBROWSER']



@fixture(scope='session')
def desktop_app(get_playwright, get_browser, request):
    #app = App(get_playwright, base_url=settings.BASE_URL)
    base_url = request.config.getoption('--base-url')
    #base_url = request.config.getini('base-url')
    #app = App(get_playwright, base_url=base_url)
    app = App(get_browser, base_url=base_url, **settings.BROWSER_OPTIONS)
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


@fixture(scope='session', params=['iPhone 11', 'Pixel 2'])
def mobile_app(get_playwright, get_browser, request):
    if os.environ.get('PWBROWSER') == 'firefox':
        pytest.skip('FireFox is not supported for Mobile')

    base_url = request.config.getoption('--base-url')
    #device = request.config.getoption('--device')
    device = request.param

    device_config = get_playwright.devices.get(device)
    if device_config is not None:
        device_config.update(settings.BROWSER_OPTIONS)
    else:
        device_config = settings.BROWSER_OPTIONS

    app = App(get_browser, base_url=base_url, **device_config)
    app.goto('/')
    yield app
    app.close()


@fixture(scope='session')
def mobile_app_auth(mobile_app, request):
    secure = request.config.getoption('--secure')
    config = load_config(secure)
    app = mobile_app
    app.goto('/login')
    app.login(**config)
    yield app


def pytest_addoption(parser):
    parser.addoption('--base-url', action='store', default='http://127.0.0.1:8000')
    #parser.addini('base-url', help='base url for site under test', default='http://127.0.0.1:8000')
    parser.addoption('--secure', action='store', default='secure.json')
    parser.addoption('--device', action='store', default='')
    parser.addoption('--browser', help='browser to run', default='chromium')
    parser.addini('headless', help='run browser in headless mode', default='True')


# request.session.fspath.strpath - path to project root
def load_config(file: str) -> dict:
    config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
    with open(config_file) as cfg:
        return json.loads(cfg.read())