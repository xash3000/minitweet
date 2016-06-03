from flask.ext.testing import TestCase
from minitweet_app import app, db
import os
from minitweet_app.shared.models import User, Post


class BaseTestCase(TestCase):
    """A base test case."""

    def create_app(self):
        app.config.from_object("config.TestConfig")
        return app

    def setUp(self):
        """
        this method will execute before every test method
        """
        # make sure config = TestConfig
        app.config.from_object("config.TestConfig")
        # create all tables
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
        """
        this method will execute after every test method
        """
        # make sure config = TestConfig
        app.config.from_object("config.TestConfig")
        db.session.remove()
        # drop all tables to strart with fresh database on every test method
        db.drop_all()

    def create_user(self, name, email, password,
                    bio='', website="", confirmed=False):
        """
        helper method to create User instance and store it in the database
        """
        # make sure config = TestConfig
        app.config.from_object("config.TestConfig")
        u = User(name, email, password, bio, website, confirmed)
        db.session.add(u)
        db.session.commit()

    def login(self, name, password):
        """
        helper method to login users
        """
        app.config.from_object("config.TestConfig")
        return self.client.post("/login",
                                data=dict(username=name,
                                          password=password
                                          ),
                                follow_redirects=True
                                )

    def create_post(self, title, body, author_id):
        """
        helper method to create Post instance and store it in the database
        """
        app.config.from_object("config.TestConfig")
        post = Post(title, body, author_id)
        db.session.add(post)
        db.session.commit()
