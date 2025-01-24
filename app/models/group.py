#!/usr/bin/env python
""""Creates, edit, delete, and manage groups and lists of members and available groups"""
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from app.models.association_tables import member_group
from app.models.base_model import BaseModel, Base


class Group(BaseModel, Base):
    """Tracks and organizes church groups"""
    __tablename__ = 'groups'

    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=False)
    head = Column(String(60), ForeignKey('members.id'), nullable=False)
    member_id = Column(String(60), ForeignKey('members.id'), nullable=False)

    # Relationships
    members = relationship("Member", secondary=member_group, back_populates="group")
    financial_records = relationship("FinancialRecord", back_populates="group")

    def __init__(self, *args, **kwargs):
        """Initializes the Group instance"""
        super().__init__(*args, **kwargs)

    def __repr__(self):
        return f"<Group {self.name}>"