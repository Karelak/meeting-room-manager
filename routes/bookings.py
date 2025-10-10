from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models import db, Employee, Room, Booking
from datetime import datetime

bookings_bp = Blueprint("bookings", __name__)


def is_logged_in():
    return "employeeid" in session


def get_current_user():
    if is_logged_in():
        return db.session.get(Employee, session["employeeid"])
    return None


@bookings_bp.route("/bookings")
def bookings():
    if not is_logged_in():
        return redirect(url_for("auth.login"))

    user = get_current_user()
    user_bookings = Booking.query.filter_by(employeeid=user.employeeid).all()

    return render_template("bookings/list.html", user=user, bookings=user_bookings)


@bookings_bp.route("/bookings/new", methods=["GET", "POST"])
def new_booking():
    if not is_logged_in():
        return redirect(url_for("auth.login"))

    user = get_current_user()

    if request.method == "POST":
        roomid = request.form.get("roomid")
        timebegin = request.form.get("timebegin")
        timefinish = request.form.get("timefinish")

        # Validate all fields are provided
        if not all([roomid, timebegin, timefinish]):
            flash("All fields are required", "error")
            rooms = Room.query.all()
            return render_template("bookings/new.html", user=user, rooms=rooms)

        # Validate room exists
        room = Room.query.get(roomid)
        if not room:
            flash("Invalid room selected", "error")
            rooms = Room.query.all()
            return render_template("bookings/new.html", user=user, rooms=rooms)

        # Validate datetime format and parse
        try:
            begin_dt = datetime.fromisoformat(timebegin)
            finish_dt = datetime.fromisoformat(timefinish)
        except ValueError:
            flash("Invalid date/time format", "error")
            rooms = Room.query.all()
            return render_template("bookings/new.html", user=user, rooms=rooms)

        # Validate finish time is after begin time
        if finish_dt <= begin_dt:
            flash("End time must be after start time", "error")
            rooms = Room.query.all()
            return render_template("bookings/new.html", user=user, rooms=rooms)

        # Validate booking is not in the past
        if begin_dt < datetime.now():
            flash("Cannot create bookings in the past", "error")
            rooms = Room.query.all()
            return render_template("bookings/new.html", user=user, rooms=rooms)

        # Validate booking duration (going with with 8 hrs since nobody doing a )
        duration = finish_dt - begin_dt
        duration_hours = duration.total_seconds() / 3600
        if duration_hours > 8:
            flash("Booking duration cannot exceed 8 hours", "error")
            rooms = Room.query.all()
            return render_template("bookings/new.html", user=user, rooms=rooms)

        # Check for conflicts
        conflicts = Booking.query.filter(
            Booking.roomid == roomid,
            Booking.timebegin < timefinish,
            Booking.timefinish > timebegin,
        ).first()

        if conflicts:
            flash("This room is already booked for the selected time", "error")
            rooms = Room.query.all()
            return render_template("bookings/new.html", user=user, rooms=rooms)

        try:
            booking = Booking(
                employeeid=user.employeeid,
                roomid=roomid,
                timebegin=timebegin,
                timefinish=timefinish,
            )
            db.session.add(booking)
            db.session.commit()
            flash("Booking created successfully", "success")
            return redirect(url_for("bookings.bookings"))
        except Exception as e:
            db.session.rollback()
            flash(f"Error creating booking: {str(e)}", "error")
            rooms = Room.query.all()
            return render_template("bookings/new.html", user=user, rooms=rooms)

    rooms = Room.query.all()
    return render_template("bookings/new.html", user=user, rooms=rooms)


@bookings_bp.route("/bookings/<int:booking_id>/cancel", methods=["POST"])
def cancel_booking(booking_id):
    if not is_logged_in():
        return redirect(url_for("auth.login"))

    user = get_current_user()
    booking = Booking.query.get_or_404(booking_id)

    if booking.employeeid != user.employeeid and user.role != "admin":
        flash("You can only cancel your own bookings", "error")
        return redirect(url_for("bookings.bookings"))

    db.session.delete(booking)
    db.session.commit()
    flash("Booking cancelled successfully", "success")

    return redirect(url_for("bookings.bookings"))
