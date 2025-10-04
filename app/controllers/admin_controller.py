"""Admin controller."""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.services.auth_service import AuthService
from app.services.admin_service import AdminService
from app.services.room_service import RoomService
from app.middleware.auth_decorators import admin_required

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


class AdminController:
    """Controller for admin routes."""

    def __init__(self):
        self.auth_service = AuthService()
        self.admin_service = AdminService()
        self.room_service = RoomService()

    def admin_dashboard(self):
        """Admin dashboard."""
        user = self.auth_service.get_current_user()
        all_bookings = self.admin_service.get_all_bookings()
        all_employees = self.admin_service.get_all_employees()
        all_rooms = self.admin_service.get_all_rooms()
        tickets = self.admin_service.get_all_tickets()

        return render_template(
            "dashboard/admin.html",
            user=user,
            bookings=all_bookings,
            employees=all_employees,
            rooms=all_rooms,
            tickets=tickets,
        )

    def create_room(self):
        """Create a new room (admin only)."""
        roomname = request.form.get("roomname")
        floor = request.form.get("floor")
        capacity = request.form.get("capacity")

        try:
            self.room_service.create_room(roomname, floor, capacity)
            flash("Room created successfully", "success")
        except ValueError as e:
            flash(str(e), "error")

        return redirect(url_for("admin.admin_dashboard"))

    def create_user(self):
        """Create a new user (admin only)."""
        fname = request.form.get("fname")
        lname = request.form.get("lname")
        email = request.form.get("email")
        password = request.form.get("password")
        role = request.form.get("role")

        try:
            self.admin_service.create_user(fname, lname, email, password, role)
            flash("User created successfully", "success")
        except ValueError as e:
            flash(str(e), "error")

        return redirect(url_for("admin.admin_dashboard"))


# Initialize controller
admin_controller = AdminController()


# Register routes
@admin_bp.route("/dashboard")
@admin_required
def admin_dashboard():
    return admin_controller.admin_dashboard()


@admin_bp.route("/rooms/new", methods=["POST"])
@admin_required
def create_room():
    return admin_controller.create_room()


@admin_bp.route("/users/new", methods=["POST"])
@admin_required
def create_user():
    return admin_controller.create_user()
