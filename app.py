from flask import Flask
from models import db, Employee, Admin, Room, Booking, SupportTicket
import os
from datetime import datetime, timedelta

# Import blueprints
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.rooms import rooms_bp
from routes.bookings import bookings_bp
from routes.support import support_bp
from routes.admin import admin_bp

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///meeting_rooms.db"
app.config["SECRET_KEY"] = os.urandom(32)


db.init_app(app)

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(rooms_bp)
app.register_blueprint(bookings_bp)
app.register_blueprint(support_bp)
app.register_blueprint(admin_bp)


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
            room_alpha = (
                Room.query.filter_by(roomname="Alpha").first() or Room.query.first()
            )
            room_beta = Room.query.filter_by(roomname="Beta").first() or room_alpha

            booking1 = Booking(
                employeeid=employee.employeeid,
                roomid=room_alpha.roomid,
                timefinish=(datetime.now() + timedelta(hours=2)).isoformat(),
            )
            booking2 = Booking(
                employeeid=employee.employeeid,
                roomid=room_beta.roomid,
                timefinish=(
                    datetime.now() + timedelta(hours=2, minutes=30)
                ).isoformat(),
            )
            db.session.add_all([booking1, booking2])

        # Ensure at least one admin exists (create a lightweight admin profile if missing)
        admin = Admin.query.first()
        if not admin:
            # Try to reuse an existing admin employee if present, otherwise create one
            admin_employee = Employee.query.filter_by(email="admin@caa.co.uk").first()
            if not admin_employee:
                admin_employee = Employee(
                    fname="Admin",
                    lname="User",
                    email="admin@caa.co.uk",
                    password="admin123",
                    role="admin",
                )
                db.session.add(admin_employee)
                db.session.flush()

            admin = Admin(
                employeeid=admin_employee.employeeid,
                fname=admin_employee.fname,
                lname=admin_employee.lname,
                email=admin_employee.email,
            )
            db.session.add(admin)
            db.session.flush()

        # Add a demo support ticket for the demo staff user if they have none
        if SupportTicket.query.filter_by(employeeid=employee.employeeid).count() == 0:
            ticket = SupportTicket(
                employeeid=employee.employeeid,
                adminid=admin.adminid,
                subject="Demo: Assistance needed",
                message="This is a demo support ticket created during demo data generation.",
            )
            db.session.add(ticket)

        db.session.commit()
        print("Demo data generated.")


if __name__ == "__main__":
    init_db()
    generate_demo_data()  # testing purposes
    app.run(debug=True)
