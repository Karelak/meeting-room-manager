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


if __name__ == "__main__":
    init_db()
    app.run(debug=True, host="0.0.0.0", port=8000)
