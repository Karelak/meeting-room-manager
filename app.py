from flask import Flask, render_template, request, redirect, url_for, session, flash
from models import db, Employee, Room, Booking, Admin, SupportTicket

app = Flask(__name__)
app.config["SECRET_KEY"] = "dev-secret-key-change-in-production"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///meeting_rooms.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db.init_app(app)


def is_logged_in():
    return "employeeid" in session


def get_current_user():
    if is_logged_in():
        return db.session.get(Employee, session["employeeid"])
    return None


@app.route("/")
def index():
    if is_logged_in():
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        employee = Employee.query.filter_by(email=email).first()
        if employee and employee.password == password:
            session["employeeid"] = employee.employeeid
            session["role"] = employee.role
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid email or password", "error")

    return render_template("auth/login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out", "info")
    return redirect(url_for("login"))


@app.route("/dashboard")
def dashboard():
    if not is_logged_in():
        return redirect(url_for("login"))

    user = get_current_user()
    bookings = Booking.query.filter_by(employeeid=user.employeeid).all()

    return render_template("dashboard/main.html", user=user, bookings=bookings)


@app.route("/admin/dashboard")
def admin_dashboard():
    if not is_logged_in() or session.get("role") != "admin":
        flash("Access denied", "error")
        return redirect(url_for("dashboard"))

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


@app.route("/rooms")
def rooms():
    if not is_logged_in():
        return redirect(url_for("login"))

    user = get_current_user()
    all_rooms = Room.query.order_by(Room.floor, Room.roomname).all()

    return render_template("rooms/list.html", user=user, rooms=all_rooms)


@app.route("/rooms/<int:room_id>")
def room_detail(room_id):
    if not is_logged_in():
        return redirect(url_for("login"))

    user = get_current_user()
    room = Room.query.get_or_404(room_id)
    bookings = Booking.query.filter_by(roomid=room_id).all()

    return render_template("rooms/detail.html", user=user, room=room, bookings=bookings)


@app.route("/bookings")
def bookings():
    if not is_logged_in():
        return redirect(url_for("login"))

    user = get_current_user()
    user_bookings = Booking.query.filter_by(employeeid=user.employeeid).all()

    return render_template("bookings/list.html", user=user, bookings=user_bookings)


@app.route("/bookings/new", methods=["GET", "POST"])
def new_booking():
    if not is_logged_in():
        return redirect(url_for("login"))

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
            return redirect(url_for("bookings"))

    rooms = Room.query.all()
    return render_template("bookings/new.html", user=user, rooms=rooms)


@app.route("/bookings/<int:booking_id>/cancel", methods=["POST"])
def cancel_booking(booking_id):
    if not is_logged_in():
        return redirect(url_for("login"))

    user = get_current_user()
    booking = Booking.query.get_or_404(booking_id)

    if booking.employeeid != user.employeeid and user.role != "admin":
        flash("You can only cancel your own bookings", "error")
        return redirect(url_for("bookings"))

    db.session.delete(booking)
    db.session.commit()
    flash("Booking cancelled successfully", "success")

    return redirect(url_for("bookings"))


@app.route("/support", methods=["GET", "POST"])
def support():
    if not is_logged_in():
        return redirect(url_for("login"))

    user = get_current_user()

    if request.method == "POST":
        subject = request.form.get("subject")
        message = request.form.get("message")

        admin = Admin.query.first()
        if admin:
            ticket = SupportTicket(
                employeeid=user.employeeid,
                adminid=admin.adminid,
                subject=subject,
                message=message,
            )
            db.session.add(ticket)
            db.session.commit()
            flash("Support ticket submitted successfully", "success")
            return redirect(url_for("support"))
        else:
            flash("No admin available. Please try again later.", "error")

    tickets = SupportTicket.query.filter_by(employeeid=user.employeeid).all()
    return render_template("support/form.html", user=user, tickets=tickets)


@app.route("/admin/rooms/new", methods=["POST"])
def admin_create_room():
    if not is_logged_in() or session.get("role") != "admin":
        flash("Access denied", "error")
        return redirect(url_for("dashboard"))

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

    return redirect(url_for("admin_dashboard"))


@app.route("/admin/users/new", methods=["POST"])
def admin_create_user():
    if not is_logged_in() or session.get("role") != "admin":
        flash("Access denied", "error")
        return redirect(url_for("dashboard"))

    fname = request.form.get("fname")
    lname = request.form.get("lname")
    email = request.form.get("email")
    password = request.form.get("password")
    role = request.form.get("role")

    if fname and lname and email and password and role:
        # Check if email already exists
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

    return redirect(url_for("admin_dashboard"))


def init_db():
    with app.app_context():
        db.create_all()
        # Create admin account if no employees exist
        if Employee.query.count() == 0:
            admin_employee = Employee(
                fname="Admin",
                lname="User",
                email="admin@caa.co.uk",
                password="admin123",
                role="admin",
            )
            db.session.add(admin_employee)
            db.session.flush()  # Flush to get the employeeid

            admin = Admin(
                employeeid=admin_employee.employeeid,
                fname="Admin",
                lname="User",
                email="admin@caa.co.uk",
            )
            db.session.add(admin)

            db.session.commit()
            print("Database initialized with admin account")

def generate_demo_data():
    with app.app_context():
        # Ensure tables exist (safe if already created)
        db.create_all()

        # 1 staff user
        staff_email = "jane.doe@example.com"
        employee = Employee.query.filter_by(email=staff_email).first()
        if not employee:
            employee = Employee(
                fname="Jane",
                lname="Doe",
                email=staff_email,
                password="password123",
                role="staff",
            )
            db.session.add(employee)
            db.session.flush()  # get employeeid

        # 4 rooms
        rooms_to_create = [
            {"roomname": "Alpha", "floor": 1, "capacity": 4},
            {"roomname": "Beta", "floor": 1, "capacity": 8},
            {"roomname": "Gamma", "floor": 2, "capacity": 12},
            {"roomname": "Delta", "floor": 3, "capacity": 20},
        ]
        for r in rooms_to_create:
            if not Room.query.filter_by(roomname=r["roomname"]).first():
                db.session.add(Room(**r))
        db.session.flush()

        # 2 bookings for that user (only if they have none)
        if Booking.query.filter_by(employeeid=employee.employeeid).count() == 0:
            room_alpha = Room.query.filter_by(roomname="Alpha").first() or Room.query.first()
            room_beta = Room.query.filter_by(roomname="Beta").first() or room_alpha

            booking1 = Booking(
                employeeid=employee.employeeid,
                roomid=room_alpha.roomid,
                timebegin="2025-10-10 09:00",
                timefinish="2025-10-10 10:00",
            )
            booking2 = Booking(
                employeeid=employee.employeeid,
                roomid=room_beta.roomid,
                timebegin="2025-10-10 11:00",
                timefinish="2025-10-10 12:00",
            )
            db.session.add_all([booking1, booking2])

        db.session.commit()
        print("Demo data generated.")


if __name__ == "__main__":
    init_db()
    generate_demo_data() # testing purposes
    app.run(debug=True)
