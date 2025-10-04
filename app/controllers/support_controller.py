"""Support ticket controller."""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.services.auth_service import AuthService
from app.services.support_service import SupportService
from app.middleware.auth_decorators import login_required, admin_required

support_bp = Blueprint("support", __name__, url_prefix="/support")


class SupportController:
    """Controller for support ticket routes."""

    def __init__(self):
        self.auth_service = AuthService()
        self.support_service = SupportService()

    def support_form(self):
        """Support ticket form and list."""
        user = self.auth_service.get_current_user()

        if request.method == "POST":
            subject = request.form.get("subject")
            message = request.form.get("message")

            try:
                self.support_service.create_ticket(user.employeeid, subject, message)
                flash("Support ticket submitted successfully", "success")
                return redirect(url_for("support.support_form"))
            except ValueError as e:
                flash(str(e), "error")

        tickets = self.support_service.get_employee_tickets(user.employeeid)
        return render_template("support/form.html", user=user, tickets=tickets)

    def delete_ticket(self, ticket_id):
        """Delete a support ticket (admin only)."""
        user = self.auth_service.get_current_user()

        try:
            self.support_service.delete_ticket(ticket_id, user)
            flash("Ticket deleted successfully", "success")
        except ValueError as e:
            flash(str(e), "error")
        except PermissionError as e:
            flash(str(e), "error")

        return redirect(url_for("admin.admin_dashboard"))


# Initialize controller
support_controller = SupportController()


# Register routes
@support_bp.route("/", methods=["GET", "POST"])
@login_required
def support_form():
    return support_controller.support_form()


@support_bp.route("/<int:ticket_id>/delete", methods=["POST"])
@admin_required
def delete_ticket(ticket_id):
    return support_controller.delete_ticket(ticket_id)
