#!/usr/bin/python3
"""Manages and keeps track of Departments in the Church
It also manages Department creation and other stuff that concerns the
departments.
Has the ability to create New departments and Ministries
Has the ability to Manage department membership

Features could include:
    Creating, editing, and deleting departments/units/ministries.
    Assigning leaders and tracking members for each department.
    Tracking activities, events, and reports for specific ministries.Features could include:

    Creating, editing, and deleting departments/units/ministries.
    Assigning leaders and tracking members for each department.
    Tracking activities, events, and reports for specific ministries.
"""

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.models.base_model import BaseModel, Base


class Department(BaseModel, Base):
    """Manages departments in the church"""
    __tablename__ = 'departments'
    name = Column(String(100), nullable=False)
    notes = Column(String(255), nullable=False)

    members = relationship('Membership', back_populates='departments')
    pass