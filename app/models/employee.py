"""Employee model with authentication and authorization logic."""
from app.models import db


class Employee(db.Model):
    """Employee model representing system users."""

    __tablename__ = "employees"

    employeeid = db.Column(
        db.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True
    )
    fname = db.Column(db.Text, nullable=False)
    lname = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False)
    password = db.Column(db.Text, nullable=False)
    role = db.Column(db.Text, nullable=False, default="staff")

    # Relationships
    bookings = db.relationship(
        "Booking", back_populates="employee", cascade="all, delete-orphan"
    )
    support_tickets = db.relationship(
        "SupportTicket", back_populates="employee", cascade="all, delete-orphan"
    )
    admin_profile = db.relationship(
        "Admin", back_populates="employee", uselist=False, cascade="all, delete-orphan"
    )

    __table_args__ = (
        db.CheckConstraint("role IN ('staff', 'senior', 'admin')", name="check_role"),
    )

    def __repr__(self):
        return f"<Employee {self.fname} {self.lname}>"

    # Business logic methods
    def is_admin(self):
        """Check if employee has admin role."""
        return self.role == "admin"

    def is_senior(self):
        """Check if employee has senior role."""
        return self.role == "senior"

    def check_password(self, password):
        """Verify password (in production, use proper hashing)."""
        return self.password == password

    def get_full_name(self):
        """Get employee's full name."""
        return f"{self.fname} {self.lname}"

    def can_cancel_booking(self, booking):
        """Check if this employee can cancel a specific booking."""
        return booking.employeeid == self.employeeid or self.is_admin()

    def can_delete_ticket(self, ticket):
        """Check if this employee can delete a support ticket."""
        return self.is_admin()

    @classmethod
    def authenticate(cls, email, password):
        """Authenticate an employee with email and password."""
        employee = cls.query.filter_by(email=email).first()
        if employee and employee.check_password(password):
            return employee
        return None

    @classmethod
    def find_by_email(cls, email):
        """Find employee by email address."""
        return cls.query.filter_by(email=email).first()

    @classmethod
    def create_employee(cls, fname, lname, email, password, role="staff"):
        """Factory method to create a new employee."""
        employee = cls(
            fname=fname, lname=lname, email=email, password=password, role=role
        )
        return employee
