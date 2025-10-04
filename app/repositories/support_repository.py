"""Repository for SupportTicket data access."""
from app.repositories.base_repository import BaseRepository
from app.models.support_ticket import SupportTicket


class SupportRepository(BaseRepository):
    """Repository for SupportTicket-specific queries."""

    def __init__(self):
        super().__init__(SupportTicket)

    def find_by_employee(self, employee_id):
        """Find all tickets for an employee."""
        return self.model.query.filter_by(employeeid=employee_id).all()

    def find_by_admin(self, admin_id):
        """Find all tickets assigned to an admin."""
        return self.model.query.filter_by(adminid=admin_id).all()

    def get_recent_tickets(self, days=7):
        """Get tickets created within specified days."""
        return [t for t in self.get_all() if t.is_recent(days)]

    def create_ticket(self, employee_id, admin_id, subject, message):
        """Create and save a new support ticket."""
        ticket = SupportTicket.create_ticket(employee_id, admin_id, subject, message)
        return self.save(ticket)

    def get_employee_tickets_sorted(self, employee_id):
        """Get employee tickets sorted by creation date."""
        return (
            self.model.query.filter_by(employeeid=employee_id)
            .order_by(self.model.created_at.desc())
            .all()
        )

    def get_all_sorted(self):
        """Get all tickets sorted by creation date."""
        return self.model.query.order_by(self.model.created_at.desc()).all()
