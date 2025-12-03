"""User utility functions."""

from __future__ import annotations

from ..extensions import db
from ..models import User


def create_user(**data) -> User:
    password = data.pop("password", None)
    user = User(**data)
    if password:
        user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return user


def update_user(user: User, **changes) -> User:
    password = changes.pop("password", None)
    for key, value in changes.items():
        setattr(user, key, value)
    if password:
        user.set_password(password)
    db.session.commit()
    return user
