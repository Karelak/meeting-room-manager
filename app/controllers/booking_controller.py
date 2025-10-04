"""Booking controller."""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.services.auth_service import AuthService
from app.services.booking_service import BookingService, BookingConflictError
from app.services.room_service import RoomService
from app.middleware.auth_decorators import login_required

booking_bp = Blueprint("bookings", __name__, url_prefix="/bookings")


class BookingController:
    """Controller for booking routes."""

    def __init__(self):
        self.auth_service = AuthService()
        self.booking_service = BookingService()
        self.room_service = RoomService()

    def list_bookings(self):
        """List all bookings for current user."""
        user = self.auth_service.get_current_user()
        user_bookings = self.booking_service.get_employee_bookings(user.employeeid)

        return render_template("bookings/list.html", user=user, bookings=user_bookings)

    def new_booking(self):
        """Create new booking."""
        user = self.auth_service.get_current_user()

        if request.method == "POST":
            roomid = request.form.get("roomid")
            timebegin = request.form.get("timebegin")
            timefinish = request.form.get("timefinish")

            try:
                self.booking_service.create_booking(
                    user.employeeid, roomid, timebegin, timefinish
                )
                flash("Booking created successfully", "success")
                return redirect(url_for("bookings.list_bookings"))
            except BookingConflictError as e:
                flash(str(e), "error")
            except ValueError as e:
                flash(str(e), "error")

        rooms = self.room_service.get_all_rooms()
        return render_template("bookings/new.html", user=user, rooms=rooms)

    def cancel_booking(self, booking_id):
        """Cancel a booking."""
        user = self.auth_service.get_current_user()

        try:
            self.booking_service.cancel_booking(booking_id, user)
            flash("Booking cancelled successfully", "success")
        except ValueError as e:
            flash(str(e), "error")
        except PermissionError as e:
            flash(str(e), "error")

        return redirect(url_for("bookings.list_bookings"))


# Initialize controller
booking_controller = BookingController()


# Register routes
@booking_bp.route("/")
@login_required
def list_bookings():
    return booking_controller.list_bookings()


@booking_bp.route("/new", methods=["GET", "POST"])
@login_required
def new_booking():
    return booking_controller.new_booking()


@booking_bp.route("/<int:booking_id>/cancel", methods=["POST"])
@login_required
def cancel_booking(booking_id):
    return booking_controller.cancel_booking(booking_id)
