"""Repository for Room data access."""
from app.repositories.base_repository import BaseRepository
from app.models.room import Room


class RoomRepository(BaseRepository):
    """Repository for Room-specific queries."""

    def __init__(self):
        super().__init__(Room)

    def get_all_sorted(self):
        """Get all rooms sorted by floor and name."""
        return self.model.query.order_by(self.model.floor, self.model.roomname).all()

    def find_by_floor(self, floor):
        """Find all rooms on a specific floor."""
        return self.model.query.filter_by(floor=floor).all()

    def find_by_capacity(self, min_capacity):
        """Find rooms with at least specified capacity."""
        return self.model.query.filter(self.model.capacity >= min_capacity).all()

    def find_by_name(self, roomname):
        """Find room by name."""
        return self.model.query.filter_by(roomname=roomname).first()

    def find_available_rooms(self, time_begin, time_finish, min_capacity=None):
        """Find available rooms for a time slot."""
        return Room.find_available_rooms(time_begin, time_finish, min_capacity)

    def create_room(self, roomname, floor, capacity):
        """Create and save a new room."""
        room = Room.create_room(roomname, floor, capacity)
        return self.save(room)

    def get_floors(self):
        """Get list of unique floor numbers."""
        floors = self.model.query.with_entities(self.model.floor).distinct().all()
        return sorted([f[0] for f in floors])
