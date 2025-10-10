from flask import Blueprint, render_template, redirect, url_for, session, flash
from models import db, Employee, Booking, Room, SupportTicket

dashboard_bp = Blueprint('dashboard', __name__)

def is_logged_in():
    return "employeeid" in session


def get_current_user():
    if is_logged_in():
        return db.session.get(Employee, session["employeeid"])
    return None


@dashboard_bp.route("/")
def index():
    if is_logged_in():
        return redirect(url_for("dashboard.dashboard"))
    return redirect(url_for("auth.login"))


@dashboard_bp.route("/dashboard")
def dashboard():
    if not is_logged_in():
        return redirect(url_for("auth.login"))

    user = get_current_user()
    bookings = Booking.query.filter_by(employeeid=user.employeeid).all()
    
    return render_template("dashboard/main.html", user=user, bookings=bookings)


@dashboard_bp.route("/admin/dashboard")
def admin_dashboard():
    if not is_logged_in() or session.get("role") != "admin":
        flash("Access denied", "error")
        return redirect(url_for("dashboard.dashboard"))

    user = get_current_user()
    all_bookings = Booking.query.all()
    all_employees = Employee.query.all()
    all_rooms = Room.query.all()
    tickets = SupportTicket.query.all()

    return render_template(
        "dashboard/admin.html",
        user=user,
        bookings=all_bookings,
        employees=all_employees,
        rooms=all_rooms,
        tickets=tickets,
    )
