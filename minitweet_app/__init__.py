from flask import Flask
import os
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager

app = Flask(__name__)

app.config.from_object(os.environ["CONFIG"])
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

from . import views
