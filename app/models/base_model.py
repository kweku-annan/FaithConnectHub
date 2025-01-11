#!/usr/bin/python3
"""Base Model of FaithConnect Hub"""
import uuid
from datetime import datetime


class BaseModel:
    """The Base Model Class of this project"""
    def __init__(self):
        """Initializes Attributes"""
        self.id = str(uuid.uuid4()) # Assign when an instance is created
        self.created_at = self.updated_at = datetime.now()

    def __str__(self):
        """Returns [<class name>] (<self.id>) <self.__dict__>"""
        return f"[{type(self).__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        """Updates the public instance attribute <update_at> with current
        datetime"""
        self.updated_at = datetime.now()

    def to_dict(self):
        """Returns a dictionary containing all keys/values of __dict__"""
        a_dict = dict(self.__dict__)
        for key in a_dict:
            if key == "created_at" or key == "updated_at":
                a_dict[key] = a_dict[key].isoformat()
        a_dict["__class__"] = type(self).__name__
        return a_dict
