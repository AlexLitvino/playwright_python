import json

import pytest


@pytest.mark.test_id(211)
def test_dashboard_data(desktop_app_auth):
    payload = json.dumps({"total": 0, "passed": 0, "failed": 0, "norun": 0})
    desktop_app_auth.intercept_requests('**/getstat/*', payload)
    desktop_app_auth.refresh_dashboard()
    desktop_app_auth.stop_intercept('**/getstat/*')
    assert desktop_app_auth.get_total_tests_stat() == '0'


@pytest.mark.test_id(212)
def test_multiple_roles(desktop_app_auth, desktop_app_bob, get_db):
    alice = desktop_app_auth
    bob = desktop_app_bob
    alice.refresh_dashboard()  # TODO: not clear why need this step: initially Alice statistics shows all 0 when run with other tests
    # https://youtu.be/bZ0WepSr6ak?list=PLGE9K4YL_ywj4F7cSA4oDptnqTmyS7hZp&t=196
    # page wasn't reloaded, but session remain the same
    before = alice.get_total_tests_stat()
    bob.navigate_to_menu('Create new test')
    bob.create_test('test by bob', 'bob')
    alice.refresh_dashboard()
    after = alice.get_total_tests_stat()
    get_db.delete_test_case('test by bob')
    assert int(before) + 1 == int(after)


# Test for Fail
@pytest.mark.test_id(213)
def test_multiple_roles_fail(desktop_app_auth, desktop_app_bob, get_db):
    alice = desktop_app_auth
    bob = desktop_app_bob
    #alice.refresh_dashboard()  # Tcommented out to make it fail
    before = alice.get_total_tests_stat()
    bob.navigate_to_menu('Create new test')
    bob.create_test('test by bob', 'bob')
    alice.refresh_dashboard()
    after = alice.get_total_tests_stat()
    get_db.delete_test_case('test by bob')
    assert int(before) + 1 == int(after)
