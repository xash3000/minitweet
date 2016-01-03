import os

class BaseConfig(object):
    """
    Base Configuration which other configs inherits from it
    """
    # flask settings
    DEBUG = False
    SECRET_KEY = b'5\x00\x05\x84\x8a3-\\K#\xba\x08\xf6"\x9b\xef3\x84\xcd\xc7'

    # SQLALCHEMY settings
    SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class DevConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False
