from flask import Flask
import os

from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.bcrypt import Bcrypt
from flask.ext.gravatar import Gravatar
from flask.ext.mail import Mail


app = Flask(__name__)
app.config.from_object(os.environ["CONFIG"])

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "views.login"

bcrypt = Bcrypt(app)

gravatar = Gravatar(
                    app,
                    size=200,
                    rating='g',
                    default='retro',
                    force_default=False,
                    force_lower=False,
                    use_ssl=True,
                    base_url=None
             )

mail = Mail(app)

from .models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id= int(user_id)).first()

from . import views
