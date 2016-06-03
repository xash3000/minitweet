from flask import Blueprint

users = Blueprint("users", __name__, template_folder="templates",
                  static_folder="static")

from . import routes
