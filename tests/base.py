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
        self.create_user(
                    "admin",
                    "ad@min.com",
                    "adminpassword",
                    confirmed=True
                    )
        admin = User.query.get(1)
        # user follow himself to show his posts in the main page
        admin.follow(admin)
        db.session.add(
            Post("Test post", "This is a test", 1))
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
