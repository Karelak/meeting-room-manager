"""Endpoints for room screen kiosks."""

from __future__ import annotations

from datetime import datetime

from flask import Blueprint, abort, jsonify, render_template, request

from ..extensions import db
from ..models import Booking, Room, RoomTerminal

bp = Blueprint("terminals", __name__, url_prefix="/terminals")


def _resolve_device(key: str) -> RoomTerminal:
    terminal = RoomTerminal.query.filter_by(device_key=key).first()
    if not terminal:
        abort(404)
    terminal.last_seen = datetime.utcnow()
    db.session.commit()
    return terminal


@bp.route("/<device_key>")
def screen(device_key: str):
    terminal = _resolve_device(device_key)
    room = Room.query.get_or_404(terminal.room_id)
    now = datetime.utcnow()
    current_booking = (
        Booking.query.filter(
            Booking.room_id == room.id,
            Booking.start_ts <= now,
            Booking.end_ts >= now,
            Booking.status == "scheduled",
        )
        .order_by(Booking.start_ts)
        .first()
    )
    upcoming = (
        Booking.query.filter(Booking.room_id == room.id, Booking.start_ts >= now)
        .order_by(Booking.start_ts)
        .limit(3)
        .all()
    )
    return render_template(
        "terminals/screen.html",
        room=room,
        current_booking=current_booking,
        upcoming=upcoming,
    )


@bp.route("/<device_key>/check-in", methods=["POST"])
def check_in(device_key: str):
    terminal = _resolve_device(device_key)
    room = Room.query.get_or_404(terminal.room_id)
    badge = request.json.get("employee_id")
    if not badge:
        abort(400)
    now = datetime.utcnow()
    booking = (
        Booking.query.filter(
            Booking.room_id == room.id,
            Booking.start_ts <= now,
            Booking.end_ts >= now,
            Booking.status == "scheduled",
        )
        .order_by(Booking.start_ts)
        .first()
    )
    if not booking:
        return jsonify({"status": "no-active-booking"}), 200
    booking.status = "in-progress"
    db.session.commit()
    return jsonify({"status": "checked-in", "bookingId": booking.id})
