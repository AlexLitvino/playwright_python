from playwright.sync_api import Page


class TestCases:

    def __init__(self, page: Page):
        self.page = page

    def check_test_exists(self, test_name):
        return self.page.query_selector(f'//td[text()="{test_name}"]') is not None

    def delete_test_by_name(self, test_name: str):
        self.page.locator(f'//td[text()="{test_name}"]/../*[@class="ttRemBtn"]/button').click()