# Meeting Room Booking System - Setup Instructions

## Installation

1. Install dependencies:

   ```
   pip install flask flask-sqlalchemy flask-login
   ```

   Or use uv (if you have it installed):

   ```
   uv pip install flask flask-sqlalchemy flask-login
   ```

## Running the Application

1. Run the application:

   ```
   python main.py
   ```

2. Open your web browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```

## Test Credentials

### Admin Account

- Email: admin@caa.co.uk
- Password: admin123

### Staff Account

- Email: john.smith@caa.co.uk
- Password: password123

## Features

- **Authentication**: Login/logout functionality
- **Dashboard**: View your bookings and notifications
- **Rooms**: Browse all meeting rooms and their details
- **Bookings**: Create, view, and cancel bookings
- **Conflict Detection**: Automatic double-booking prevention
- **Notifications**: System notifications for users
- **Support Tickets**: Submit and track support requests
- **Admin Dashboard**: Complete system overview (admin only)
- **Role-Based Access**: Different permissions for staff, senior, and admin users

## Project Structure

```
meeting-room-manager/
├── main.py                          # Flask application with routes
├── models.py                        # SQLAlchemy database models
├── pyproject.toml                   # Project dependencies
├── README.md                        # Project documentation
├── SETUP.md                         # This file
├── meeting_rooms.db                 # SQLite database (created on first run)
└── templates/                       # HTML templates
    ├── base.html                    # Base template with navigation
    ├── auth/
    │   └── login.html              # Login page
    ├── dashboard/
    │   ├── main.html               # User dashboard
    │   └── admin.html              # Admin dashboard
    ├── rooms/
    │   ├── list.html               # Room listing
    │   └── detail.html             # Room details
    ├── bookings/
    │   ├── list.html               # User's bookings
    │   └── new.html                # Create new booking
    ├── notifications/
    │   └── list.html               # Notifications
    └── support/
        └── form.html               # Support ticket form
```

## Database Schema

The application automatically creates the following tables:

- **employees**: User accounts and authentication
- **rooms**: Meeting room information
- **bookings**: Room reservations
- **notifications**: User notifications
- **admins**: Admin user information
- **supporttickets**: Support requests

## Notes

- The database is automatically initialized with sample data on first run
- All templates use plain HTML with no CSS (as per requirements)
- The application uses Flask-SQLAlchemy ORM for database operations
- Sessions are used for user authentication
- Simple password storage (for development only - not production-ready)
