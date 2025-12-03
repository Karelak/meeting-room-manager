"""Role helpers and decorators."""

from __future__ import annotations

from functools import wraps
from typing import Callable, TypeVar

from flask import abort
from flask_login import current_user

ROLE_ORDER = {"staff": 0, "senior": 1, "admin": 2}
F = TypeVar("F", bound=Callable[..., object])


def has_privilege(user_role: str, required: str) -> bool:
    return ROLE_ORDER.get(user_role, 0) >= ROLE_ORDER.get(required, 0)


def role_required(required_role: str) -> Callable[[F], F]:
    def decorator(fn: F) -> F:
        @wraps(fn)
        def wrapper(*args, **kwargs):  # type: ignore[misc]
            if not current_user.is_authenticated or not has_privilege(
                current_user.role, required_role
            ):
                abort(403)
            return fn(*args, **kwargs)

        return wrapper  # type: ignore[return-value]

    return decorator
