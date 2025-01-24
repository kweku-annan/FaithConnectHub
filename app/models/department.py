#!/usr/bin/env python
"""Creates, edit, delete, and manage departments and lists of members and available departments"""
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base_model import BaseModel, Base
from app.models.association_tables import member_department


class Department(BaseModel, Base):
    """Tracks and organizes church departments"""
    __tablename__ = 'departments'

    name = ""
    description = ""
    head = ""

    # Relationships
    members = relationship("Member", secondary=member_department, back_populates="department")

    def __init__(self, *args, **kwargs):
        """Initializes the Department instance"""
        super().__init__(*args, **kwargs)

    def __repr__(self):
        return f"<Department {self.name}>"