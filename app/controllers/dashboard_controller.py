"""Dashboard controller."""
from flask import Blueprint, render_template, redirect, url_for
from app.services.auth_service import AuthService
from app.services.booking_service import BookingService
from app.middleware.auth_decorators import login_required

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")


class DashboardController:
    """Controller for dashboard routes."""

    def __init__(self):
        self.auth_service = AuthService()
        self.booking_service = BookingService()

    def main_dashboard(self):
        """Main user dashboard."""
        user = self.auth_service.get_current_user()
        bookings = self.booking_service.get_employee_bookings(user.employeeid)

        return render_template("dashboard/main.html", user=user, bookings=bookings)


# Initialize controller
dashboard_controller = DashboardController()


# Register routes
@dashboard_bp.route("/")
@login_required
def main():
    return dashboard_controller.main_dashboard()
