"""Room management forms."""

from __future__ import annotations

from flask_wtf import FlaskForm
from wtforms import BooleanField, IntegerField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, NumberRange


class RoomForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(max=120)])
    floor = IntegerField("Floor", validators=[DataRequired()])
    capacity = IntegerField(
        "Capacity", validators=[DataRequired(), NumberRange(min=1, max=200)]
    )
    equipment = TextAreaField("Equipment", validators=[Length(max=2000)])
    notes = TextAreaField("Notes", validators=[Length(max=2000)])
    is_active = BooleanField("Active", default=True)
    submit = SubmitField("Save room")
