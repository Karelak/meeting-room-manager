"""Repository for Booking data access."""
from app.repositories.base_repository import BaseRepository
from app.models.booking import Booking


class BookingRepository(BaseRepository):
    """Repository for Booking-specific queries."""

    def __init__(self):
        super().__init__(Booking)

    def find_by_employee(self, employee_id):
        """Find all bookings for an employee."""
        return self.model.query.filter_by(employeeid=employee_id).all()

    def find_by_room(self, room_id):
        """Find all bookings for a room."""
        return self.model.query.filter_by(roomid=room_id).all()

    def check_conflict(self, room_id, time_begin, time_finish, exclude_booking_id=None):
        """Check if booking conflicts with existing bookings."""
        return Booking.check_conflict(
            room_id, time_begin, time_finish, exclude_booking_id
        )

    def get_active_bookings(self):
        """Get all currently active bookings."""
        return [b for b in self.get_all() if b.is_active()]

    def get_future_bookings(self):
        """Get all future bookings."""
        return [b for b in self.get_all() if b.is_future()]

    def get_past_bookings(self):
        """Get all past bookings."""
        return [b for b in self.get_all() if b.is_past()]

    def create_booking(self, employee_id, room_id, time_begin, time_finish):
        """Create and save a new booking."""
        booking = Booking.create_booking(employee_id, room_id, time_begin, time_finish)
        return self.save(booking)

    def get_employee_bookings_sorted(self, employee_id):
        """Get employee bookings sorted by time."""
        return (
            self.model.query.filter_by(employeeid=employee_id)
            .order_by(self.model.timebegin.desc())
            .all()
        )

    def get_room_bookings_sorted(self, room_id):
        """Get room bookings sorted by time."""
        return (
            self.model.query.filter_by(roomid=room_id)
            .order_by(self.model.timebegin)
            .all()
        )
