"""Room management service."""
from app.repositories.room_repository import RoomRepository


class RoomService:
    """Service for room-related business logic."""

    def __init__(self):
        self.room_repo = RoomRepository()

    def get_all_rooms(self):
        """Get all rooms sorted by floor and name."""
        return self.room_repo.get_all_sorted()

    def get_room(self, room_id):
        """Get a specific room."""
        return self.room_repo.get_by_id(room_id)

    def create_room(self, roomname, floor, capacity):
        """Create a new room."""
        # Validate inputs
        if not roomname or not roomname.strip():
            raise ValueError("Room name is required")

        if floor is None or floor < 0:
            raise ValueError("Valid floor number is required")

        if capacity is None or capacity < 1:
            raise ValueError("Capacity must be at least 1")

        # Check if room name already exists
        existing = self.room_repo.find_by_name(roomname)
        if existing:
            raise ValueError(f"Room '{roomname}' already exists")

        # Create room
        room = self.room_repo.create_room(roomname, int(floor), int(capacity))
        return room

    def update_room(self, room_id, roomname=None, floor=None, capacity=None):
        """Update room details."""
        room = self.room_repo.get_by_id(room_id)
        if not room:
            raise ValueError("Room not found")

        if roomname is not None:
            room.roomname = roomname
        if floor is not None:
            room.floor = int(floor)
        if capacity is not None:
            room.capacity = int(capacity)

        return self.room_repo.update(room)

    def delete_room(self, room_id):
        """Delete a room."""
        return self.room_repo.delete_by_id(room_id)

    def get_rooms_by_floor(self, floor):
        """Get all rooms on a specific floor."""
        return self.room_repo.find_by_floor(floor)

    def find_available_rooms(self, time_begin, time_finish, min_capacity=None):
        """Find available rooms for a time slot."""
        return self.room_repo.find_available_rooms(
            time_begin, time_finish, min_capacity
        )

    def get_floors(self):
        """Get list of all floor numbers."""
        return self.room_repo.get_floors()

    def room_exists(self, room_id):
        """Check if room exists."""
        return self.room_repo.exists(room_id)
