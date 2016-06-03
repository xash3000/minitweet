from flask import Flask, abort, render_template
import os

from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager, current_user
from flask.ext.bcrypt import Bcrypt
from flask.ext.gravatar import Gravatar
from flask.ext.mail import Mail
from flask.ext.misaka import Misaka
from flask.ext.admin import Admin, AdminIndexView
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.compress import Compress

app = Flask(__name__, template_folder='shared/templates',
            static_folder='shared/static')
app.config.from_object(os.environ["CONFIG"])


@app.errorhandler(404)
# for quick access
@app.route('/404')
def not_found(error=404):
    return render_template('404.html'), 404


@app.errorhandler(500)
# for quick access
@app.route('/500')
def internal_server_error(error=500):
    return render_template('500.html'), 500


@app.errorhandler(403)
# for quick access
@app.route('/403')
def forbidden(error=500):
    return render_template('403.html'), 403


db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = "auth.login"

bcrypt = Bcrypt(app)
gravatar = Gravatar(app,
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
            return current_user.is_admin
        except AttributeError:
            # anonymous user object doesn't have is_admin attribute
            self.inaccessible_callback()

    def inaccessible_callback(self, *args, **kwargs):
        return abort(403)

admin = Admin(app,
              name='minitweet',
              index_view=CustomAdminIndexView(),
              template_mode="bootstrap3"
              )

from .shared.models import User, Post

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Post, db.session))

Compress(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

from .main import main
from .auth import auth
from .posts import posts
from .users import users

app.register_blueprint(main)
app.register_blueprint(auth)
app.register_blueprint(posts)
app.register_blueprint(users)
