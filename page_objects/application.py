from playwright.sync_api import Browser

from page_objects.test_cases import TestCases


class App:

    def __init__(self, browser: Browser, base_url, **kwargs):
        self.browser = browser
        self.context = self.browser.new_context(**kwargs)
        self.page = self.context.new_page()
        self.base_url = base_url
        self.test_cases = TestCases(self.page)

    def goto(self, endpoint: str, use_base_url=True):
        if use_base_url:
            self.page.goto(self.base_url + endpoint)
        else:
            self.page.goto(endpoint)

    def navigate_to_menu(self, menu):
        self.page.get_by_role("link", name=menu).click()
        self.page.wait_for_load_state()

    def login(self, login: str, password: str):
        self.page.get_by_role("textbox", name="Username:").fill(login)
        self.page.get_by_role("textbox", name="Password:").fill(password)
        self.page.get_by_role("button", name="Login").click()

    def create_test(self, test_name: str, test_description: str):
        self.page.locator("#id_name").fill(test_name)
        self.page.get_by_role("textbox", name="Test description").fill(test_description)
        self.page.get_by_role("button", name="Create").click()

    def click_menu_button(self):
        self.page.click('.menuBtn')

    def is_visible_menu_button(self):
        return self.page.is_visible('.menuBtn')

    def get_location(self):
        return self.page.text_content('.position')

    def close(self):
        self.page.close()
        self.context.close()
