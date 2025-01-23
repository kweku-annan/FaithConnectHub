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


    def __str__(self):
        """Returns [<class name>] (<self.id>) <self.__dict__>"""
        return f"[{type(self).__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        """Updates the public instance attribute <update_at> with current
        datetime"""
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """Returns a dictionary containing all keys/values of __dict__"""
        a_dict = dict(self.__dict__)
        for key in a_dict:
            if key == "id":
                a_dict[key] = self.id
            elif key == "created_at":
                a_dict[key] = self.created_at.isoformat()
            elif key == "updated_at":
                a_dict[key] = self.updated_at.isoformat()
        a_dict["__class__"] = type(self).__name__
        return a_dict

    def delete(self):
        """Deletes the current instance from the storage"""
        models.storage.delete(self)