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
    # Email settings
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    try:
        MAIL_USERNAME = os.environ["MAIL_USERNAME"]
    except:
        MAIL_USERNAME = "alifaki077@gmail.com"
    try:
        MAIL_PASSWORD = os.environ["MAIL_PASSWORD"]
    except:
        MAIL_PASSWORD = "Aloba077"


class DevConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False
