"""User management forms."""

from __future__ import annotations

from flask_wtf import FlaskForm
from wtforms import PasswordField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Optional


class UserForm(FlaskForm):
    first_name = StringField("First name", validators=[DataRequired(), Length(max=80)])
    last_name = StringField("Last name", validators=[DataRequired(), Length(max=80)])
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=255)])
    role = SelectField(
        "Role", choices=[("staff", "Staff"), ("senior", "Senior"), ("admin", "Admin")]
    )
    password = PasswordField(
        "Password", validators=[Optional(), Length(min=8, max=128)]
    )
    submit = SubmitField("Save user")
