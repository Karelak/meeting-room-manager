# Meeting Room Manager

A Flask-based intranet web application for the Civil Aviation Authority (CAA) Crawley office that digitises meeting room reservations, room terminals, booking priorities, and administrator oversight. The platform replaces paper-based processes with live availability, automated conflict detection, NFC-enabled check-ins, and GDPR-conscious data handling.

## Features

- **Self-service booking**: staff create, edit, and cancel bookings with automatic conflict and buffer enforcement.
- **Room catalogue**: searchable/filterable room list with capacity, equipment, and live occupancy insights.
- **Priority overrides**: senior staff and admins can reassign rooms with mandatory justification and audit logging.
- **Room terminals**: kiosk-friendly pages for NFC/ID check-in, early checkout, and instant "book now" actions.
- **Notifications**: in-app inbox plus SMTP hooks (via Mailjet) for confirmations, changes, reminders, and critical alerts.
- **Support desk**: capture, assign, and resolve support tickets with transparent history.
- **Admin console**: manage rooms, users, bookings, settings, and monitor utilisation metrics.

## Tech Stack

- Python 3.13+
- Flask, SQLAlchemy, Flask-Migrate, Flask-Login, Flask-WTF
- SQLite for development (PostgreSQL-ready)
- HTMX and Alpine.js for lightweight interactivity
- SCSS-compiled CSS (prebuilt stylesheet included)

## Getting Started

1. Create and activate a virtual environment.
2. Install dependencies: `pip install -r requirements.txt`.
3. Set environment variables:
   ```pwsh
   $env:FLASK_APP = "app:create_app"
   $env:FLASK_ENV = "development"
   $env:SECRET_KEY = "change-me"
   ```
4. Initialise the database:
   ```pwsh
   flask db upgrade
   flask seed sample-data
   ```
5. Run the development server:
   ```pwsh
   flask run
   ```

## Project Layout

```
app/
  __init__.py        # application factory
  config.py          # configuration objects
  extensions.py      # db, migrate, login, csrf instances
  models.py          # SQLAlchemy models
  forms/
  routes/
  services/
  templates/
  static/
  tasks/
  utils/
```

## Tests

```
pytest
```

## Notes

- Default admin login is `admin@caa.co.uk` with password `Passw0rd!` (update in production).
- Mail integrations default to console logging until SMTP credentials are provided.
- NFC check-in endpoints accept mocked payloads; integrate with hardware readers via REST calls.
