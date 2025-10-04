"""Admin model representing administrator profiles."""
from app.models import db


class Admin(db.Model):
    """Admin model for administrator-specific data."""

    __tablename__ = "admins"

    adminid = db.Column(
        db.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True
    )
    employeeid = db.Column(
        db.Integer,
        db.ForeignKey("employees.employeeid", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=True,
    )
    fname = db.Column(db.Text, nullable=False)
    lname = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False)

    # Relationships
    employee = db.relationship("Employee", back_populates="admin_profile")
    support_tickets = db.relationship(
        "SupportTicket", back_populates="admin", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Admin {self.fname} {self.lname}>"

    # Business logic methods
    def get_full_name(self):
        """Get admin's full name."""
        return f"{self.fname} {self.lname}"

    def get_pending_tickets_count(self):
        """Get count of pending support tickets."""
        return len(self.support_tickets)

    @classmethod
    def get_first_admin(cls):
        """Get the first admin (for ticket assignment)."""
        return cls.query.first()

    @classmethod
    def create_admin(cls, employee_id, fname, lname, email):
        """Factory method to create a new admin profile."""
        admin = cls(employeeid=employee_id, fname=fname, lname=lname, email=email)
        return admin
