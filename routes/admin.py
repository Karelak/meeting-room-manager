from flask import Blueprint, request, redirect, url_for, session, flash
from models import db, Employee

admin_bp = Blueprint("admin", __name__)


def is_logged_in():
    return "employeeid" in session


@admin_bp.route("/admin/users/new", methods=["POST"])
def admin_create_user():
    if not is_logged_in() or session.get("role") != "admin":
        flash("Access denied", "error")
        return redirect(url_for("dashboard.dashboard"))

    fname = request.form.get("fname", "").strip()
    lname = request.form.get("lname", "").strip()
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")
    role = request.form.get("role", "").strip()

    # Check if all fields are provided
    if not all([fname, lname, email, password, role]):
        flash("All fields are required", "error")
        return redirect(url_for("dashboard.admin_dashboard"))

    # Validate role
    if role not in ["staff", "senior", "admin"]:
        flash("Invalid role selected", "error")
        return redirect(url_for("dashboard.admin_dashboard"))

    # Validate email domain
    if not email.endswith("@caa.co.uk"):
        flash("Email must be a valid @caa.co.uk address", "error")
        return redirect(url_for("dashboard.admin_dashboard"))

    # Validate password length
    if len(password) < 8:
        flash("Password must be at least 8 characters long", "error")
        return redirect(url_for("dashboard.admin_dashboard"))

    # Validate name lengths
    if len(fname) < 2 or len(lname) < 2:
        flash("First and last names must be at least 2 characters long", "error")
        return redirect(url_for("dashboard.admin_dashboard"))

    # Check for existing email
    existing = Employee.query.filter_by(email=email).first()
    if existing:
        flash("Email already exists", "error")
        return redirect(url_for("dashboard.admin_dashboard"))

    try:
        employee = Employee(
            fname=fname, lname=lname, email=email, password=password, role=role
        )
        db.session.add(employee)
        db.session.commit()
        flash("User created successfully", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error creating user: {str(e)}", "error")

    return redirect(url_for("dashboard.admin_dashboard"))
