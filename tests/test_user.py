import unittest
from base import BaseTestCase
from minitweet_app.models import User
from flask.ext.login import current_user
from flask import request


class TestUser(BaseTestCase):

    def test_correct_login(self):
        with self.client:
            response = self.client.post("/login",
                                        data=dict(
                                            username="admin",
                                            password="adminpassword"
                                        ),
                                        follow_redirects=True
                                        )

            # 200 (OK) HTTP status code
            self.assert200(response)

            # check if user is authenticated
            self.assertTrue(current_user.is_authenticated())
            # check if user is active
            self.assertTrue(current_user.is_active())
            # check if user is not anonymous
            self.assertFalse(current_user.is_anonymous())
            # get user id
            self.assertEqual(current_user.get_id(), "1")
            # test user redirects to the main page
            self.assertIn('/posts', request.url)

            # Ensure alert is shown after logging in
            # Binary format because str() object doesn't support Buffer api
            self.assertIn(b'you were just logged in', response.data)

    def test_incorrect_login(self):
        response = self.client.post("/login",
                                    data=dict(username="incorrect",
                                              password="incorrect"
                                              ),
                                    follow_redirects=True
                                    )

        # Ensure alert is shown
        self.assertIn(b'Invalid username or password', response.data)

    def test_change_user_profile_info(self):
        with self.client:
            self.client.post("/login",
                             data=dict(username="admin",
                                       password="adminpassword"
                                       ),
                             follow_redirects=True
                             )
            response = self.client.post("/u/admin/profile_settings",
                                        data=dict(bio="test bio",
                                                  website="http://example.com"
                                                  ),
                                        follow_redirects=True
                                        )
            user = User.query.filter_by(name="admin").first()
            self.assertEqual(user.bio, "test bio")
            self.assertEqual(user.website, "http://example.com")
            msg = b"new settings were successfully applied"
            self.assertIn(msg, response.data)

    def test_user_logout(self):
        # login
        self.client.post("/login",
                         data=dict(username="admin", password="adminpassword"),
                         follow_redirects=True
                         )
        # logout
        response = self.client.get("/logout", follow_redirects=True)
        self.assertIn(b"you were just logged out", response.data)

    def test_publish_page_requires_login(self):
        response = self.client.get("/publish", follow_redirects=True)
        self.assertIn(b"Please log in to access this page.", response.data)

    def test_publish_page_requires_email_confirmation(self):
        with self.client:
            self.create_user(name="unconfirmed_user",
                             email="unconfirmed@unconfirmed.un",
                             password="unconfirmed"
                             )
            self.client.post("/login",
                             data=dict(username="unconfirmed_user",
                                       password="unconfirmed"
                                       ),
                             follow_redirects=True
                             )
            response = self.client.get('/publish', follow_redirects=True)

            # test alert is shown
            self.assertIn(b'Please confirm your account', response.data)

    def test_logout_page_requires_login(self):
        response = self.client.get("/logout", follow_redirects=True)
        self.assertIn(b"Please log in to access this page.", response.data)

    def test_profile_settings_only_appear_to_profile_owner(self):
        with self.client:
            response = self.client.get('u/admin/profile_settings',
                                       follow_redirects=True
                                       )

            # 403 (Forbidden) HTTP status code
            self.assert403(response)

    def test_confirmed_user_redirects_to_mainPage_on_unconfirmed_page(self):
        with self.client:
            self.client.post("/login",
                             data=dict(username="admin",
                                       password="adminpassword"
                                       ),
                             follow_redirects=True
                             )
            self.client.get('/unconfirmed', follow_redirects=True)
            self.assertTrue(request.url.endswith('/posts/newest'))

        def test__repr__method(self):
            user = User.query.filter_by(name="admin").first()
            self.assertTrue(str(user) == '<User admin>')

        def test_user_user_redirects_to_main_page_if_already_logged_in(self):
            with self.client:
                self.client.post("/login",
                                 data=dict(username="admin",
                                           password="adminpassword"
                                           ),
                                 follow_redirects=True
                                 )

                msg = b"You are already logged in"

                response1 = self.client.get("/login", follow_redirects=True)
                self.assertIn(msg, response1.data)

                response2 = self.client.get("/signup", follow_redirects=True)
                self.assertIn(msg, response2.data)

if __name__ == '__main__':
    unittest.main()
