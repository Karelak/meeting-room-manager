"""Custom Flask CLI commands."""

from __future__ import annotations

import click
from flask import Flask

from ..extensions import db
from ..models import Booking, Room, User, seed_default_admin


def register_cli_commands(app: Flask) -> None:
    @app.cli.group("seed")
    def seed_group() -> None:
        """Seed helper commands."""

    @seed_group.command("sample-data")
    def seed_sample_data() -> None:
        """Seed sample users, rooms, and bookings."""
        click.echo("Seeding default admin...")
        seed_default_admin()

        if not Room.query.first():
            rooms = [
                Room(
                    name="Aviation Lab",
                    floor=1,
                    capacity=12,
                    equipment="TV, Camera, VC",
                ),
                Room(
                    name="Gatwick Suite",
                    floor=2,
                    capacity=20,
                    equipment="TV, Whiteboard",
                ),
                Room(name="Control Tower", floor=3, capacity=8, equipment="TV"),
            ]
            db.session.add_all(rooms)
            click.echo("Added sample rooms")

        if not User.query.filter_by(email="staff@caa.co.uk").first():
            staff = User(first_name="Sam", last_name="Staff", email="staff@caa.co.uk")
            staff.set_password("Passw0rd!")
            db.session.add(staff)
            click.echo("Added sample staff user")

        db.session.commit()
        click.echo("Sample data seeded")
