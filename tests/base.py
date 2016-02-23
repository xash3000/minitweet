from flask.ext.testing import TestCase
from minitweet_app import app, db
import os
from minitweet_app.models import User, Post


class BaseTestCase(TestCase):
    """A base test case."""

    def create_app(self):
        app.config.from_object("config.TestConfig")
        return app

    def setUp(self):
        app.config.from_object("config.TestConfig")
        db.create_all()
        self.create_user("admin",
                         "ad@min.com",
                         "adminpassword",
                         confirmed=True
                         )
        admin = User.query.get(1)
        # user follow himself to show his posts in the main page
        admin.follow(admin)
        db.session.commit()

    def tearDown(self):
        app.config.from_object("config.TestConfig")
        db.session.remove()
        db.drop_all()

    def create_user(self, name, email, password,
                    bio='', website="", confirmed=False):
        app.config.from_object("config.TestConfig")
        u = User(name, email, password, bio, website, confirmed)
        db.session.add(u)
        db.session.commit()

    def login(self, name, password):
        app.config.from_object("config.TestConfig")
        return self.client.post("/login",
                                data=dict(username=name,
                                          password=password
                                          ),
                                follow_redirects=True
                                )

    def create_post(self, title, body, author_id):
        app.config.from_object("config.TestConfig")
        post = Post(title, body, author_id)
        db.session.add(post)
        db.session.commit()
