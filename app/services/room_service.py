"""Room helper routines."""

from __future__ import annotations

from ..extensions import db
from ..models import Room


def save_room(room: Room, **changes) -> Room:
    for key, value in changes.items():
        setattr(room, key, value)
    db.session.add(room)
    db.session.commit()
    return room


def create_room(**data) -> Room:
    room = Room(**data)
    db.session.add(room)
    db.session.commit()
    return room
