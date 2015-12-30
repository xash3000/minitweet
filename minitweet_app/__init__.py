from flask import Flask
import os
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_object(os.environ["CONFIG"])
db = SQLAlchemy(app)
db.create_all()

from . import views
