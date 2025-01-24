#!/usr/bin/python3
""""Tracks attendance and attendance records for church events"""
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base_model import BaseModel, Base


class Attendance(BaseModel, Base):
    """Tracks attendance for church events"""
    __tablename__ = 'attendance'

    member_id = Column(String(60), ForeignKey('members.id'), nullable=False)
    event_id = Column(String(60), ForeignKey('events.id'), nullable=False)



    # Relationships
    member = relationship("Member", back_populates="attendance")
    event = relationship("Event", back_populates="attendance")
