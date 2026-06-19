import re

import requests


class WebService:

    def __init__(self, base_url):
        self.session = requests.session()  # to keep session between tests
        self.base_url = base_url

    def _get_token(self, url: str):
        rsp = self.session.get(self.base_url + url)
        match = re.search('<input type="hidden" name="csrfmiddlewaretoken" value="(.+?)">', rsp.text)
        if match:
            return match.group(1)
        else:
            assert False, 'Failed to get token'

    def login(self, login, password):
        token = self._get_token('/login/')
        data = {
            'username': login,
            'password': password,
            'csrfmiddlewaretoken': token
        }
        self.session.post(self.base_url + '/login/', data=data)
        # https://youtu.be/RBOtkYOsD-M?list=PLGE9K4YL_ywj4F7cSA4oDptnqTmyS7hZp&t=84
        csrftoken = self.session.cookies.get('csrftoken')
        self.session.headers.update({'X-CSRFToken': csrftoken})

    def create_test(self, test_name, test_description):
        token = self._get_token('/test/new')
        data = {
            'name': test_name,
            'description': test_description,
            'csrfmiddlewaretoken': token
        }
        self.session.post(self.base_url + '/test/new', data=data)

    def report_test(self, test_id: int, status: str):
        self.session.post(self.base_url + f'/tests/{test_id}/status', json={'status': status})

    def close(self):
        self.session.close()
