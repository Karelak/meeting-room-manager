"""Booking related forms."""

from __future__ import annotations

from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import (
    DateField,
    DateTimeLocalField,
    IntegerField,
    SelectField,
    SelectMultipleField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import DataRequired, Length, NumberRange


class BookingForm(FlaskForm):
    room_id = SelectField("Room", coerce=int, validators=[DataRequired()])
    title = StringField("Title", validators=[DataRequired(), Length(max=255)])
    agenda = TextAreaField("Agenda", validators=[Length(max=2000)])
    start_ts = DateTimeLocalField(
        "Start",
        format="%Y-%m-%dT%H:%M",
        validators=[DataRequired()],
        default=datetime.utcnow,
    )
    end_ts = DateTimeLocalField(
        "End", format="%Y-%m-%dT%H:%M", validators=[DataRequired()]
    )
    attendees = SelectMultipleField("Attendees", coerce=int)
    priority_level = SelectField(
        "Priority",
        choices=[("normal", "Normal"), ("high", "High"), ("critical", "Critical")],
        default="normal",
    )
    justification = TextAreaField("Justification", validators=[Length(max=2000)])
    submit = SubmitField("Save booking")


class BookingFilterForm(FlaskForm):
    date = DateField("Date")
    min_capacity = IntegerField(
        "Minimum capacity", validators=[NumberRange(min=1)], default=1
    )
    floor = IntegerField("Floor")
    equipment = StringField("Equipment contains")
    submit = SubmitField("Apply filters")
