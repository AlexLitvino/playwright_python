import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)

    context = browser.new_context(
        geolocation={"longitude": 41.890221, "latitude": 12.492348},
        permissions=["geolocation"]
    )

    page = context.new_page()

    page.goto("http://127.0.0.1:8000/login/?next=/")
    page.get_by_role("textbox", name="Username:").fill("alice")
    page.get_by_role("textbox", name="Password:").fill("Qamania123")
    page.get_by_role("button", name="Login").click()

    page.get_by_role("link", name="Create new test").click()
    page.locator("#id_name").fill("Hello")
    page.get_by_role("textbox", name="Test description").fill("World")
    page.get_by_role("button", name="Create").click()

    page.get_by_role("link", name="Test Cases").click()

    assert page.query_selector('//td[text()="Hello"]') is not None

    page.goto('http://127.0.0.1:8000/tests')

    #page.locator(".ttRem.deleteBtn.delete_15").click()  # TODO: locator should be updated as id every time incremented
    page.get_by_role("link").filter(has_text=re.compile(r"^$")).nth(1).click()

    # ---------------------
    context.close()
    browser.close()


# with sync_playwright() as playwright:
#     run(playwright)


def test_new_testcase():
    with sync_playwright() as playwright:
        run(playwright)
