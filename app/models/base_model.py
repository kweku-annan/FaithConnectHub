#!/usr/bin/python3
"""Base Model of FaithConnect Hub"""
import uuid
from email.policy import default

from sqlalchemy import Column, String, DATETIME
# from sqlalchemy.dialects.mysql import DATETIME
from sqlalchemy.ext.declarative import declarative_base

from app import models
from datetime import datetime

from app.models import storage

Base = declarative_base()

class BaseModel:
    """The Base Model Class of this project"""
    id = Column(String(60), nullable=False, primary_key=True, unique=True)
    created_at = Column(DATETIME, nullable=False, default=datetime.utcnow())
    updated_at = Column(DATETIME, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Initializes Attributes"""
        if kwargs is not None and len(kwargs) != 0:
            for key, value in kwargs.items():
                if key == "id":
                    self.id = kwargs[key]
                elif key == "created_at":
                    self.created_at = datetime.strptime(kwargs[key],
                                                        "%Y-%m-%dT%H:%M:%S.%f")
                elif key == "updated_at":
                    self.updated_at = datetime.strptime(kwargs[key],
                                                        "%Y-%m-%dT%H:%M:%S.%f")
                else:
                    if key != "__class__":
                        setattr(self, key, kwargs[key])
        else:
            self.id = str(uuid.uuid4()) # Assign when an instance is created
            self.created_at = datetime.now()
            self.updated_at = datetime.now()


    def __str__(self):
        """Returns [<class name>] (<self.id>) <self.__dict__>"""
        return f"[{type(self).__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        """Updates the public instance attribute <update_at> with current
        datetime"""
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def delete(self):
        """Deletes the current instance from the storage"""
        storage.delete(self)

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
        if '_sa_instance_state' in a_dict:
            del a_dict['_sa_instance_state']
        return a_dict
