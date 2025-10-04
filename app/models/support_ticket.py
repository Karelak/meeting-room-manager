"""Support ticket model for help requests."""
from datetime import datetime
from app.models import db


class SupportTicket(db.Model):
    """Support ticket model for employee help requests."""

    __tablename__ = "supporttickets"

    ticketid = db.Column(
        db.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True
    )
    employeeid = db.Column(
        db.Integer,
        db.ForeignKey("employees.employeeid", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    adminid = db.Column(
        db.Integer,
        db.ForeignKey("admins.adminid", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    subject = db.Column(db.Text, nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(
        db.Text, nullable=False, default=lambda: datetime.now().isoformat()
    )

    # Relationships
    employee = db.relationship("Employee", back_populates="support_tickets")
    admin = db.relationship("Admin", back_populates="support_tickets")

    def __repr__(self):
        return f"<SupportTicket {self.ticketid} - {self.subject}>"

    # Business logic methods
    def get_created_date(self):
        """Get formatted creation date."""
        try:
            created = datetime.fromisoformat(self.created_at)
            return created.strftime("%Y-%m-%d %H:%M")
        except (ValueError, TypeError):
            return self.created_at

    def is_recent(self, days=7):
        """Check if ticket was created within specified days."""
        try:
            created = datetime.fromisoformat(self.created_at)
            age = (datetime.now() - created).days
            return age <= days
        except (ValueError, TypeError):
            return False

    def can_be_deleted_by(self, employee):
        """Check if employee can delete this ticket."""
        return employee.can_delete_ticket(self)

    @classmethod
    def create_ticket(cls, employee_id, admin_id, subject, message):
        """Factory method to create a new support ticket."""
        ticket = cls(
            employeeid=employee_id, adminid=admin_id, subject=subject, message=message
        )
        return ticket

    @classmethod
    def find_by_employee(cls, employee_id):
        """Find all tickets for a specific employee."""
        return cls.query.filter_by(employeeid=employee_id).all()

    @classmethod
    def find_by_admin(cls, admin_id):
        """Find all tickets assigned to a specific admin."""
        return cls.query.filter_by(adminid=admin_id).all()
