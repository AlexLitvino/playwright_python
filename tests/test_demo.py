import allure

import pytest


@pytest.mark.test_id(214)
@allure.title('test to wait more than 30 seconds')
def test_more_30_sec(desktop_app_auth):
    desktop_app_auth.navigate_to_menu('Demo pages')
    desktop_app_auth.demo_pages.open_page_after_wait(32)
    assert desktop_app_auth.demo_pages.check_wait_page()


@pytest.mark.test_id(215)
def test_ajax(desktop_app_auth):
    desktop_app_auth.navigate_to_menu('Demo pages')
    desktop_app_auth.demo_pages.open_page_and_wait_ajax(2)
    assert 2 == desktop_app_auth.demo_pages.get_ajax_responses_count()


@pytest.mark.test_id(216)
def test_handlers(desktop_app_auth):
    desktop_app_auth.navigate_to_menu('Demo pages')
    desktop_app_auth.demo_pages.click_new_page_button()
    desktop_app_auth.demo_pages.inject_js()
    desktop_app_auth.navigate_to_menu('Test Cases')
    assert desktop_app_auth.test_cases.check_test_exists('Check new test')
