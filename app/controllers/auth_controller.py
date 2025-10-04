"""Authentication controller."""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.services.auth_service import AuthService

auth_bp = Blueprint("auth", __name__)


class AuthController:
    """Controller for authentication routes."""

    def __init__(self):
        self.auth_service = AuthService()

    def index(self):
        """Root route - redirect to login or dashboard."""
        if self.auth_service.is_logged_in():
            return redirect(url_for("dashboard.main"))
        return redirect(url_for("auth.login"))

    def login(self):
        """Login route."""
        if request.method == "POST":
            email = request.form.get("email")
            password = request.form.get("password")

            employee = self.auth_service.login(email, password)
            if employee:
                return redirect(url_for("dashboard.main"))
            else:
                flash("Invalid email or password", "error")

        return render_template("auth/login.html")

    def logout(self):
        """Logout route."""
        self.auth_service.logout()
        flash("You have been logged out", "info")
        return redirect(url_for("auth.login"))


# Initialize controller
auth_controller = AuthController()

# Register routes
@auth_bp.route("/")
def index():
    return auth_controller.index()


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    return auth_controller.login()


@auth_bp.route("/logout")
def logout():
    return auth_controller.logout()
