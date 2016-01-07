import os

class BaseConfig(object):
    """
    Base Configuration which other configs inherits from it
    """
    # flask settings
    DEBUG = False
    SECRET_KEY = os.environ["SECRET_KEY"]

    # SQLALCHEMY settings
    SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class DevConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False
