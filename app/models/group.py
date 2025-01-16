#!/usr/bin/python3
"""Manages and handles groups in the church
Allows creation and managing of groups in the church
"""
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.models.base_model import BaseModel, Base


class Group(BaseModel, Base):
    """Manages and handles groups in the church."""
    __tablename__ = 'groups'
    name = Column(String(100), nullable=False)
    notes = Column(String(255), nullable=False)

    members = relationship('Membership', back_populates='groups')
    pass