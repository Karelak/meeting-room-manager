from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models import db, Employee, Room, Booking

rooms_bp = Blueprint('rooms', __name__)

def is_logged_in():
    return "employeeid" in session


def get_current_user():
    if is_logged_in():
        return db.session.get(Employee, session["employeeid"])
    return None


@rooms_bp.route("/rooms")
def rooms():
    if not is_logged_in():
        return redirect(url_for("auth.login"))

    user = get_current_user()
    all_rooms = Room.query.order_by(Room.floor, Room.roomname).all()

    return render_template("rooms/list.html", user=user, rooms=all_rooms)


@rooms_bp.route("/rooms/<int:room_id>")
def room_detail(room_id):
    if not is_logged_in():
        return redirect(url_for("auth.login"))

    user = get_current_user()
    room = Room.query.get_or_404(room_id)
    bookings = Booking.query.filter_by(roomid=room_id).all()

    return render_template("rooms/detail.html", user=user, room=room, bookings=bookings)


@rooms_bp.route("/admin/rooms/new", methods=["POST"])
def admin_create_room():
    if not is_logged_in() or session.get("role") != "admin":
        flash("Access denied", "error")
        return redirect(url_for("dashboard.dashboard"))

    roomname = request.form.get("roomname")
    floor = request.form.get("floor")
    capacity = request.form.get("capacity")

    if roomname and floor and capacity:
        room = Room(roomname=roomname, floor=int(floor), capacity=int(capacity))
        db.session.add(room)
        db.session.commit()
        flash("Room created successfully", "success")
    else:
        flash("All fields are required", "error")

    return redirect(url_for("dashboard.admin_dashboard"))
