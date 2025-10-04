"""Controllers (Flask Blueprints)."""
from app.controllers.auth_controller import auth_bp
from app.controllers.dashboard_controller import dashboard_bp
from app.controllers.booking_controller import booking_bp
from app.controllers.room_controller import room_bp
from app.controllers.admin_controller import admin_bp
from app.controllers.support_controller import support_bp

__all__ = [
    "auth_bp",
    "dashboard_bp",
    "booking_bp",
    "room_bp",
    "admin_bp",
    "support_bp",
]
