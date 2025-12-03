"""Support contact workflows."""

from __future__ import annotations

from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from ..extensions import db
from ..forms.support import SupportTicketForm
from ..models import SupportTicket
from ..services.support_service import create_ticket

bp = Blueprint("support", __name__, url_prefix="/support")


@bp.route("/", methods=["GET", "POST"])
@login_required
def index():
    form = SupportTicketForm()
    if form.validate_on_submit():
        create_ticket(current_user.id, form.subject.data, form.body.data)
        flash("Support ticket submitted", "success")
        return redirect(url_for("support.index"))

    tickets = (
        SupportTicket.query.filter_by(employee_id=current_user.id)
        .order_by(SupportTicket.created_at.desc())
        .all()
    )
    return render_template("support/index.html", form=form, tickets=tickets)


@bp.route("/<int:ticket_id>/resolve", methods=["POST"])
@login_required
def resolve(ticket_id: int):
    ticket = SupportTicket.query.get_or_404(ticket_id)
    if current_user.role != "admin":
        flash("Only admins can resolve tickets", "warning")
        return redirect(url_for("support.index"))
    ticket.status = "closed"
    db.session.commit()
    flash("Ticket resolved", "success")
    return redirect(url_for("support.index"))
