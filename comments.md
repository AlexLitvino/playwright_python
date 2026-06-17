https://www.youtube.com/watch?v=024tZHVFiLA&list=PLGE9K4YL_ywj4F7cSA4oDptnqTmyS7hZp  
https://github.com/Ypurek/playwright-automation  
https://github.com/Ypurek/Playwright-Python-Cool-Features/tree/master  
https://github.com/Ypurek/Playwright-pytest-2023    Project with Testomat.io integration  
2 hours, 26 minutes, 12 seconds  


# Playwright Python: 00 Intro

Why Playwright
- Fast
- Modern
- Brand new
- Can intercept web requests

What do you get?
- Cross platform course (Windows 10, Ubuntu 20.04, MacOS)
- Guide how to setup environment and create 1st test
- Intro to pytest
- Creating test project template
- Writing UI test
- Usage REST API and DB in tests
- Setup test report with Allure
- Introducing test to CI/CD with Jenkins
- Review typical issues of test automation

What you don't get?
- Python basics (https://www.python.org/about/gettingstarted/)
- No detailed tool comparison


# Playwright Python: 01 Basic Tools
What we need?
- Browser (based on Chromium or FireFox)
- Python
```shell
sudo apt install python3
```
- PIP
```shell
sudo apt install python3-pip
```
- PyCharm
- Git


# Playwright Python: 03 Pycharm Project
Create PyCharm project  
Install pytest: using UI or command line  
Create simple test  
Run test using terminal  
Run test using PyCharm UI  
Debugging tests in PyCharm  


# Playwright Python: 03.1 asserts
Assert with comments  
Code after failed assert doesn't run  


# Playwright Python: 04 Test Me
https://github.com/Ypurek/TestMe-TCM    test app  
Clone repo  
Install dependencies  
```shell
pip install -r requirements.txt
```
Start project
```shell
python3 manage.py runserver
```
Navigate http://localhost:8000/  
Login: alice  
Password: Qamania123  


# Playwright Python: 05 Record playback
Install playwright:
```shell
pip install playwright
pip show playwright
```

Install browser drivers
```shell
python playwright install
```
On version 1.60.0, need to run
```shell
playwright install
```

First test case
Steps:
- Open site
- Login with user = alice, password = Qamania123
- Open new test page
- Set test name = hello, test description = world
- Click button create
- Navigate to test cases page
Expected result:
- Test case hello is displayed
Post conditions:
- Delete test case hello

Start playwright in record mode
```shell
playwright codegen http://127.0.0.1:8000
```
Click all steps. 
Code will appear in separate inspector window.
Copy code, paste it into python module and after that close browser.
Run function.

To made test, create test function in the same module and move there
```python
def test_new_testcase():
    with sync_playwright() as playwright:
        run(playwright)
```

Test might fail due to geo location blocking. Add
https://playwright.dev/python/docs/emulation#geolocation
```python
    context = browser.new_context(
        geolocation={"longitude": 41.890221, "latitude": 12.492348},
        permissions=["geolocation"]
    )
```


# Playwright Python: 06 Playwright structure
During testing could be ONE instance of Playwright that could start up to 3 browser per time.  
If you need more, you should use Context (it's like Incognito mode) - for example to log in with different users to application.

Playwright code could be synchronous and asynchronous.


# Playwright Python: 07 Selectors
Set environment variable
PWDEBUG=1

Start browser with opened DevTools (works only with Chromium?)
```python
browser = playwright.chromium.launch(headless=False, devtools=True)
```
Start test in debug mode.

Selectors:
- XPath
  - w3schools.com/xml/xpath_syntax.asp
  - devhints.io/xpath
- CSS
  - w3schools.com/cssref/css_selectors.asp
  - devhints.io/css
- TEXT
- ID
- Custom
https://playwright.dev/docs/locators
https://playwright.dev/docs/selectors

In DevTools console write: playwright.$('xpath=//tr') and Enter.
playwright.$('css=.PASS')
playwright.$('text=Check pass test') - will search by partial match if without quotes
playwright.$('text=\"\Alice"') - full match if with quotes
Quotes could be escaped by \ or by another type of quotes

Selectors chain (combining using >>)
playwright.$('xpath=//table >> css=tr >> css=.PASS')

To find parent need mark with * what we want to find:
playwright.$('xpath=//table >> *css=tr >> css=.PASS')


# Playwright Python: 08 Pytest Fixtures


# Playwright Python: 09 Test Project
Project structure:
- Readme
- pytest.ini
- conftest.py
- page_objects
- tests

Create page object for the whole app (?)
```python
from playwright.sync_api import Playwright

class App:

    def __init__(self, playwright: Playwright):
        pass

    def login(self):
        pass

    def create_test(self):
        pass

    def open_test(self):
        pass

    def check_test_created(self):
        pass

    def delete_test(self):
        pass

    def close(self):
        pass
```

Create fixtures:
```python
@pytest.fixture
def get_playwright():
    with sync_playwright() as playwright:
        yield playwright

@pytest.fixture
def desktop_app(get_playwright):
    app = App(get_playwright)
    yield app
    app.close()
```

# Playwright Python: 10 Page objects
Two approaches:
1. Create meta page object Application.
Only this object will be created in fixtures. Other pages will be created inside app object.
2. Create fixtures for each page object.


# Playwright Python: 11 Scope
For each test user logging in from the beginning. If it takes 6 s, for 100 tests it takes 10 minutes. Optimization might be used.

Fixtures scopes:
- Session
- Package
- Module
- Class
- Function

Fixture of bigger scope can't use fixture of smaller scope (session can't use function).
Test methods could be combined into class if tests use common variables or methods.

Don't make tests dependent one from another!
If you need some pre-condition - move it to fixture.
Think is it possible to sett app state manipulating by web services or DB.
Ficture parameter autouse=True - when we don't need to pass fixture value to test functions but need this fixture is performed before tests.


# Playwright Python: 12 Configurations
How settings could be defined:
1. Python module settings.py with constants
2. Using pytest hooks (hook is special function with predefined name that is called in specific time).
Hooks should be written in conftest.py or in plugins for pytest.
Could be added to pytest.ini to addopts parameter
3. Using parameters in pytest.ini
```python
def pytest_addoption(parser):
    parser.addini('base_url', help='base url for site under test', default='http://127.0.0.1:8000')

@pytest.fixture
def desktop_app(get_playwright, request):
    base_url = request.config.getini('base_url')
```
4. Using config file (.json)

base-url better pass via command line options.
Keeping usernames and passwords in files is bad idea:
- it could be saved in file but not saved in VCS
- keep it in environment variables


# Playwright Python: 13 DDT
Decorator pytest.mark.parametrize
All parametrization data could kept in dictionary
```python
ddt = {
    'argnames': 'test_name,description',
    'argvalues': [('hello', 'world'),
                  ('hello', ''),
                  ('123', 'world'), ],
    'ids': ['general test', 'test with no description', 'test with digits in name']
}
```


# Playwright Python: 14 Browser configuration
slow_mo - to slower script run in get_playwright.chromium.launch(headless=headless)

Adding configuration options for browser:
```python
def __init__(self, playwright: Playwright, base_url: str, headless=False, device=None, **kwargs):
```
Playwright has predefined list of devices
If device config found, update it with kwargs. If not found, use kwargs as device config:
```python
device_config = playwright.devices.get(device)
if device_config is not None:
    device_config.update(kwargs)
else:
    device_config = kwargs
self.context = self.browser.new_context(**device_config)
```
List of devices:
https://github.com/microsoft/playwright/blob/main/packages/playwright-core/src/server/deviceDescriptorsSource.json

Add fixtures for mobile device.

Adding settings for location and accepted permissions to settings.py:
```python
BROWSER_OPTIONS = {
    "geolocation": {"latitude": 48.8, "longitude": 2.3},
    "permissions": ["geolocation"]
}
```
And use them when creating app:
```python
app = App(get_playwright, base_url=base_url, device=device, **settings.BROWSER_OPTIONS)
```
If desktop and mobile version differ too much, think about writing separate page objects.


# Playwright Python: 15 firefox and webkit
Move browser to separate fixture.
browser and headless to configuration options
self.page.wait_for_load_state()
FireFox is not supported for mobile. To pass browser to mobile_app fixture create environment variable. Remove it after test.
To run tests on different combination - parametrize fixtures
TODO: how to specify list of parameters in config?


# Playwright Python: 15 firefox and webkit 1
Duplicate of previous video


# Playwright Python: 16 waiting
Auto-waiting
https://playwright.dev/python/docs/actionability

page.wait_for_load_state() 
- load (default) - wait till all html, css and js are loaded
- domcontentloaded - wait for only html loaded
- networkidle - wait for network non-activity

For wait context manager could be used. wait_until - condition, timeout.
In click need to disable automatic wait as we have another wait:
```python
with self.page.expect_navigation(wait_until='load', timeout=(wait_time+1)*1000):
    self.page.click('.waitPage', no_wait_after=True)
```

Method self.page.query_selector doesn't have own timeout. If no elements, it returns None.


# Playwright Python: 17 request intercept
- Need to perform many actions to perform simple test
- Service required for testing is not available in our environment
In these cases are two ways:
- Leave test manual
- Make mocks with required data
For this cases Playwright allows intercept and modify requests to server.
self.page.route(url, handler) - method to intercept requests.
def handler(route: Route, request: Request):
- route.fullfill - response substitution
- route.continue_() - do nothing, or modify data nad to server
- route.abort() - cancel request
```python
        def handler(route: Route, request: Request):
            route.fulfill(status=200, body=payload)
```

After performing test with request interception it should be stopped:
If handler is not specified - routing for all handlers will be stopped
```python
def stop_intercept(self, url: str):
    self.page.unroute(url)
```

Url pattern could be passed as regular expression

Request interception works only for browser request, for requests made by backend need real mocks.


# Playwright Python: 18 Event handlers
https://playwright.dev/python/docs/api/class-page#events    Events to handle
There are two methods to work with events:
- page.on - process all events of specified type
- page.once - only one event, after that handler will be removed

```python
        def console_handler(message: ConsoleMessage):
            if message.type == 'error':
                logging.error(f'Page {self.page.url}: console error: {message.text}')

        def dialog_handler(dialog: Dialog):
            logging.warning(f'Page {self.page.url}: dialog text: {dialog.message}')
            dialog.accept()

        self.page.on('console', console_handler)
        self.page.on('dialog', dialog_handler)
```

self.page.evaluate() - just performs JavaScript code
self.page.evaluate_handle() - performs JavaScript code and returns JavaScript object as variable with which we could interact in tests


# Playwright Python: 19 Git


# Playwright Python: 20 Web services
To work with web service need token that could be taken from page.
self.page.wait_for_timeout(300) - non-conditional wait (in ms)


# Playwright Python: 21 DB
DB Browser for SQLite - for professional PyCharm
sqlitebrowser.org
Tables tcm_testcase and tcm_testrun


# Playwright Python: 22 multiple roles
For another role - created new fixture desktop_app_bob
self.page.wait_for_event('response') - added to refresh_dashboard


# Playwright Python: 23 Reporting
Pytest parameter junitxml=report.xml
Allure:
https://allurereport.org/docs/
pip install allure-pytest
Added decorator @allure.step to steps in App class
Added @allure.title("Title") - to tests
Add parameter --alluredir report/ to start tests to generate metadata
https://github.com/allure-framework/allure2/releases/tag/2.32.0
For Windows:
echo $Env:path
allure serve ./report/ --port 3060

Adding screenshots on FAIL:
```python
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
```


# Playwright Python: 24 TCM
Add pytest markers for tests to be added to test management system: @pytest.mark.test_id(213)

TODO: Need investigate


# Playwright Python: 25 Test Parameters


# Playwright: взаємодіємо з методом .locator()
Test module test_locator.py

- self.page.click(<LOCATOR>) - raises TimeoutException if element is not found
- self.page.query_selector().click(<LOCATOR>) - returns None if element is not found
- self.page.locator(<LOCATOR>).click() (.is_hidden()) - it doesn't raise exception, doesn't return None; it could be used in method expect
Check visibility:
```python
def test_locator_does_not_exist(test_case):
    not_existing_selector = '.not_existing_selector'

    # old fashion way
    assert test_case.query_selector(not_existing_selector) is None
    # brand-new with pytest assert
    assert test_case.locator(not_existing_selector).is_hidden()
    # brand-new with playwright expect
    expect(test_case.locator(not_existing_selector)).not_to_be_visible()
```
locator(, has_text="expected text on screen")
```python
def test_locator_has_text(test_case):
    # find row locator by has_text, then find button locator
    row = test_case.locator('tbody tr', has_text='Successfull registration')
    row.locator('.passBtn').click()

    # same way with selectors chain and css pseudo class :has-text
    test_case.locator('tbody tr:has-text("Successfull registration") >> .passBtn').click()
```
page.locator(, has=page.locator()) - finds element with nested element (in has parameter)
```python
def test_locator_has_locator(test_case):
    test_case.locator('tbody tr', has=test_case.locator('.delete_1')).locator('.passBtn').click()
    test_case.locator('tbody tr:has(.delete_1) .passBtn').click()
```
If element could have different locators, they could be separated by comma:
```python
def test_locator_different_options(test_case):
    # if locator can be changed, you may put few, separated with coma. 1st found will be used
    test_case.locator('tbody tr:has-text("Successfull registration") >> .passBtn, pass_1, .aaa').click()
```
Referring to first or nth element:
```python
def test_locator_multiple_findings_handle(test_case):
    # click 1st button
    test_case.locator('.passBtn').first.click()
    # click 2nd button
    test_case.locator('.passBtn').nth(1).click()

    # first property work even if 1 locator found
    test_case.locator('.pass_1').first.click()
```
Filtering element if several were found:
```python
def test_locator_filter(test_case):
    # if locator still finds many elements, there is a way to filter them
    test_case.locator('tbody tr').filter(has=test_case.locator('.pass_1')).locator('.passBtn').click()
```
self.page.locator().wait_for(timeout, state) - wait till element will be in state. Visible by default.
state - "attached", "detached", "hidden", "visible"
```python
    last_record = alice.locator('p >> nth=2')
    # wait until element is visible
    # also we can wait it disappear
    # last_record.wait_for(state='hidden')
    last_record.wait_for()
    assert last_record.is_visible()
```


# Playwright: метод перевірки expect()
Test module test_expect.py

To expect could be passed:
- page ()
- locator
- response

There're couples of expects: to_be_ok vs not_to_be_ok
expect(status).not_to_have_class('123456') - checks all classes
expect(status).to_have_text('PASS', timeout=10_000) - timeout in ms to check expect
Check of attributes and css
    expect(pass_btn).to_have_attribute(name='onclick', value="setStatus(1, 'PASS')")
    expect(pass_btn).to_have_css(name='margin', value='0px 5px 0px 0px')
expect(menu_items).to_have_count(5) - how many elements are found
expect(test_name).to_have_value(text) - value of input field
Failed expect stops script.


# Playwright: тестуємо API
Test module test_http.py
alice is page object
    response = alice.request.get('/getstat')
    expect(response).to_be_ok()
In request we shouldn't specify full endpoint as base_url is specified in context object:
```python
    context = chromium.new_context(permissions=["geolocation"],
                                   geolocation={"latitude": 48.8, "longitude": 2.3},
                                   base_url='http://127.0.0.1:8000')
    page = context.new_page()
```
If need to make request to another backend, we could pass the whole endpoint.


# Pytest-analyzer: я написав Testomat.io плагін для pytest
pytest-analyzer - plugin for Testomat.io
pytest --analyzer add
- This plugin collects data about tests, sends to testomat.io, gets ids and updates tests with those ids.
https://10minutemail.com/ - email box for 10 minutes
pytest --analyzer sync


////////////////////////////////
https://playwright.dev/python/docs/api/class-framelocator    Working with iframes
https://playwright.dev/python/docs/input#upload-files    Uploading files
