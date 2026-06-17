from playwright.sync_api import Playwright


class App:

    def __init__(self, playwright: Playwright):
        self.browser = playwright.chromium.launch(headless=False)
        self.context = self.browser.new_context(
            geolocation={"longitude": 41.890221, "latitude": 12.492348},
            permissions=["geolocation"]
        )
        self.page = self.context.new_page()
        self.page.goto("http://127.0.0.1:8000/login/?next=/")

    def login(self):
        self.page.get_by_role("textbox", name="Username:").fill("alice")
        self.page.get_by_role("textbox", name="Password:").fill("Qamania123")
        self.page.get_by_role("button", name="Login").click()

    def create_test(self):
        self.page.get_by_role("link", name="Create new test").click()
        self.page.locator("#id_name").fill("Hello")
        self.page.get_by_role("textbox", name="Test description").fill("World")
        self.page.get_by_role("button", name="Create").click()

    def open_tests(self):
        self.page.get_by_role("link", name="Test Cases").click()

    def check_test_created(self):
        return self.page.query_selector('//td[text()="Hello"]') is not None

    def delete_test(self):
        self.page.locator(".ttRem.deleteBtn.delete_15").click()  # TODO: locator should be updated as id every time incremented

    def close(self):
        self.page.close()
        self.context.close()
        self.browser.close()
