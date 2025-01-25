#!/usr/bin/env python
"""Creates, edit, delete, and manage departments and lists of members and available departments"""
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base_model import BaseModel, Base
from app.models.association_tables import member_department


class Department(BaseModel, Base):
    """Tracks and organizes church departments"""
    __tablename__ = 'departments'

    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=False)
    leader_id = Column(String(60), ForeignKey('members.id'), nullable=False)

    # Relationships
    members = relationship("Member", secondary=member_department, back_populates="department")
    leader = relationship("Member", secondary=member_department, back_populates="leading_department")
    financial_records = relationship("FinancialRecord", back_populates="department")
    event = relationship("Event", back_populates="department")
    group = relationship("Group", back_populates="department")

    def __init__(self, name=None, description=None, leader_id=None, *args, **kwargs):
        """
        Initializes the Department instance with strict required field validation.
        """
        if not name or not isinstance(name, str):
            raise TypeError("'name' is required and should be a non-empty string.")
        if not description or not isinstance(description, str):
            raise TypeError("'description' is required and should be a non-empty string.")
        if not leader_id or not isinstance(leader_id, str):
            raise TypeError("'leader_id' is required and should be a non-empty string.")

        self.name = name
        self.description = description
        self.leader_id = leader_id
        super().__init__(*args, **kwargs)

    def __repr__(self):
        return f"<Department {self.name}>"

    def __str__(self):
        return f"<Department {self.name}>"