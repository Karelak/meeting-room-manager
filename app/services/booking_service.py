"""Business logic for booking operations."""

from __future__ import annotations

from datetime import datetime, timedelta

from flask import current_app

from ..extensions import db
from ..models import Booking, BookingAttendee, Room
from .notification_service import record_notification


class BookingError(Exception):
    """Raised when booking validation fails."""


def _enforce_temporal_rules(start_ts: datetime, end_ts: datetime) -> None:
    if end_ts <= start_ts:
        raise BookingError("End time must be after start time")
    if start_ts < datetime.utcnow():
        raise BookingError("Cannot create bookings in the past")
    duration = end_ts - start_ts
    if duration > timedelta(hours=8):
        raise BookingError("Booking duration cannot exceed 8 hours")


def _has_conflict(
    room_id: int, start_ts: datetime, end_ts: datetime, booking_id: int | None = None
) -> bool:
    query = Booking.query.filter(
        Booking.room_id == room_id,
        Booking.status == "scheduled",
        Booking.start_ts < end_ts,
        Booking.end_ts > start_ts,
    )
    if booking_id:
        query = query.filter(Booking.id != booking_id)

    return db.session.query(query.exists()).scalar()  # type: ignore[attr-defined]


def _apply_buffer(start_ts: datetime, end_ts: datetime) -> tuple[datetime, datetime]:
    buffer_minutes = int(current_app.config.get("ROOM_BUFFER_MINUTES", 60))
    buffer_delta = timedelta(minutes=buffer_minutes)
    return start_ts - buffer_delta, end_ts + buffer_delta


def create_booking(
    owner_id: int,
    room_id: int,
    title: str,
    start_ts: datetime,
    end_ts: datetime,
    **kwargs,
) -> Booking:
    _enforce_temporal_rules(start_ts, end_ts)
    padded_start, padded_end = _apply_buffer(start_ts, end_ts)
    if _has_conflict(room_id, padded_start, padded_end):
        raise BookingError("Room is already booked for selected time window")

    booking = Booking(
        owner_id=owner_id,
        room_id=room_id,
        title=title,
        start_ts=start_ts,
        end_ts=end_ts,
        agenda=kwargs.get("agenda"),
        priority_level=kwargs.get("priority_level", "normal"),
        justification=kwargs.get("justification"),
    )
    attendees: list[int] = kwargs.get("attendees", [])
    db.session.add(booking)
    db.session.flush()

    for attendee_id in attendees:
        db.session.add(BookingAttendee(booking_id=booking.id, employee_id=attendee_id))

    db.session.commit()

    record_notification(
        owner_id, f"Booking '{title}' confirmed for room {booking.room.name}"
    )
    return booking


def update_booking(booking: Booking, **changes) -> Booking:
    start_ts = changes.get("start_ts", booking.start_ts)
    end_ts = changes.get("end_ts", booking.end_ts)
    _enforce_temporal_rules(start_ts, end_ts)
    padded_start, padded_end = _apply_buffer(start_ts, end_ts)
    if _has_conflict(booking.room_id, padded_start, padded_end, booking.id):
        raise BookingError("Room is already booked for the new time window")

    for key, value in changes.items():
        setattr(booking, key, value)

    db.session.commit()
    record_notification(booking.owner_id, f"Booking '{booking.title}' updated")
    return booking


def cancel_booking(booking: Booking, actor_id: int) -> None:
    booking.status = "cancelled"
    db.session.commit()
    record_notification(booking.owner_id, f"Booking '{booking.title}' cancelled")
    if booking.owner_id != actor_id:
        record_notification(
            actor_id,
            f"You cancelled booking '{booking.title}' on behalf of {booking.owner.get_full_name()}",
        )


def find_available_rooms(
    start_ts: datetime, end_ts: datetime, min_capacity: int = 1
) -> list[Room]:
    padded_start, padded_end = _apply_buffer(start_ts, end_ts)
    rooms = (
        Room.query.filter(Room.is_active.is_(True), Room.capacity >= min_capacity)
        .order_by(Room.floor, Room.name)
        .all()
    )

    available: list[Room] = []
    for room in rooms:
        if not _has_conflict(room.id, padded_start, padded_end):
            available.append(room)
    return available
