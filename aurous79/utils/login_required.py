from flask import flash, session, redirect, url_for
from functools import wraps


def login_required(f):
    """Redirect user to login page if not logged in"""
    @wraps(f)
    def wrap(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first.")
            return redirect(url_for("login"))
    return wrap