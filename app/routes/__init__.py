"""Blueprint registrations."""

from __future__ import annotations

from flask import Flask

from . import admin, auth, bookings, dashboard, rooms, support, terminals


def register_blueprints(app: Flask) -> None:
    app.register_blueprint(auth.bp)
    app.register_blueprint(dashboard.bp)
    app.register_blueprint(rooms.bp)
    app.register_blueprint(bookings.bp)
    app.register_blueprint(support.bp)
    app.register_blueprint(admin.bp)
    app.register_blueprint(terminals.bp)
