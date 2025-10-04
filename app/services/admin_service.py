"""Admin management service."""
from app.repositories.employee_repository import EmployeeRepository
from app.repositories.admin_repository import AdminRepository
from app.repositories.booking_repository import BookingRepository
from app.repositories.room_repository import RoomRepository
from app.repositories.support_repository import SupportRepository


class AdminService:
    """Service for admin-specific operations."""

    def __init__(self):
        self.employee_repo = EmployeeRepository()
        self.admin_repo = AdminRepository()
        self.booking_repo = BookingRepository()
        self.room_repo = RoomRepository()
        self.support_repo = SupportRepository()

    def create_user(self, fname, lname, email, password, role):
        """Create a new user (admin operation)."""
        # Validate inputs
        if not all([fname, lname, email, password, role]):
            raise ValueError("All fields are required")

        if role not in ["staff", "senior", "admin"]:
            raise ValueError("Invalid role")

        # Check if email exists
        if self.employee_repo.email_exists(email):
            raise ValueError("Email already exists")

        # Create employee
        employee = self.employee_repo.create_employee(
            fname, lname, email, password, role
        )

        # If admin role, create admin profile
        if role == "admin":
            self.admin_repo.create_admin(
                employee_id=employee.employeeid,
                fname=fname,
                lname=lname,
                email=email,
            )

        return employee

    def get_all_employees(self):
        """Get all employees."""
        return self.employee_repo.get_all()

    def get_all_bookings(self):
        """Get all bookings."""
        return self.booking_repo.get_all()

    def get_all_rooms(self):
        """Get all rooms."""
        return self.room_repo.get_all_sorted()

    def get_all_tickets(self):
        """Get all support tickets."""
        return self.support_repo.get_all_sorted()

    def get_dashboard_stats(self):
        """Get statistics for admin dashboard."""
        return {
            "total_employees": self.employee_repo.count(),
            "total_rooms": self.room_repo.count(),
            "total_bookings": self.booking_repo.count(),
            "total_tickets": self.support_repo.count(),
            "active_bookings": len(self.booking_repo.get_active_bookings()),
            "future_bookings": len(self.booking_repo.get_future_bookings()),
        }

    def delete_employee(self, employee_id):
        """Delete an employee (admin operation)."""
        return self.employee_repo.delete_by_id(employee_id)

    def get_employee(self, employee_id):
        """Get a specific employee."""
        return self.employee_repo.get_by_id(employee_id)
