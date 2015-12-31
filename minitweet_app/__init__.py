from flask import Flask
import os
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager


app = Flask(__name__)

app.config.from_object(os.environ["CONFIG"])
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)


login_manager.login_view = "views.login"

from .models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == int(user_id)).first()
from . import views
