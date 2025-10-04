"""Application entry point."""
from app import create_app
from app.services.auth_service import AuthService
from app.models import db, Employee, Admin, Room, Booking, SupportTicket


def init_database(app):
    """Initialize database with tables and demo data."""
    with app.app_context():
        # Create all tables
        db.create_all()

        # Initialize admin account if no employees exist
        auth_service = AuthService()
        auth_service.initialize_admin_account()

        print("Database initialized")


def generate_demo_data(app):
    """Generate demo data for testing."""
    with app.app_context():
        # Check if demo data already exists
        if Employee.query.filter_by(email="jane.doe@example.com").first():
            print("Demo data already exists")
            return

        # Create demo staff user
        staff_employee = Employee(
            fname="Jane",
            lname="Doe",
            email="jane.doe@example.com",
            password="password123",
            role="staff",
        )
        db.session.add(staff_employee)
        db.session.flush()

        # Create demo rooms
        rooms_data = [
            {"roomname": "Alpha", "floor": 1, "capacity": 4},
            {"roomname": "Beta", "floor": 1, "capacity": 8},
            {"roomname": "Gamma", "floor": 2, "capacity": 12},
            {"roomname": "Delta", "floor": 3, "capacity": 20},
        ]

        rooms = []
        for room_data in rooms_data:
            if not Room.query.filter_by(roomname=room_data["roomname"]).first():
                room = Room(**room_data)
                db.session.add(room)
                rooms.append(room)

        db.session.flush()

        # Create demo bookings
        if len(rooms) >= 2:
            booking1 = Booking(
                employeeid=staff_employee.employeeid,
                roomid=rooms[0].roomid,
                timebegin="2025-10-10 09:00",
                timefinish="2025-10-10 10:00",
            )
            booking2 = Booking(
                employeeid=staff_employee.employeeid,
                roomid=rooms[1].roomid,
                timebegin="2025-10-10 11:00",
                timefinish="2025-10-10 12:00",
            )
            db.session.add_all([booking1, booking2])

        # Ensure admin exists
        admin = Admin.query.first()
        if not admin:
            admin_employee = Employee.query.filter_by(email="admin@caa.co.uk").first()
            if admin_employee:
                admin = Admin(
                    employeeid=admin_employee.employeeid,
                    fname=admin_employee.fname,
                    lname=admin_employee.lname,
                    email=admin_employee.email,
                )
                db.session.add(admin)
                db.session.flush()

        # Create demo support ticket
        if admin:
            ticket = SupportTicket(
                employeeid=staff_employee.employeeid,
                adminid=admin.adminid,
                subject="Demo: Assistance needed",
                message="This is a demo support ticket.",
            )
            db.session.add(ticket)

        db.session.commit()
        print("Demo data generated")


if __name__ == "__main__":
    # Create app instance
    app = create_app()

    # Initialize database
    init_database(app)

    # Generate demo data for testing
    generate_demo_data(app)

    # Run the application
    app.run(debug=True)
