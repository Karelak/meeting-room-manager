"""Lightweight scheduler hooks for periodic maintenance."""

from __future__ import annotations

import logging
from datetime import datetime, timedelta

from flask import Flask

from ..extensions import db
from ..models import Booking

logger = logging.getLogger(__name__)


_last_cleanup: datetime | None = None


def register_scheduled_jobs(app: Flask) -> None:
    """Register low-overhead maintenance hooks.

    For a more robust production setup, wire Celery or APScheduler.
    """

    @app.before_request
    def expire_past_bookings() -> None:
        global _last_cleanup
        if _last_cleanup and datetime.utcnow() - _last_cleanup < timedelta(minutes=15):
            return
        _last_cleanup = datetime.utcnow()

        with app.app_context():
            outdated = Booking.query.filter(
                Booking.status == "scheduled", Booking.end_ts < datetime.utcnow()
            ).update({"status": "completed"})
            if outdated:
                logger.info("Auto-completed %s historical bookings", outdated)
                db.session.commit()
