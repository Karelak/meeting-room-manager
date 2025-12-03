"""Dashboard and home views."""

from __future__ import annotations

from datetime import datetime, timedelta

from flask import Blueprint, render_template
from flask_login import current_user, login_required

from ..models import Booking, Notification, Room

bp = Blueprint("dashboard", __name__)


@bp.route("/")
@login_required
def home():
    upcoming = (
        Booking.query.filter(
            Booking.owner_id == current_user.id,
            Booking.start_ts >= datetime.utcnow() - timedelta(hours=1),
            Booking.status == "scheduled",
        )
        .order_by(Booking.start_ts)
        .limit(5)
        .all()
    )
    notices = (
        Notification.query.filter_by(employee_id=current_user.id, read_at=None)
        .order_by(Notification.created_at.desc())
        .limit(5)
        .all()
    )
    rooms = Room.query.filter_by(is_active=True).order_by(Room.floor).limit(6).all()
    return render_template(
        "dashboard/home.html", upcoming=upcoming, notices=notices, rooms=rooms
    )
