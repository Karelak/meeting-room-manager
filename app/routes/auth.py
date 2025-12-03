"""Authentication endpoints."""

from __future__ import annotations

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from ..forms.auth import LoginForm
from ..models import User

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.home"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user and user.check_password(form.password.data):
            if not user.is_active:
                flash("Account is disabled. Contact admin.", "danger")
            else:
                login_user(user, remember=form.remember_me.data)
                flash("Welcome back!", "success")
                next_url = request.args.get("next") or url_for("dashboard.home")
                return redirect(next_url)
        else:
            flash("Invalid credentials", "danger")
    return render_template("auth/login.html", form=form)


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Signed out", "info")
    return redirect(url_for("auth.login"))
