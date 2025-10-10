from flask import Blueprint, request, redirect, url_for, session, flash
from models import db, Employee

admin_bp = Blueprint('admin', __name__)

def is_logged_in():
    return "employeeid" in session


@admin_bp.route("/admin/users/new", methods=["POST"])
def admin_create_user():
    if not is_logged_in() or session.get("role") != "admin":
        flash("Access denied", "error")
        return redirect(url_for("dashboard.dashboard"))

    fname = request.form.get("fname")
    lname = request.form.get("lname")
    email = request.form.get("email")
    password = request.form.get("password")
    role = request.form.get("role")

    if fname and lname and email and password and role:
        existing = Employee.query.filter_by(email=email).first()
        if existing:
            flash("Email already exists", "error")
        else:
            employee = Employee(
                fname=fname, lname=lname, email=email, password=password, role=role
            )
            db.session.add(employee)
            db.session.commit()
            flash("User created successfully", "success")
    else:
        flash("All fields are required", "error")

    return redirect(url_for("dashboard.admin_dashboard"))
