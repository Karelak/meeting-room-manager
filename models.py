from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Employee(db.Model):
    __tablename__ = "employees"

    employeeid = db.Column(
        db.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True
    )
    fname = db.Column(db.Text, nullable=False)
    lname = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False)
    password = db.Column(db.Text, nullable=False)  # Added for authentication
    role = db.Column(db.Text, nullable=False, default="staff")

    # Relationships
    bookings = db.relationship(
        "Booking", back_populates="employee", cascade="all, delete-orphan"
    )
    notifications = db.relationship(
        "Notification", back_populates="employee", cascade="all, delete-orphan"
    )
    support_tickets = db.relationship(
        "SupportTicket", back_populates="employee", cascade="all, delete-orphan"
    )

    __table_args__ = (
        db.CheckConstraint("role IN ('staff', 'senior', 'admin')", name="check_role"),
    )

    def __repr__(self):
        return f"<Employee {self.fname} {self.lname}>"


class Room(db.Model):
    __tablename__ = "rooms"

    roomid = db.Column(
        db.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True
    )
    floor = db.Column(db.Integer, nullable=False)
    roomname = db.Column(db.Text, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)

    # Relationships
    bookings = db.relationship(
        "Booking", back_populates="room", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Room {self.roomname} (Floor {self.floor})>"


class Booking(db.Model):
    __tablename__ = "bookings"

    bookingid = db.Column(
        db.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True
    )
    employeeid = db.Column(
        db.Integer,
        db.ForeignKey("employees.employeeid", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    roomid = db.Column(
        db.Integer,
        db.ForeignKey("rooms.roomid", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    timebegin = db.Column(
        db.Text, nullable=False, default=lambda: datetime.now().isoformat()
    )
    timefinish = db.Column(db.Text)

    # Relationships
    employee = db.relationship("Employee", back_populates="bookings")
    room = db.relationship("Room", back_populates="bookings")

    def __repr__(self):
        return f"<Booking {self.bookingid} - Room {self.roomid}>"


class Notification(db.Model):
    __tablename__ = "notifications"

    notificationid = db.Column(
        db.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True
    )
    employeeid = db.Column(
        db.Integer,
        db.ForeignKey("employees.employeeid", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(
        db.Text, nullable=False, default=lambda: datetime.now().isoformat()
    )

    # Relationships
    employee = db.relationship("Employee", back_populates="notifications")

    def __repr__(self):
        return f"<Notification {self.notificationid}>"


class Admin(db.Model):
    __tablename__ = "admins"

    adminid = db.Column(
        db.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True
    )
    fname = db.Column(db.Text, nullable=False)
    lname = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False)

    # Relationships
    support_tickets = db.relationship(
        "SupportTicket", back_populates="admin", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Admin {self.fname} {self.lname}>"


class SupportTicket(db.Model):
    __tablename__ = "supporttickets"

    ticketid = db.Column(
        db.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True
    )
    employeeid = db.Column(
        db.Integer,
        db.ForeignKey("employees.employeeid", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    adminid = db.Column(
        db.Integer,
        db.ForeignKey("admins.adminid", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    subject = db.Column(db.Text, nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(
        db.Text, nullable=False, default=lambda: datetime.now().isoformat()
    )

    # Relationships
    employee = db.relationship("Employee", back_populates="support_tickets")
    admin = db.relationship("Admin", back_populates="support_tickets")

    def __repr__(self):
        return f"<SupportTicket {self.ticketid} - {self.subject}>"
