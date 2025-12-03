"""Room catalogue views."""

from __future__ import annotations

from datetime import datetime

from flask import Blueprint, abort, render_template, request
from flask_login import login_required

from ..forms.booking import BookingFilterForm
from ..models import Booking, Room

bp = Blueprint("rooms", __name__, url_prefix="/rooms")


@bp.route("/", methods=["GET", "POST"])
@login_required
def index():
    form = BookingFilterForm(request.args)
    query = Room.query.filter_by(is_active=True)
    if form.min_capacity.data:
        query = query.filter(Room.capacity >= form.min_capacity.data)
    if form.floor.data:
        query = query.filter(Room.floor == form.floor.data)
    rooms = query.order_by(Room.floor, Room.name).all()
    return render_template("rooms/index.html", rooms=rooms, form=form)


@bp.route("/<int:room_id>")
@login_required
def detail(room_id: int):
    room = Room.query.get_or_404(room_id)
    upcoming = (
        Booking.query.filter(
            Booking.room_id == room.id, Booking.start_ts >= datetime.utcnow()
        )
        .order_by(Booking.start_ts)
        .limit(5)
        .all()
    )
    return render_template("rooms/detail.html", room=room, upcoming=upcoming)
