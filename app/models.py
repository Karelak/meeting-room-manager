"""Database models."""

from __future__ import annotations

from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from .extensions import db


class TimestampMixin:
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )


class User(db.Model, UserMixin, TimestampMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(255), unique=True, index=True, nullable=False)
    role = db.Column(db.String(20), default="staff", nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, default=True)

    bookings = db.relationship("Booking", back_populates="owner", lazy=True)
    notifications = db.relationship(
        "Notification", back_populates="employee", lazy=True
    )

    def get_full_name(self) -> str:
        return f"{self.first_name} {self.last_name}".strip()

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


class Room(db.Model, TimestampMixin):
    __tablename__ = "rooms"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    floor = db.Column(db.Integer, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    equipment = db.Column(db.Text, default="")
    notes = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)

    bookings = db.relationship("Booking", back_populates="room", lazy=True)


class Booking(db.Model, TimestampMixin):
    __tablename__ = "bookings"

    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey("rooms.id"), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    start_ts = db.Column(db.DateTime, nullable=False, index=True)
    end_ts = db.Column(db.DateTime, nullable=False, index=True)
    title = db.Column(db.String(255), nullable=False)
    agenda = db.Column(db.Text)
    status = db.Column(db.String(20), default="scheduled", nullable=False)
    priority_level = db.Column(db.String(20), default="normal", nullable=False)
    justification = db.Column(db.Text)

    room = db.relationship("Room", back_populates="bookings")
    owner = db.relationship("User", back_populates="bookings")
    attendees = db.relationship(
        "BookingAttendee", back_populates="booking", cascade="all, delete-orphan"
    )


class BookingAttendee(db.Model, TimestampMixin):
    __tablename__ = "booking_attendees"

    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey("bookings.id"), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    response_state = db.Column(db.String(20), default="pending")

    booking = db.relationship("Booking", back_populates="attendees")
    employee = db.relationship("User")


class Notification(db.Model, TimestampMixin):
    __tablename__ = "notifications"

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    category = db.Column(db.String(30), default="info")
    message = db.Column(db.Text, nullable=False)
    read_at = db.Column(db.DateTime)

    employee = db.relationship("User", back_populates="notifications")


class SupportTicket(db.Model, TimestampMixin):
    __tablename__ = "support_tickets"

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    subject = db.Column(db.String(255), nullable=False)
    body = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default="open", nullable=False)
    resolved_at = db.Column(db.DateTime)


class AuditEvent(db.Model, TimestampMixin):
    __tablename__ = "audit_events"

    id = db.Column(db.Integer, primary_key=True)
    actor_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    action = db.Column(db.String(80), nullable=False)
    entity_type = db.Column(db.String(80), nullable=False)
    entity_id = db.Column(db.Integer, nullable=False)
    payload = db.Column(db.JSON, nullable=False, default=dict)


class RoomTerminal(db.Model, TimestampMixin):
    __tablename__ = "room_terminals"

    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey("rooms.id"), nullable=False)
    device_key = db.Column(db.String(64), unique=True, nullable=False)
    last_seen = db.Column(db.DateTime)


def seed_default_admin() -> None:
    """Ensure a default admin exists for first-run convenience."""
    if not User.query.filter_by(email="admin@caa.co.uk").first():
        admin = User(
            first_name="Default",
            last_name="Admin",
            email="admin@caa.co.uk",
            role="admin",
        )
        admin.set_password("Passw0rd!")
        db.session.add(admin)
        db.session.commit()
