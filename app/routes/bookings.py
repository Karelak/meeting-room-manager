"""Booking workflows."""

from __future__ import annotations

from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from ..forms.booking import BookingForm
from ..models import Booking, Room, User
from ..services.booking_service import BookingError, create_booking, update_booking

bp = Blueprint("bookings", __name__, url_prefix="/bookings")


def _inject_choices(form: BookingForm) -> None:
    form.room_id.choices = [
        (room.id, f"{room.name} (Floor {room.floor})")
        for room in Room.query.filter_by(is_active=True).all()
    ]
    form.attendees.choices = [
        (user.id, user.get_full_name())
        for user in User.query.filter(
            User.is_active.is_(True), User.id != current_user.id
        ).order_by(User.first_name)
    ]


@bp.route("/")
@login_required
def index():
    bookings = (
        Booking.query.filter_by(owner_id=current_user.id)
        .filter(Booking.status == "scheduled")
        .order_by(Booking.start_ts)
        .all()
    )
    return render_template("bookings/index.html", bookings=bookings)


@bp.route("/new", methods=["GET", "POST"])
@login_required
def create():
    form = BookingForm()
    _inject_choices(form)
    if form.validate_on_submit():
        try:
            create_booking(
                owner_id=current_user.id,
                room_id=form.room_id.data,
                title=form.title.data,
                start_ts=form.start_ts.data,
                end_ts=form.end_ts.data,
                agenda=form.agenda.data,
                attendees=form.attendees.data,
                priority_level=form.priority_level.data,
                justification=form.justification.data,
            )
        except BookingError as exc:
            flash(str(exc), "danger")
        else:
            flash("Booking created", "success")
            return redirect(url_for("bookings.index"))
    return render_template("bookings/form.html", form=form)


@bp.route("/<int:booking_id>/edit", methods=["GET", "POST"])
@login_required
def edit(booking_id: int):
    booking = Booking.query.get_or_404(booking_id)
    if booking.owner_id != current_user.id and current_user.role != "admin":
        flash("You can only edit your own bookings", "warning")
        return redirect(url_for("bookings.index"))

    form = BookingForm(obj=booking)
    _inject_choices(form)
    if form.validate_on_submit():
        try:
            update_booking(
                booking,
                room_id=form.room_id.data,
                title=form.title.data,
                agenda=form.agenda.data,
                start_ts=form.start_ts.data,
                end_ts=form.end_ts.data,
                priority_level=form.priority_level.data,
                justification=form.justification.data,
            )
        except BookingError as exc:
            flash(str(exc), "danger")
        else:
            flash("Booking updated", "success")
            return redirect(url_for("bookings.index"))
    return render_template("bookings/form.html", form=form, booking=booking)


@bp.route("/<int:booking_id>/cancel", methods=["POST"])
@login_required
def cancel(booking_id: int):
    booking = Booking.query.get_or_404(booking_id)
    if booking.owner_id != current_user.id and current_user.role != "admin":
        flash("You can only cancel your own bookings", "warning")
        return redirect(url_for("bookings.index"))
    booking.status = "cancelled"
    booking.updated_at = datetime.utcnow()
    from ..extensions import db

    db.session.commit()
    flash("Booking cancelled", "info")
    return redirect(url_for("bookings.index"))
