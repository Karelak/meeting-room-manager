"""Support ticket forms."""

from __future__ import annotations

from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class SupportTicketForm(FlaskForm):
    subject = StringField("Subject", validators=[DataRequired(), Length(max=255)])
    body = TextAreaField(
        "Describe the issue", validators=[DataRequired(), Length(max=4000)]
    )
    severity = SelectField(
        "Severity",
        choices=[("low", "Low"), ("medium", "Medium"), ("high", "High")],
        default="medium",
    )
    submit = SubmitField("Submit ticket")
