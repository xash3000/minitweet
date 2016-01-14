from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
import os
import unittest
from minitweet_app import app, db
from minitweet_app.models import User
import coverage

app.config.from_object(os.environ["CONFIG"])
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command("db", MigrateCommand)


@manager.command
def test():
    """Runs the unit tests"""
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.command
def create_admin():
    """ create admin """
    admin = User(
        name="admin",
        email="ad@min.com",
        password="adminpassword",
        confirmed=True
    )
    db.session.add(admin)
    db.session.commit()


@manager.command
def test_user():
    """ create test user """
    admin = User(
        name="test_user",
        email="test@user.com",
        password="testuserpassword",
        confirmed=False
    )
    db.session.add(admin)
    db.session.commit()

@manager.command
def cov():
    """Runs the unit tests with coverage."""
    cov = coverage.coverage(
        branch=True,
        include='minitweet_app/*',
        omit="*/__init__.py"
    )
    cov.start()
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    cov.stop()
    cov.save()
    print('Coverage Summary:')
    cov.report()
    basedir = os.path.abspath(os.path.dirname(__file__))
    covdir = os.path.join(basedir, 'coverage')
    cov.html_report(directory=covdir)
    cov.erase()

if __name__ == '__main__':
    manager.run()
