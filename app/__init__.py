"""Flask application factory."""
from flask import Flask
from app.config import DevelopmentConfig


def create_app(config_class=DevelopmentConfig):
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    from app.models import db
    db.init_app(app)

    # Register blueprints
    from app.controllers.auth_controller import auth_bp
    from app.controllers.dashboard_controller import dashboard_bp
    from app.controllers.booking_controller import booking_bp
    from app.controllers.room_controller import room_bp
    from app.controllers.admin_controller import admin_bp
    from app.controllers.support_controller import support_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(booking_bp)
    app.register_blueprint(room_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(support_bp)

    # Create database tables
    with app.app_context():
        db.create_all()

    return app
