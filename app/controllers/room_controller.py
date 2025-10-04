"""Room controller."""
from flask import Blueprint, render_template
from app.services.auth_service import AuthService
from app.services.room_service import RoomService
from app.services.booking_service import BookingService
from app.middleware.auth_decorators import login_required

room_bp = Blueprint("rooms", __name__, url_prefix="/rooms")


class RoomController:
    """Controller for room routes."""

    def __init__(self):
        self.auth_service = AuthService()
        self.room_service = RoomService()
        self.booking_service = BookingService()

    def list_rooms(self):
        """List all rooms."""
        user = self.auth_service.get_current_user()
        all_rooms = self.room_service.get_all_rooms()

        return render_template("rooms/list.html", user=user, rooms=all_rooms)

    def room_detail(self, room_id):
        """Show room details."""
        user = self.auth_service.get_current_user()
        room = self.room_service.get_room(room_id)

        if not room:
            from flask import abort
            abort(404)

        bookings = self.booking_service.get_room_bookings(room_id)

        return render_template("rooms/detail.html", user=user, room=room, bookings=bookings)


# Initialize controller
room_controller = RoomController()


# Register routes
@room_bp.route("/")
@login_required
def list_rooms():
    return room_controller.list_rooms()


@room_bp.route("/<int:room_id>")
@login_required
def room_detail(room_id):
    return room_controller.room_detail(room_id)
