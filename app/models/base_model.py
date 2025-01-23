#!/usr/bin/python3
"""Base Model of FaithConnect Hub"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Boolean, event
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from app import models

Base = declarative_base()

class BaseModel(Base):
    """The Base Model Class of this project"""
    __abstract__ = True

    id = Column(String(60), nullable=False, primary_key=True, unique=True)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True), nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)
    deleted_at = Column(DateTime(timezone=True))

    @declared_attr
    def created_by_id(cls):
        return Column(String(60), ForeignKey('users.id', ondelete='SET NULL'))

    @declared_attr
    def updated_by_id(cls):
        return Column(String(60), ForeignKey('users.id', ondelete='SET NULL'))

    @declared_attr
    def deleted_by_id(cls):
        return Column(String(60), ForeignKey('users.id', ondelete='SET NULL'))


    def __init__(self, *args, **kwargs):
        """Enhanced initialization with better datetime handling"""
        super().__init__(*args, **{k: v for k, v in kwargs.items() if hasattr(type(self), k)})

        # Explicitly set additional attributes that are not SQLAlchemy-mapped
        self.id = kwargs.get('id', str(uuid.uuid4()))
        self.created_at = kwargs.get('created_at', datetime.utcnow())
        self.updated_at = kwargs.get('created_at', datetime.utcnow())

        for key, value in kwargs.items():
            if key in ['created_at', 'updated_at', 'deleted_at'] and isinstance(value, str):
                setattr(self, key, datetime.fromisoformat(value.replace("Z", "+00:00")))
            elif not hasattr(self, key) and key not in ['_sa_instance_state']:
                setattr(self, key, value)

    def soft_delete(self, deleted_by_id=None):
        """Enhanced soft delete with validation"""
        if not self.is_deleted:
            self.is_deleted = True
            self.deleted_at = datetime.utcnow()
            self.deleted_by_id = deleted_by_id
            self.save()
        return True

    def save(self):
        """Save with automatic timestamp update"""
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """Enhanced dictionary representation with audit fields"""
        result = {}
        for key, value in self.__dict__.items():
            if key != '_sa_instance_state':
                if isinstance(value, datetime):
                    result[key] = value.isoformat()
                else:
                    result[key] = value
        result['__class__'] = self.__class__.__name__
        return result

    def __str__(self):
        """Enhanced string representation"""
        return f"[{self.__class__.__name__}] ({self.id}) {self.to_dict()}"

@event.listens_for(BaseModel, 'before_update', propagate=True)
def before_update(mapper, connection, target):
    """Event listener for updates"""
    target.updated_at = datetime.utcnow()

@event.listens_for(BaseModel, 'before_insert', propagate=True)
def before_insert(mapper, connection, target):
    """Event listener for inserts"""
    now = datetime.utcnow()
    if not target.created_at:
        target.created_at = now
    target.updated_at = now
