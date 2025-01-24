#!/usr/bin/env python
""""Creates, edit, delete, and manage groups and lists of members and available groups"""
from app.models.base_model import BaseModel, Base


class Group(BaseModel, Base):
    """Tracks and organizes church groups"""
    __tablename__ = 'groups'

    name = ""
    description = ""
    head = ""

    def __init__(self, *args, **kwargs):
        """Initializes the Group instance"""
        super().__init__(*args, **kwargs)

    def __repr__(self):
        return f"<Group {self.name}>"