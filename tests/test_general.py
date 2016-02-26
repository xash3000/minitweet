import unittest
from base import BaseTestCase

# TODO: refactor tests


class TestGeneral(BaseTestCase):

    def test_404(self):
        with self.client:
            response = self.client.get("/wrong_url")
            self.assert404(response)

    def test_403(self):
        with self.client:
            # anonymous user can't access to other users settings
            response = self.client.get("/u/admin/profile_settings")
            self.assert403(response)

    def test_500_page_template(self):
        with self.client:
            # currently i can't find a way to cause 500 error
            # in the tests so i will just use /500 view
            response = self.client.get('/500')
            self.assert500(response)
