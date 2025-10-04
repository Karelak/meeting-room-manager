"""Authentication decorators for route protection."""
from functools import wraps
from flask import session, redirect, url_for, flash


def login_required(f):
    """Decorator to require login for a route."""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "employeeid" not in session:
            flash("Please log in to access this page", "error")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)

    return decorated_function


def admin_required(f):
    """Decorator to require admin role for a route."""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "employeeid" not in session:
            flash("Please log in to access this page", "error")
            return redirect(url_for("auth.login"))

        if session.get("role") != "admin":
            flash("Access denied. Admin privileges required.", "error")
            return redirect(url_for("dashboard.main"))

        return f(*args, **kwargs)

    return decorated_function
