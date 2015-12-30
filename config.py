class BaseConfig(object):
    """
    Base Configuration which other configs inherits from it
    """
    DEBUG = False
    SECRET_KEY = b'5\x00\x05\x84\x8a3-\\K#\xba\x08\xf6"\x9b\xef3\x84\xcd\xc7'
    SQLALCHEMY_DATABASE_URI = "postgresql:///minitweet_dev"
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class DevConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False
