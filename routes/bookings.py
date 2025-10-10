from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models import db, Employee, Room, Booking

bookings_bp = Blueprint('bookings', __name__)

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

        conflicts = Booking.query.filter(
            Booking.roomid == roomid,
            Booking.timebegin < timefinish,
            Booking.timefinish > timebegin,
        ).first()

        if conflicts:
            flash("This room is already booked for the selected time", "error")
        else:
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
