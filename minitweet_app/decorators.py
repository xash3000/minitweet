# ``# pragma: no cover`` is to exclude lines from coverage test
from functools import wraps  # pragma: no cover

from flask import flash, redirect, url_for  # pragma: no cover
from flask.ext.login import current_user  # pragma: no cover


def check_confirmed(func):
    """
    check if user is confirmed if not redirect him to unconfirmed page
    example usage:

        @app.route("/publish")
        @check_confirmed
        def publish():
            return "this is publish page"
    """
    @wraps(func)  # pragma: no cover
    def decorated_function(*args, **kwargs):
        # don't redirect not logged in users
        if current_user.is_authenticated:
            if current_user.confirmed is False:
                return redirect(url_for('unconfirmed'))
        return func(*args, **kwargs)
    return decorated_function  # pragma: no cover


def check_user_already_logged_in(func):
    """
    check if user is already_logged if yes redirect him to main page
    """
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
                flash("You are already logged in", "primary")
                return redirect(url_for('home'))
        return func(*args, **kwargs)
    return decorated_function  # pragma: no cover
