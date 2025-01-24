#!/usr/bin/env python
"""Creates, edit, delete, and manage departments and lists of members and available departments"""
from app.models.base_model import BaseModel, Base


class Department(BaseModel, Base):
    """Tracks and organizes church departments"""
    __tablename__ = 'departments'

    name = ""
    description = ""
    head = ""

    def __init__(self, *args, **kwargs):
        """Initializes the Department instance"""
        super().__init__(*args, **kwargs)

    def __repr__(self):
        return f"<Department {self.name}>"