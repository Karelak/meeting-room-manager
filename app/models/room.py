"""Room model with availability logic."""
from app.models import db


class Room(db.Model):
    """Room model representing meeting rooms."""

    __tablename__ = "rooms"

    roomid = db.Column(
        db.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True
    )
    floor = db.Column(db.Integer, nullable=False)
    roomname = db.Column(db.Text, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)

    # Relationships
    bookings = db.relationship(
        "Booking", back_populates="room", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Room {self.roomname} (Floor {self.floor})>"

    # Business logic methods
    def get_display_name(self):
        """Get formatted room display name."""
        return f"{self.roomname} (Floor {self.floor}, Capacity: {self.capacity})"

    def is_available(self, time_begin, time_finish):
        """Check if room is available for given time slot."""
        from app.models.booking import Booking

        conflict = Booking.query.filter(
            Booking.roomid == self.roomid,
            Booking.timebegin < time_finish,
            Booking.timefinish > time_begin,
        ).first()

        return conflict is None

    def get_bookings_for_date(self, date_str):
        """Get all bookings for this room on a specific date."""
        from app.models.booking import Booking

        # Simple date filtering (can be improved with proper datetime parsing)
        return [b for b in self.bookings if b.timebegin.startswith(date_str)]

    def meets_capacity_requirement(self, required_capacity):
        """Check if room can accommodate required number of people."""
        return self.capacity >= required_capacity

    @classmethod
    def find_available_rooms(cls, time_begin, time_finish, min_capacity=None):
        """Find all rooms available for a given time slot."""
        all_rooms = cls.query.all()
        available = [r for r in all_rooms if r.is_available(time_begin, time_finish)]

        if min_capacity:
            available = [r for r in available if r.capacity >= min_capacity]

        return available

    @classmethod
    def create_room(cls, roomname, floor, capacity):
        """Factory method to create a new room."""
        room = cls(roomname=roomname, floor=floor, capacity=capacity)
        return room
