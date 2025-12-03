"""Admin console."""

from __future__ import annotations

from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import login_required

from ..forms.room import RoomForm
from ..forms.user import UserForm
from ..models import Booking, Room, User
from ..services.room_service import create_room
from ..services.user_service import create_user
from ..utils.security import role_required

bp = Blueprint("admin", __name__, url_prefix="/admin")


@bp.route("/")
@login_required
@role_required("admin")
def dashboard():
    room_form = RoomForm()
    user_form = UserForm()
    stats = {
        "rooms": Room.query.count(),
        "bookings": Booking.query.count(),
        "users": User.query.count(),
    }
    return render_template(
        "admin/dashboard.html", room_form=room_form, user_form=user_form, stats=stats
    )


@bp.route("/rooms", methods=["POST"])
@login_required
@role_required("admin")
def create_room_view():
    form = RoomForm()
    if form.validate_on_submit():
        create_room(
            name=form.name.data,
            floor=form.floor.data,
            capacity=form.capacity.data,
            equipment=form.equipment.data,
            notes=form.notes.data,
            is_active=form.is_active.data,
        )
        flash("Room created", "success")
    else:
        flash("Fix validation errors", "danger")
    return redirect(url_for("admin.dashboard"))


@bp.route("/users", methods=["POST"])
@login_required
@role_required("admin")
def create_user_view():
    form = UserForm()
    if form.validate_on_submit():
        create_user(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data.lower(),
            role=form.role.data,
            password=form.password.data or "Passw0rd!",
        )
        flash("User created", "success")
    else:
        flash("Fix validation errors", "danger")
    return redirect(url_for("admin.dashboard"))
