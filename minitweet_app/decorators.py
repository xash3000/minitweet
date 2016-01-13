from functools import wraps

from flask import flash, redirect, url_for
from flask.ext.login import current_user


def check_confirmed(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated or current_user.is_active:
            if current_user.confirmed is False:
                return redirect(url_for('unconfirmed'))
        return func(*args, **kwargs)
    return decorated_function
