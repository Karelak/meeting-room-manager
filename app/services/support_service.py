"""Support ticket logic."""

from __future__ import annotations

from ..extensions import db
from ..models import SupportTicket


def create_ticket(
    employee_id: int, subject: str, body: str, admin_id: int | None = None
) -> SupportTicket:
    ticket = SupportTicket(
        employee_id=employee_id, admin_id=admin_id, subject=subject, body=body
    )
    db.session.add(ticket)
    db.session.commit()
    return ticket


def close_ticket(ticket: SupportTicket, admin_id: int) -> None:
    ticket.status = "closed"
    ticket.admin_id = admin_id
    db.session.commit()
