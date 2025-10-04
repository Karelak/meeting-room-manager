"""Booking management service."""
from app.repositories.booking_repository import BookingRepository
from app.repositories.room_repository import RoomRepository
from app.repositories.employee_repository import EmployeeRepository


class BookingConflictError(Exception):
    """Exception raised when a booking conflicts with existing bookings."""

    pass


class BookingService:
    """Service for booking-related business logic."""

    def __init__(self):
        self.booking_repo = BookingRepository()
        self.room_repo = RoomRepository()
        self.employee_repo = EmployeeRepository()

    def create_booking(self, employee_id, room_id, time_begin, time_finish):
        """Create a new booking with conflict detection."""
        # Check for conflicts
        if self.booking_repo.check_conflict(room_id, time_begin, time_finish):
            raise BookingConflictError(
                "This room is already booked for the selected time"
            )

        # Verify room exists
        room = self.room_repo.get_by_id(room_id)
        if not room:
            raise ValueError("Room does not exist")

        # Verify employee exists
        employee = self.employee_repo.get_by_id(employee_id)
        if not employee:
            raise ValueError("Employee does not exist")

        # Create booking
        booking = self.booking_repo.create_booking(
            employee_id, room_id, time_begin, time_finish
        )
        return booking

    def cancel_booking(self, booking_id, employee):
        """Cancel a booking if employee has permission."""
        booking = self.booking_repo.get_by_id(booking_id)

        if not booking:
            raise ValueError("Booking not found")

        if not booking.can_be_cancelled_by(employee):
            raise PermissionError("You can only cancel your own bookings")

        self.booking_repo.delete(booking)
        return True

    def get_employee_bookings(self, employee_id):
        """Get all bookings for an employee."""
        return self.booking_repo.get_employee_bookings_sorted(employee_id)

    def get_room_bookings(self, room_id):
        """Get all bookings for a room."""
        return self.booking_repo.get_room_bookings_sorted(room_id)

    def get_all_bookings(self):
        """Get all bookings."""
        return self.booking_repo.get_all()

    def get_booking(self, booking_id):
        """Get a specific booking."""
        return self.booking_repo.get_by_id(booking_id)

    def check_availability(self, room_id, time_begin, time_finish):
        """Check if a room is available for a time slot."""
        return not self.booking_repo.check_conflict(
            room_id, time_begin, time_finish
        )

    def get_active_bookings(self):
        """Get currently active bookings."""
        return self.booking_repo.get_active_bookings()

    def get_future_bookings(self):
        """Get future bookings."""
        return self.booking_repo.get_future_bookings()
