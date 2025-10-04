"""Database models with business logic."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import all models to make them available
from app.models.employee import Employee
from app.models.room import Room
from app.models.booking import Booking
from app.models.admin import Admin
from app.models.support_ticket import SupportTicket

__all__ = ["db", "Employee", "Room", "Booking", "Admin", "SupportTicket"]
