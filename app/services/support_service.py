"""Support ticket management service."""
from app.repositories.support_repository import SupportRepository
from app.repositories.admin_repository import AdminRepository


class SupportService:
    """Service for support ticket-related business logic."""

    def __init__(self):
        self.support_repo = SupportRepository()
        self.admin_repo = AdminRepository()

    def create_ticket(self, employee_id, subject, message):
        """Create a new support ticket."""
        # Validate inputs
        if not subject or not subject.strip():
            raise ValueError("Subject is required")

        if not message or not message.strip():
            raise ValueError("Message is required")

        # Get first admin for assignment
        admin = self.admin_repo.get_first_admin()
        if not admin:
            raise ValueError("No admin available. Please try again later.")

        # Create ticket
        ticket = self.support_repo.create_ticket(
            employee_id, admin.adminid, subject, message
        )
        return ticket

    def get_employee_tickets(self, employee_id):
        """Get all tickets for an employee."""
        return self.support_repo.get_employee_tickets_sorted(employee_id)

    def get_all_tickets(self):
        """Get all tickets sorted by date."""
        return self.support_repo.get_all_sorted()

    def get_ticket(self, ticket_id):
        """Get a specific ticket."""
        return self.support_repo.get_by_id(ticket_id)

    def delete_ticket(self, ticket_id, employee):
        """Delete a support ticket if employee has permission."""
        ticket = self.support_repo.get_by_id(ticket_id)

        if not ticket:
            raise ValueError("Ticket not found")

        if not ticket.can_be_deleted_by(employee):
            raise PermissionError("You cannot delete tickets")

        self.support_repo.delete(ticket)
        return True

    def get_admin_tickets(self, admin_id):
        """Get all tickets assigned to an admin."""
        return self.support_repo.find_by_admin(admin_id)

    def get_recent_tickets(self, days=7):
        """Get tickets created within specified days."""
        return self.support_repo.get_recent_tickets(days)

    def get_ticket_count(self):
        """Get total number of tickets."""
        return self.support_repo.count()
