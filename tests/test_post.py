import unittest
from base import BaseTestCase
from minitweet_app.models import Post, User
import json


class TestPostViews(BaseTestCase):
    """
    Test views related to posts
    """

    def test_logged_in_user_can_publish_a_post(self):
        self.login("admin", "adminpassword")
        response = self.client.post('/publish',
                                    data=dict(post_title="test title",
                                              textarea="test post"
                                              ),
                                    follow_redirects=True
                                    )

        # Ensure post is stored in the database
        post = Post.query.filter_by(title="test title").first()
        # assert post is not None
        self.assertTrue(post)
        self.assertEqual(post.title, "test title")
        self.assertEqual(post.body, "test post")
        admin = User.query.filter_by(name="admin").first()
        self.assertEqual(post.author_id, admin.id)

        # Ensure post is shown in the page
        self.assertIn(b"test title", response.data)
        self.assertIn(b"test post", response.data)

    def test_like_post_with_logged_in_and_confirmed_user(self):
        """
        test login and confirmed users can like posts
        since liking is done through ajax the return from
        the view function is json
        """
        self.login("admin", "adminpassword")
        admin = User.query.filter_by(name="admin").first()
        self.create_post("test1", "test1", admin.id)
        test1 = Post.query.filter_by(title="test1").first()
        # send POST request to /post/1/like
        response = self.client.post("/post/{}/like".format(test1.id))
        # the expcected json to be returned from the view function
        expcected = {"status": "good",
                     "msg": None,
                     "category": None,
                     "like": True,
                     "likes_counting": test1.likers.count()
                     }
        self.assertTrue(admin.is_liking(test1))
        # unlike the post
        self.client.post("/post/{}/like".format(test1.id))
        self.assertFalse(admin.is_liking(test1))

        # response.data is not str it's Bytes object so we \
        # need to decode it first
        returned_json = json.loads(response.data.decode())
        self.assertEqual(returned_json, expcected)

    def test_like_post_with_not_logged_in_user(self):
        """
        test warning alert is returned when not logged in user
        try to like a post
        """
        admin = User.query.filter_by(name="admin").first()
        self.create_post("test1", "test1", admin.id)

        test1 = Post.query.filter_by(title="test1").first()
        response = self.client.post("/post/{}/like".format(test1.id))
        expcected = {"status": "error",
                     "msg": "Please Login or signup first",
                     "category": "warning",
                     "like": None,
                     "likes_counting": test1.likers.count()
                     }

        self.assertFalse(admin.is_liking(test1))

        # response.data is not str it is Bytes object so we \
        # need to decode it first
        returned_json = json.loads(response.data.decode())
        self.assertEqual(returned_json, expcected)

    def test_like_post_with_unconfirmed_user(self):
        """
        test warning alert is returned when unconfirmed user
        try to like a post
        """
        self.create_user("test_user", "test_user", "test_user")
        test_user = User.query.filter_by(name="test_user").first()
        admin = User.query.filter_by(name="admin").first()
        self.login("test_user", "test_user")

        self.create_post("test1", "test1", admin.id)
        test1 = Post.query.filter_by(title="test1").first()

        response = self.client.post("/post/{}/like".format(test1.id))
        expcected = {"status": "error",
                     "msg": "Please confirm your email first",
                     "category": "warning",
                     "like": None,
                     "likes_counting": test1.likers.count()
                     }

        self.assertFalse(test_user.is_liking(test1))

        # response.data is not str it is Bytes object so we \
        # need to decode it first
        returned_json = json.loads(response.data.decode())
        self.assertEqual(returned_json, expcected)


class TestPostMethods(BaseTestCase):
    """
    test methods related to the Post class
    """

    def test__repr__method(self):
        self.create_post('Test post', 'Test post', 1)
        post = Post.query.get(1)
        self.assertTrue(repr(post) == "<Post Test post>")


if __name__ == '__main__':
    unittest.main()
