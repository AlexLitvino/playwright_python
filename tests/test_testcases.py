import pytest

ddt = {"argnames": 'name,description',
       "argvalues": [("Hello", "World"),
                     ("Hello", ""),("123", "World")],
       'ids': ["General test", "Test with no description", "Test with digits in name"]
       }


@pytest.mark.parametrize(**ddt)
def test_new_testcase(desktop_app_auth, name, description):
    desktop_app_auth.navigate_to_menu('Create new test')
    desktop_app_auth.create_test(name, description)
    desktop_app_auth.navigate_to_menu('Test Cases')
    assert desktop_app_auth.test_cases.check_test_exists(name)
    desktop_app_auth.test_cases.delete_test_by_name(name)


def test_testcase_does_not_exists(desktop_app_auth):
    desktop_app_auth.navigate_to_menu('Test Cases')
    assert not desktop_app_auth.test_cases.check_test_exists('Abracadabra')


def test_delete_test_case(desktop_app_auth, get_web_service):
    test_name = 'test for deletion'
    get_web_service.create_test(test_name, 'delete me')
    desktop_app_auth.navigate_to_menu('Test Cases')
    assert desktop_app_auth.test_cases.check_test_exists(test_name)
    desktop_app_auth.test_cases.delete_test_by_name(test_name)
    assert not desktop_app_auth.test_cases.check_test_exists(test_name)


# Test using DB
def test_new_testcase_simple(desktop_app_auth, get_db):
    test_name = 'Hello'
    tests = get_db.list_test_cases()
    desktop_app_auth.navigate_to_menu('Create new test')
    desktop_app_auth.create_test(test_name, 'world')
    desktop_app_auth.navigate_to_menu('Test Cases')
    assert desktop_app_auth.test_cases.check_test_exists(test_name)
    assert len(tests) + 1 == len(get_db.list_test_cases())
    #desktop_app_auth.test_cases.delete_test_by_name(test_name)
    get_db.delete_test_case(test_name)
