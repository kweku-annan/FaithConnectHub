#!/usr/bin/python3
"""Base Model of FaithConnect Hub"""
import uuid
from os import getenv

from sqlalchemy import Column, String, DateTime

from app import models
from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BaseModel:
    """The Base Model Class of this project"""
    id = Column(String(60), default=lambda: str(uuid.uuid4()), primary_key=True, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, nullable=False)

    def __init__(self, *args, **kwargs):
        """Initializes the BaseModel instance"""
        if kwargs:
            for k, v in kwargs.items():
                if k in ['created_at', 'updated_at']:
                    v = datetime.strptime(v, "%Y-%m-%dT%H:%M:%S.%f")

                # Convert string to int if it is an int and float if it is a float
                if isinstance(v, str):
                    if v.isdigit():
                        v = int(v)
                    elif v.replace('.', '', 1).isdigit():
                        v = float('%.2f' % float(v))
                if k != '__class__':
                    setattr(self, k, v)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = self.updated_at = datetime.now()


    def __str__(self):
        """Returns [<class name>] (<self.id>) <self.__dict__>"""
        return f"[{type(self).__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        """Updates the public instance attribute <update_at> with current
        datetime"""
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """Returns a dictionary containing all keys/values of __dict__"""
        a_dict = {k: v for k, v in self.__dict__.items() if not k.startswith('_')}
        a_dict['__class__'] = type(self).__name__
        return a_dict

    def delete(self):
        """Deletes the current instance from the storage"""
        models.storage.delete(self)