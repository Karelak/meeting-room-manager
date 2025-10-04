"""Repository for Employee data access."""
from app.repositories.base_repository import BaseRepository
from app.models.employee import Employee


class EmployeeRepository(BaseRepository):
    """Repository for Employee-specific queries."""

    def __init__(self):
        super().__init__(Employee)

    def find_by_email(self, email):
        """Find employee by email."""
        return self.model.query.filter_by(email=email).first()

    def find_by_role(self, role):
        """Find all employees with a specific role."""
        return self.model.query.filter_by(role=role).all()

    def get_all_admins(self):
        """Get all admin employees."""
        return self.find_by_role("admin")

    def get_all_staff(self):
        """Get all staff employees."""
        return self.model.query.filter(self.model.role.in_(["staff", "senior"])).all()

    def email_exists(self, email):
        """Check if email already exists."""
        return self.find_by_email(email) is not None

    def authenticate(self, email, password):
        """Authenticate employee with email and password."""
        return Employee.authenticate(email, password)

    def create_employee(self, fname, lname, email, password, role="staff"):
        """Create and save a new employee."""
        employee = Employee.create_employee(fname, lname, email, password, role)
        return self.save(employee)
