import unittest
from base import BaseTestCase

class TestTemplates(BaseTestCase):

    def test_main_page_template(self):
        with self.client:
            self.client.get("/")
            self.assertTemplateUsed("index.html")

    def test_login_page_template(self):
        with self.client:
            self.client.get("/login")
            self.assertTemplateUsed("login.html")

    def test_signUp_page_template(self):
        with self.client:
            self.client.get("/signup")
            self.assertTemplateUsed("signup.html")

    def test_publish_page_template(self):
        with self.client:
            self.client.post("/login",
                data=dict(username="admin", password="adminpassword"),
                follow_redirects=True
            )
            self.client.get("/publish")
            self.assertTemplateUsed("publish.html")

    def test_userProfile_page_template(self):
        with self.client:
            self.client.get("/u/admin")
            self.assertTemplateUsed("user_profile.html")

    def test_profileSettings_page_template(self):
        with self.client:
            self.client.post("/login",
                data=dict(username="admin", password="adminpassword"),
                follow_redirects=True
            )
            self.client.get("/u/admin/profile_settings")
            self.assertTemplateUsed("profile_settings.html")

    def test_unconfirmed_page_template(self):
        with self.client:
            self.create_user(
                    name="unconfirmed_user",
                    email="unconfirmed@unconfirmed.un",
                    password="unconfirmed"
            )
            self.client.post('/login',
                data=dict(username="unconfirmed_user", password="unconfirmed"),
                follow_redirects=True
            )
            self.client.get("/unconfirmed")
            self.assertTemplateUsed("unconfirmed.html")


if __name__ == '__main__':
    unittest.main()
