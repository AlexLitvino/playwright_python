def test_column_hidden(mobile_app_auth):
    mobile_app_auth.click_menu_button()
    mobile_app_auth.navigate_to_menu('Test Cases')
    assert mobile_app_auth.test_cases.check_columns_hidden()
