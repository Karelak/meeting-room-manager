"""Base repository with common CRUD operations."""
from app.models import db


class BaseRepository:
    """Generic repository for common database operations."""

    def __init__(self, model_class):
        """Initialize repository with a model class."""
        self.model = model_class

    def get_by_id(self, entity_id):
        """Get entity by ID."""
        return db.session.get(self.model, entity_id)

    def get_all(self):
        """Get all entities."""
        return self.model.query.all()

    def save(self, entity):
        """Save entity to database."""
        db.session.add(entity)
        db.session.commit()
        return entity

    def delete(self, entity):
        """Delete entity from database."""
        db.session.delete(entity)
        db.session.commit()

    def delete_by_id(self, entity_id):
        """Delete entity by ID."""
        entity = self.get_by_id(entity_id)
        if entity:
            self.delete(entity)
            return True
        return False

    def update(self, entity):
        """Update entity in database."""
        db.session.commit()
        return entity

    def count(self):
        """Count total entities."""
        return self.model.query.count()

    def exists(self, entity_id):
        """Check if entity exists."""
        return self.get_by_id(entity_id) is not None
