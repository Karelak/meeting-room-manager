"""Authentication and authorization service."""
from flask import session
from app.repositories.employee_repository import EmployeeRepository
from app.repositories.admin_repository import AdminRepository


class AuthService:
    """Service for authentication and authorization logic."""

    def __init__(self):
        self.employee_repo = EmployeeRepository()
        self.admin_repo = AdminRepository()

    def login(self, email, password):
        """Authenticate and log in user."""
        employee = self.employee_repo.authenticate(email, password)
        if employee:
            session["employeeid"] = employee.employeeid
            session["role"] = employee.role
            return employee
        return None

    def logout(self):
        """Log out current user."""
        session.clear()

    def get_current_user(self):
        """Get currently logged-in employee."""
        if "employeeid" in session:
            return self.employee_repo.get_by_id(session["employeeid"])
        return None

    def is_logged_in(self):
        """Check if user is logged in."""
        return "employeeid" in session

    def is_admin(self):
        """Check if current user is admin."""
        return session.get("role") == "admin"

    def is_senior(self):
        """Check if current user is senior or above."""
        role = session.get("role")
        return role in ["senior", "admin"]

    def require_login(self):
        """Check if user is logged in, return True if yes."""
        return self.is_logged_in()

    def require_admin(self):
        """Check if user is admin, return True if yes."""
        return self.is_logged_in() and self.is_admin()

    def can_access_admin_dashboard(self):
        """Check if user can access admin dashboard."""
        return self.is_admin()

    def initialize_admin_account(self):
        """Create initial admin account if none exists."""
        if self.employee_repo.count() == 0:
            # Create admin employee
            admin_employee = self.employee_repo.create_employee(
                fname="Admin",
                lname="User",
                email="admin@caa.co.uk",
                password="admin123",
                role="admin",
            )

            # Create admin profile
            self.admin_repo.create_admin(
                employee_id=admin_employee.employeeid,
                fname=admin_employee.fname,
                lname=admin_employee.lname,
                email=admin_employee.email,
            )

            return admin_employee
        return None
