import pytest

ddt = {"argnames": 'name,description',
       "argvalues": [("Hello", "World"),
                     ("Hello", ""),("123", "World")],
       'ids': ["General test", "Test with no description", "Test with digits in name"]
       }


@pytest.mark.parametrize(**ddt)
def test_new_testcase(desktop_app_auth, name, description):
    desktop_app_auth.navigate_to('Create new test')
    desktop_app_auth.create_test(name, description)
    desktop_app_auth.navigate_to('Test Cases')
    assert desktop_app_auth.test_cases.check_test_exists(name)
    desktop_app_auth.test_cases.delete_test_by_name(name)
