from flask import Flask, abort
import os

from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager, current_user
from flask.ext.bcrypt import Bcrypt
from flask.ext.gravatar import Gravatar
from flask.ext.mail import Mail
from flask.ext.misaka import Misaka
from flask.ext.admin import Admin, AdminIndexView
from flask.ext.admin.contrib.sqla import ModelView


app = Flask(__name__)
app.config.from_object(os.environ["CONFIG"])

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"

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
misaka = Misaka(app)

class CustomAdminIndexView(AdminIndexView):
    def is_accessible(self):
        try:
            return current_user.name == "admin"
        except AttributeError:
            self.inaccessible_callback()

    def inaccessible_callback(self, *args, **kwargs):
        return abort(403)

admin = Admin(app,
                name='minitweet',
                index_view=CustomAdminIndexView(),
                template_mode="bootstrap3"
            )

from .models import User, Post

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Post, db.session))

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id= int(user_id)).first()

from . import routes
