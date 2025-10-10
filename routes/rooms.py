from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models import db, Employee, Room, Booking

rooms_bp = Blueprint("rooms", __name__)


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

    roomname = request.form.get("roomname", "").strip()
    floor = request.form.get("floor", "").strip()
    capacity = request.form.get("capacity", "").strip()

    # Check if all fields are provided
    if not all([roomname, floor, capacity]):
        flash("All fields are required", "error")
        return redirect(url_for("dashboard.admin_dashboard"))

    # Validate room name length
    if len(roomname) < 1:
        flash("Room name cannot be empty", "error")
        return redirect(url_for("dashboard.admin_dashboard"))

    # Validate floor is a valid integer
    try:
        floor_num = int(floor)
    except ValueError:
        flash("Floor must be a valid number", "error")
        return redirect(url_for("dashboard.admin_dashboard"))

    # Validate floor is non-negative
    if floor_num < 0:
        flash("Floor must be 0 or greater", "error")
        return redirect(url_for("dashboard.admin_dashboard"))

    # Validate capacity is a valid integer
    try:
        capacity_num = int(capacity)
    except ValueError:
        flash("Capacity must be a valid number", "error")
        return redirect(url_for("dashboard.admin_dashboard"))

    # Validate capacity is positive
    if capacity_num <= 0:
        flash("Capacity must be greater than 0", "error")
        return redirect(url_for("dashboard.admin_dashboard"))

    # Validate reasonable capacity limit, 200 is max for the building
    if capacity_num > 200:
        flash("Capacity cannot exceed 200", "error")
        return redirect(url_for("dashboard.admin_dashboard"))

    # Check for duplicate room on same floor
    existing_room = Room.query.filter_by(floor=floor_num, roomname=roomname).first()
    if existing_room:
        flash("A room with this name already exists on this floor", "error")
        return redirect(url_for("dashboard.admin_dashboard"))

    try:
        room = Room(roomname=roomname, floor=floor_num, capacity=capacity_num)
        db.session.add(room)
        db.session.commit()
        flash("Room created successfully", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error creating room: {str(e)}", "error")

    return redirect(url_for("dashboard.admin_dashboard"))
