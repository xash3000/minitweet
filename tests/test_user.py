import unittest
from base import BaseTestCase
from flask.ext.login import current_user
from flask import request
from minitweet_app.shared.models import Post, User
import json


class TestUserMethods(BaseTestCase):
    """
    test methods related to the User class
    """

    def test__repr__method(self):
        admin = User.query.filter_by(name="admin").first()
        self.assertTrue(repr(admin) == '<User admin>')

    def test_follow_method(self):
        admin = User.query.filter_by(name="admin").first()
        self.create_user("test_user", "test_user", "test_user")
        test_user = User.query.filter_by(name="test_user").first()
        admin.follow(test_user)
        test_user.follow(admin)

        self.assertIn(test_user, admin.following)
        self.assertIn(admin, test_user.following)

    def test_unfollow_method(self):
        admin = User.query.filter_by(name="admin").first()
        self.create_user("test_user", "test_user", "test_user")
        test_user = User.query.filter_by(name="test_user").first()

        admin.follow(test_user)
        test_user.follow(admin)

        admin.unfollow(test_user)
        test_user.unfollow(admin)

        self.assertNotIn(test_user, admin.following)
        self.assertNotIn(admin, test_user.following)

    def test_is_following_method(self):
        admin = User.query.filter_by(name="admin").first()
        self.create_user("test_user", "test_user", "test_user")
        test_user = User.query.filter_by(name="test_user").first()

        admin.follow(test_user)

        self.assertTrue(admin.is_following(test_user))
        self.assertFalse(test_user.is_following(admin))

    def test_get_posts_from_followed_users_method(self):
        admin = User.query.filter_by(name="admin").first()
        self.create_user("test_user", "test_user", "test_user")
        self.create_user("test_user2", "test_user2", "test_user2")
        test_user = User.query.filter_by(name="test_user").first()
        test_user2 = User.query.filter_by(name="test_user2").first()

        admin.follow(test_user)
        admin.follow(test_user2)

        self.create_post("test1", "test1", test_user.id)
        self.create_post("test2", "test2", test_user.id)
        self.create_post("test3", "test3", test_user2.id)
        posts = admin.get_posts_from_followed_users().all()
        # concnate test_user2 posts and test_user posts
        expcected = test_user2.posts.order_by(Post.id.desc()).all() + \
            test_user.posts.order_by(Post.id.desc()).all()

        self.assertEqual(posts, expcected)

    def test_is_liking_method(self):
        admin = User.query.filter_by(name="admin").first()
        self.create_post('test1', 'test1', admin.id)
        self.create_post('test2', 'test2', admin.id)
        post = Post.query.filter_by(title='test1').first()
        post2 = Post.query.filter_by(title='test2').first()
        admin.liked_posts.append(post)

        self.assertTrue(admin.is_liking(post))
        self.assertFalse(admin.is_liking(post2))

    def test_like_method(self):
        admin = User.query.filter_by(name="admin").first()
        self.create_post('test1', 'test1', admin.id)
        post = Post.query.filter_by(title='test1').first()
        admin.like(post)
        self.assertTrue(admin.is_liking(post))

    def test_unlike_method(self):
        admin = User.query.filter_by(name="admin").first()
        self.create_post('test1', 'test1', admin.id)
        post = Post.query.filter_by(title='test1').first()
        admin.like(post)
        admin.unlike(post)
        self.assertFalse(admin.is_liking(post))


class TestUserViews(BaseTestCase):
    """
    test views related to users
    """

    def test_correct_login(self):
        with self.client:
            response = self.login("admin", "adminpassword")

            # 200 (OK) HTTP status code
            self.assert200(response)

            # check if user is authenticated
            self.assertTrue(current_user.is_authenticated())
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
        response = self.login("incorrect", "incorrect")

        # Ensure alert is shown
        self.assertIn(b'Invalid username or password', response.data)

    def test_change_user_profile_info(self):
        with self.client:
            self.login("admin", "adminpassword")
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
        self.login("admin", "adminpassword")
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
            self.login("unconfirmed_user", "unconfirmed")
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
            self.login("admin", "adminpassword")
            self.client.get('/unconfirmed', follow_redirects=True)
            self.assertIn('/posts/newest', request.url)

    def test_user_redirects_to_main_page_if_already_logged_in(self):
        with self.client:
            self.login("admin", "adminpassword")

            msg = b"You are already logged in"

            response1 = self.client.get("/login", follow_redirects=True)
            self.assertIn(msg, response1.data)

            response2 = self.client.get("/signup", follow_redirects=True)
            self.assertIn(msg, response2.data)

    def test_follow_user_with_logged_in_and_confirmed_user(self):
        with self.client:
            self.login("admin", "adminpassword")
            admin = User.query.filter_by(name="admin").first()
            self.create_user("test_user", "test_user", "test_user")
            test_user = User.query.filter_by(name="test_user").first()
            response = self.client.post("/u/test_user/follow_or_unfollow")
            expcected = {"status": "good",
                         "msg": None,
                         "category": None,
                         "follow": True
                         }
            self.assertTrue(admin.is_following(test_user))
            self.client.post("/u/test_user/follow_or_unfollow")
            self.assertFalse(admin.is_following(test_user))

            # response.data is not str it is Bytes object so we \
            # need to decode it first
            returned_json = json.loads(response.data.decode())
            self.assertEqual(returned_json, expcected)

    def test_follow_user_with_not_logged_in_user(self):
        with self.client:
            admin = User.query.filter_by(name="admin").first()
            self.create_user("test_user", "test_user", "test_user")
            test_user = User.query.filter_by(name="test_user").first()
            response = self.client.post("/u/test_user/follow_or_unfollow")
            expcected = {"status": "error",
                         "msg": "Please Login or signup first",
                         "category": "warning",
                         "follow": False
                         }
            self.assertFalse(admin.is_following(test_user))
            # response.data is not str it is Bytes object so we \
            # need to decode it first
            returned_json = json.loads(response.data.decode())
            self.assertEqual(returned_json, expcected)

    def test_follow_user_with_unconfirmed_user(self):
        with self.client:
            admin = User.query.filter_by(name="admin").first()
            self.create_user("test_user", "test_user", "test_user")
            test_user = User.query.filter_by(name="test_user").first()
            self.login("test_user", "test_user")
            response = self.client.post("/u/admin/follow_or_unfollow")
            expcected = {"status": "error",
                         "msg": "Please confirm your email first",
                         "category": "warning",
                         "follow": False
                         }
            self.assertFalse(test_user.is_following(admin))
            # response.data is not str it is Bytes object so we \
            # need to decode it first
            returned_json = json.loads(response.data.decode())
            self.assertEqual(returned_json, expcected)


if __name__ == '__main__':
    unittest.main()
