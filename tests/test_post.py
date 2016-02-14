import unittest
from base import BaseTestCase
from minitweet_app.models import Post, User


class TestPost(BaseTestCase):

    def test_logged_in_user_can_publish_a_post(self):
        self.client.post("/login",
                         data=dict(username="admin", password="adminpassword"),
                         follow_redirects=True
                         )

        response = self.client.post('/publish',
                                    data=dict(
                                            post_title="test title",
                                            textarea="test post"
                                            ),
                                    follow_redirects=True
                                    )

        # Ensure post is stored in the database
        post = Post.query.filter_by(title="test title").first()
        self.assertTrue(post)
        self.assertEqual(post.title, "test title")
        self.assertEqual(post.body, "test post")
        admin = User.query.filter_by(name="admin").first()
        self.assertEqual(post.author_id, admin.id)

        # Ensure post is shown in the page
        self.assertIn(b"test title", response.data)
        self.assertIn(b"test post", response.data)

    def test__repr__method(self):
        post = Post.query.get(1)
        self.assertTrue(str(post) == "<Post Test post>")


if __name__ == '__main__':
    unittest.main()
