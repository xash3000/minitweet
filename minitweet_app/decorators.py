# ``# pragma: no cover`` is to exclude lines from coverage test
from functools import wraps  # pragma: no cover

from flask import flash, redirect, url_for  # pragma: no cover
from flask.ext.login import current_user  # pragma: no cover


def check_confirmed(func):
    @wraps(func)  # pragma: no cover
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated or current_user.is_active:
            if current_user.confirmed is False:
                return redirect(url_for('unconfirmed'))
        return func(*args, **kwargs)
    return decorated_function


def check_user_already_logged_in(func):
    @wraps(func)  # pragma: no cover
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated or current_user.is_active:
                flash("You are already logged in", "primary")
                return redirect(url_for('home'))
        return func(*args, **kwargs)
    return decorated_function
