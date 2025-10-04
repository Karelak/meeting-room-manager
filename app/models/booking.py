"""Booking model with conflict detection logic."""
from datetime import datetime
from app.models import db


class Booking(db.Model):
    """Booking model representing room reservations."""

    __tablename__ = "bookings"

    bookingid = db.Column(
        db.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True
    )
    employeeid = db.Column(
        db.Integer,
        db.ForeignKey("employees.employeeid", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    roomid = db.Column(
        db.Integer,
        db.ForeignKey("rooms.roomid", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    timebegin = db.Column(
        db.Text, nullable=False, default=lambda: datetime.now().isoformat()
    )
    timefinish = db.Column(db.Text)

    # Relationships
    employee = db.relationship("Employee", back_populates="bookings")
    room = db.relationship("Room", back_populates="bookings")

    def __repr__(self):
        return f"<Booking {self.bookingid} - Room {self.roomid}>"

    # Business logic methods
    def has_conflict(self):
        """Check if this booking conflicts with existing bookings."""
        conflict = Booking.query.filter(
            Booking.roomid == self.roomid,
            Booking.bookingid != self.bookingid,  # Exclude self when updating
            Booking.timebegin < self.timefinish,
            Booking.timefinish > self.timebegin,
        ).first()

        return conflict is not None

    def is_active(self):
        """Check if booking is currently active."""
        try:
            now = datetime.now()
            begin = datetime.fromisoformat(self.timebegin)
            finish = datetime.fromisoformat(self.timefinish)
            return begin <= now <= finish
        except (ValueError, TypeError):
            return False

    def is_past(self):
        """Check if booking is in the past."""
        try:
            finish = datetime.fromisoformat(self.timefinish)
            return finish < datetime.now()
        except (ValueError, TypeError):
            return False

    def is_future(self):
        """Check if booking is in the future."""
        try:
            begin = datetime.fromisoformat(self.timebegin)
            return begin > datetime.now()
        except (ValueError, TypeError):
            return False

    def can_be_cancelled_by(self, employee):
        """Check if employee can cancel this booking."""
        return employee.can_cancel_booking(self)

    def get_duration_minutes(self):
        """Calculate booking duration in minutes."""
        try:
            begin = datetime.fromisoformat(self.timebegin)
            finish = datetime.fromisoformat(self.timefinish)
            return int((finish - begin).total_seconds() / 60)
        except (ValueError, TypeError):
            return 0

    def get_formatted_time_range(self):
        """Get human-readable time range."""
        try:
            begin = datetime.fromisoformat(self.timebegin)
            finish = datetime.fromisoformat(self.timefinish)
            return f"{begin.strftime('%Y-%m-%d %H:%M')} - {finish.strftime('%H:%M')}"
        except (ValueError, TypeError):
            return f"{self.timebegin} - {self.timefinish}"

    @classmethod
    def check_conflict(cls, room_id, time_begin, time_finish, exclude_booking_id=None):
        """Check if a booking would conflict with existing bookings."""
        query = cls.query.filter(
            cls.roomid == room_id,
            cls.timebegin < time_finish,
            cls.timefinish > time_begin,
        )

        if exclude_booking_id:
            query = query.filter(cls.bookingid != exclude_booking_id)

        return query.first() is not None

    @classmethod
    def create_booking(cls, employee_id, room_id, time_begin, time_finish):
        """Factory method to create a new booking."""
        booking = cls(
            employeeid=employee_id,
            roomid=room_id,
            timebegin=time_begin,
            timefinish=time_finish,
        )
        return booking

    @classmethod
    def find_by_employee(cls, employee_id):
        """Find all bookings for a specific employee."""
        return cls.query.filter_by(employeeid=employee_id).all()

    @classmethod
    def find_by_room(cls, room_id):
        """Find all bookings for a specific room."""
        return cls.query.filter_by(roomid=room_id).all()
