"""Application factory for Meeting Room Manager."""

from __future__ import annotations

import os
from pathlib import Path

from flask import Flask

from .config import CONFIG_MAP
from .extensions import csrf, db, login_manager, migrate
from .routes import register_blueprints
from .tasks.scheduler import register_scheduled_jobs
from .utils.cli import register_cli_commands


def create_app(config_name: str | None = None) -> Flask:
    """Create and configure the Flask application."""
    config_key = config_name or os.getenv("FLASK_ENV", "development").lower()

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(CONFIG_MAP.get(config_key, CONFIG_MAP["development"]))

    secret_key = os.getenv("SECRET_KEY")
    if secret_key:
        app.config["SECRET_KEY"] = secret_key

    instance_path = Path(app.instance_path)
    instance_path.mkdir(parents=True, exist_ok=True)

    _register_extensions(app)
    register_blueprints(app)
    register_cli_commands(app)
    register_scheduled_jobs(app)

    return app


def _register_extensions(app: Flask) -> None:
    """Attach Flask extensions to the app."""
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)

    @login_manager.user_loader
    def load_user(user_id: str):  # type: ignore[override]
        from .models import User

        return User.query.get(int(user_id))

    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "warning"
    login_manager.session_protection = "strong"
