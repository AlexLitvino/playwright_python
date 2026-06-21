import json
import logging
import os

import allure
from playwright.sync_api import sync_playwright
import pytest
from pytest import fixture

from helpers.web_service import WebService
from helpers.db import DataBase
from page_objects.application import App
import settings


@pytest.fixture(scope='session', autouse=True)
def preconditions(request):
    logging.info('Preconditions started')

    # copied from get_web_service fixture
    base_url = request.config.getoption('--base-url')
    secure = request.config.getoption('--secure')
    config = load_config(secure)

    yield
    logging.info('Postconditions finished')
    web = WebService(base_url)
    web.login(**config['users']['userRole3'])
    for test in request.node.items:
        if len(test.own_markers) > 0:
            if test.own_markers[0].name == 'test_id':
                if test.result_call.passed:
                    web.report_test(test.own_markers[0].args[0], 'PASS')
                if test.result_call.failed:
                    web.report_test(test.own_markers[0].args[0], 'FAIL')


@pytest.fixture(scope='session')
def get_web_service(request):
    base_url = request.config.getoption('--base-url')
    secure = request.config.getoption('--secure')
    config = load_config(secure)
    web = WebService(base_url)
    web.login(**config["users"]["userRole1"])
    yield web
    web.close()


@pytest.fixture(scope='session')
def get_db(request):
    path = request.config.getini('db_path')
    db = DataBase(path)
    yield db
    db.close()


@fixture(scope='session')
def get_playwright():
    with sync_playwright() as playwright:
        yield playwright


#@fixture(scope='session', params=['chromium', 'firefox', 'webkit'], ids=['chromium', 'firefox', 'webkit'])
@fixture(scope='session', params=['chromium'], ids=['chromium'])
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
    app.login(**config["users"]["userRole1"])
    yield app


@pytest.fixture(scope='session')
def desktop_app_bob(get_browser, request):
    base_url = request.config.getoption('--base-url')
    secure = request.config.getoption('--secure')
    config = load_config(secure)
    app = App(get_browser, base_url=base_url, **settings.BROWSER_OPTIONS)
    app.goto('/login')
    app.login(**config['users']['userRole2'])
    yield app
    app.close()


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
    app.login(**config["users"]["userRole1"])
    yield app


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    result = outcome.get_result()
    # result.when == "setup" >> "call" >> "teardown"
    setattr(item, f'result_{result.when}', result)


@pytest.fixture(scope='function', autouse=True)
def make_screenshots(request):
    yield
    if request.node.result_call.failed:
        for arg in request.node.funcargs.values():
            if isinstance(arg, App):
                allure.attach(body=arg.page.screenshot(),
                              name='screenshot.png',
                              attachment_type=allure.attachment_type.PNG)


def pytest_addoption(parser):
    parser.addoption('--base-url', action='store', default='http://127.0.0.1:8000')
    #parser.addini('base-url', help='base url for site under test', default='http://127.0.0.1:8000')
    parser.addoption('--secure', action='store', default='secure.json')
    parser.addoption('--device', action='store', default='')
    parser.addoption('--browser', help='browser to run', default='chromium')
    parser.addini('headless', help='run browser in headless mode', default='True')
    parser.addini('db_path', help='path to db', default='/home/olytvynov/Projects/HL/Personal/TestMe-TCM/db.sqlite3')


# request.session.fspath.strpath - path to project root
def load_config(file: str) -> dict:
    config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
    with open(config_file) as cfg:
        return json.loads(cfg.read())


# ######################################################################################################################

SLO_MO = None
HEADLESS = False


@pytest.fixture(scope='module')
def chromium():
    """
    Main fixture. Creates Chrome browser and yields it into tests
    Shows how to work with docs
    """
    with sync_playwright() as p:
        chromium = p.chromium.launch(headless=HEADLESS, slow_mo=SLO_MO)
        yield chromium
        chromium.close()


@pytest.fixture(scope='module')
def page(chromium):
    # base url provided for context, so goto method can user only endpoint
    context = chromium.new_context(permissions=["geolocation"],
                                   geolocation={"latitude": 48.8, "longitude": 2.3},
                                   base_url='http://127.0.0.1:8000')
    page = context.new_page()
    yield page
    page.close()
    context.close()


@pytest.fixture(scope='module')
def alice(page):
    page.goto('')
    page.fill('#id_username', 'alice')
    page.fill('id=id_password', 'Qamania123')
    page.click('text="Login"')
    return page
