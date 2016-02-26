import unittest
from base import BaseTestCase


class TestTemplates(BaseTestCase):
    """
    Ensure every view function render the correct template
    """

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
            self.login("admin", "adminpassword")
            self.client.get("/publish")
            self.assertTemplateUsed("publish.html")

    def test_userProfile_page_template(self):
        with self.client:
            self.client.get("/u/admin")
            self.assertTemplateUsed("user_profile_posts.html")

    def test_profileSettings_page_template(self):
        with self.client:
            self.login("admin", "adminpassword")
            self.client.get("/u/admin/profile_settings")
            self.assertTemplateUsed("profile_settings.html")

    def test_unconfirmed_page_template(self):
        with self.client:
            self.create_user(name="unconfirmed_user",
                             email="unconfirmed@unconfirmed.un",
                             password="unconfirmed"
                             )
            self.login("unconfirmed_user", "unconfirmed")
            self.client.get("/unconfirmed")
            self.assertTemplateUsed("unconfirmed.html")

    def test_following_and_followers_page_template(self):
        with self.client:
            self.client.get("/u/admin/following")
            self.assertTemplateUsed("user_following_and_followers.html")

    def test_404_page_template(self):
        with self.client:
            self.client.get("/wrong_url")
            self.assertTemplateUsed("404.html")

    def test_403_page_template(self):
        with self.client:
            # anonymous user can't access to other users settings
            self.client.get("/u/admin/profile_settings")
            self.assertTemplateUsed("403.html")

    def test_500_page_template(self):
        with self.client:
            # currently i can't find a way to cause 500 error
            # in the tests so i will just use /500 view
            self.client.get('/500')
            self.assertTemplateUsed("500.html")


if __name__ == '__main__':
    unittest.main()
