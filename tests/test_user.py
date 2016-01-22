import unittest
from base import BaseTestCase
from minitweet_app.models import User
from flask.ext.login import current_user
from flask import request


class TestUser(BaseTestCase):

    def test_correct_login(self):
        with self.client:
            response = self.client.post("/login",
                data=dict(username="admin", password="adminpassword"),
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
            data=dict(username="incorrect", password="incorrect"),
            follow_redirects=True
        )

        # Ensure alert is shown
        self.assertIn(b'Invalid username or password', response.data)

    def test_change_user_profile_info(self):
        with self.client:
            self.client.post("/login",
                data=dict(username="admin", password="adminpassword"),
                follow_redirects=True
            )
            response = self.client.post("/u/admin/profile_settings",
                data=dict(bio="test bio", website="http://example.com"),
                follow_redirects=True
            )
            user = User.query.filter_by(name="admin").first()
            self.assertEqual(user.bio, "test bio")
            self.assertEqual(user.website, "http://example.com")
            self.assertIn(b"new settings were successfully applied",
                                                                response.data)

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
            self.create_user(
                    name="unconfirmed_user",
                    email="unconfirmed@unconfirmed.un",
                    password="unconfirmed"
            )
            self.client.post('/login',
                data=dict(username="unconfirmed_user", password="unconfirmed"),
                follow_redirects=True
            )
            response = self.client.get('/publish', follow_redirects=True)

            # check if user redirects to /unconfirmed page
            self.assertTrue(request.url.endswith('/unconfirmed'))

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
                data=dict(username="admin", password="adminpassword"),
                follow_redirects=True
            )
            self.client.get('/unconfirmed', follow_redirects=True)
            self.assertTrue(request.url.endswith('/posts'))

    def test_follow_user(self):
        with self.client:
            self.client.post("/login",
                data=dict(username="admin", password="adminpassword"),
                follow_redirects=True
            )
            self.create_user(
                name="test_user",
                email="test@user.com",
                password="testuserpassword"
            )
            admin = User.query.filter_by(name="admin").first()
            test_user= User.query.filter_by(name="test_user").first()
            response = self.client.get("/u/test_user/follow",
                follow_redirects=True
            )
            alert = b"you successfully followed test_user"
            self.assertIn(alert, response.data)
            self.assertIn(test_user, admin.following.all())
            self.assertIn(admin, test_user.followers.all())

    def test_unfollow_user(self):
        with self.client:
            self.client.post("/login",
                data=dict(username="admin", password="adminpassword"),
                follow_redirects=True
            )
            self.create_user(
                name="test_user",
                email="test@user.com",
                password="testuserpassword"
            )
            admin = User.query.filter_by(name="admin").first()
            test_user= User.query.filter_by(name="test_user").first()
            self.client.get("/u/test_user/follow",
                follow_redirects=True
            )
            response = self.client.get("/u/test_user/unfollow",
                follow_redirects=True
            )
            alert = b"you successfully Unfollowed test_user"
            self.assertIn(alert, response.data)
            self.assertNotIn(test_user, admin.following.all())
            self.assertNotIn(admin, test_user.followers.all())

    def test_follow_user_is_already_followed(self):
        self.client.post("/login",
            data=dict(username="admin", password="adminpassword"),
            follow_redirects=True
        )
        self.create_user(
            name="test_user",
            email="test@user.com",
            password="testuserpassword"
        )
        admin = User.query.filter_by(name="admin").first()
        test_user= User.query.filter_by(name="test_user").first()
        self.client.get("/u/test_user/follow",
            follow_redirects=True
        )
        response = self.client.get("/u/test_user/follow",
            follow_redirects=True
        )
        alert = b"you are already following test_user"
        self.assertIn(alert, response.data)

    def test_unfolow_user_is_not_followed(self):
        self.client.post("/login",
            data=dict(username="admin", password="adminpassword"),
            follow_redirects=True
        )
        self.create_user(
            name="test_user",
            email="test@user.com",
            password="testuserpassword"
        )
        admin = User.query.filter_by(name="admin").first()
        test_user= User.query.filter_by(name="test_user").first()
        response = self.client.get("/u/test_user/unfollow",
            follow_redirects=True
        )
        alert = b'you are not following test_user'
        self.assertIn(alert, response.data)


    def test_followings_and_followers(self):
        with self.client:
            self.create_user(name="test1", email="te@st1.com", password="test1t")
            self.create_user(name="test2", email="te@st2.com", password="test2t")
            self.client.post("/login",
                data=dict(username="admin", password="adminpassword"),
                follow_redirects=True
            )
            self.client.get("/u/test1/follow", follow_redirects=True)
            self.client.get("/u/test2/follow", follow_redirects=True)

            response = self.client.get('/u/admin/following')
            self.assertIn(b"test1", response.data)
            self.assertIn(b"test1", response.data)

            response2 = self.client.get('/u/test1/followers')
            self.assertIn(b"admin", response2.data)

    def test_followings_and_followers2(self):
        with self.client:
            self.create_user(
                            name="test1",
                            email="te@st1.com",
                            password="test1t",
                            confirmed=True)
            self.client.post("/login",
                data=dict(username="test1", password="test1t"),
                follow_redirects=True
            )

            self.client.get("/u/admin/follow")
            self.client.get("/logout")
            self.client.post("/login",
                data=dict(username="admin", password="adminpassword"),
                follow_redirects=True
            )
            response = self.client.get("/u/admin/followers",
                follow_redirects=True
            )
            self.assertIn(b"test1", response.data)

            response2 = self.client.get("/u/test1/following",
                follow_redirects=True
            )
            self.assertIn(b"admin", response2.data)

        def test__repr__method(self):
            user = User.query.filter_by(name="admin").first()
            self.assertTrue(str(user) == '<User admin>')

if __name__ == '__main__':
    unittest.main()
