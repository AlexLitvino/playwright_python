from playwright.sync_api import Playwright

from page_objects.test_cases import TestCases


class App:

    def __init__(self, playwright: Playwright, base_url, headless=False):
        self.browser = playwright.chromium.launch(headless=headless)
        self.context = self.browser.new_context(
            geolocation={"longitude": 41.890221, "latitude": 12.492348},
            permissions=["geolocation"]
        )
        self.page = self.context.new_page()
        self.base_url = base_url
        self.test_cases = TestCases(self.page)

    def goto(self, endpoint: str, use_base_url=True):
        if use_base_url:
            self.page.goto(self.base_url + endpoint)
        else:
            self.page.goto(endpoint)

    def navigate_to(self, menu):
        self.page.get_by_role("link", name=menu).click()

    def login(self, login: str, password: str):
        self.page.get_by_role("textbox", name="Username:").fill(login)
        self.page.get_by_role("textbox", name="Password:").fill(password)
        self.page.get_by_role("button", name="Login").click()

    def create_test(self, test_name: str, test_description: str):
        self.page.locator("#id_name").fill(test_name)
        self.page.get_by_role("textbox", name="Test description").fill(test_description)
        self.page.get_by_role("button", name="Create").click()

    def close(self):
        self.page.close()
        self.context.close()
        self.browser.close()
