"""Repository for Admin data access."""
from app.repositories.base_repository import BaseRepository
from app.models.admin import Admin


class AdminRepository(BaseRepository):
    """Repository for Admin-specific queries."""

    def __init__(self):
        super().__init__(Admin)

    def find_by_employee_id(self, employee_id):
        """Find admin by employee ID."""
        return self.model.query.filter_by(employeeid=employee_id).first()

    def find_by_email(self, email):
        """Find admin by email."""
        return self.model.query.filter_by(email=email).first()

    def get_first_admin(self):
        """Get the first admin (for default ticket assignment)."""
        return Admin.get_first_admin()

    def create_admin(self, employee_id, fname, lname, email):
        """Create and save a new admin profile."""
        admin = Admin.create_admin(employee_id, fname, lname, email)
        return self.save(admin)

    def admin_exists(self):
        """Check if any admin exists."""
        return self.count() > 0
