import os

class BaseConfig(object):
    """
    Base Configuration which other configs inherits from it
    """
    # flask settings
    DEBUG = False
    SECRET_KEY = os.environ["SECRET_KEY"]
    SECURITY_PASSWORD_SALT = os.environ["SECURITY_PASSWORD_SALT"]

    # SQLALCHEMY settings
    SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    #flask-mail settings
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_DEBUG = True
    MAIL_USERNAME = os.environ["MAIL_USERNAME"]
    MAIL_PASSWORD = os.environ["MAIL_PASSWORD"]
    MAIL_DEFAULT_SENDER=os.environ["MAIL_DEFAULT_SENDER"]


class DevConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False
