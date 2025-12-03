"""Notification utilities."""

from __future__ import annotations

import logging

from flask import current_app

from ..extensions import db
from ..models import Notification

logger = logging.getLogger(__name__)


def record_notification(
    employee_id: int, message: str, category: str = "info"
) -> Notification:
    notice = Notification(employee_id=employee_id, message=message, category=category)
    db.session.add(notice)
    db.session.commit()

    if current_app.config.get("MAILJET_API_KEY"):
        logger.info("Would send email to %s: %s", employee_id, message)
    else:
        logger.debug("Notification queued for %s: %s", employee_id, message)
    return notice
