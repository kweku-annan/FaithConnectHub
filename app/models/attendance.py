#!/usr/bin/python3
""""Tracks attendance and attendance records for church events"""
from datetime import datetime

from sqlalchemy import Column, String, ForeignKey, Text, Date, Boolean
from sqlalchemy.orm import relationship

from app.models.base_model import BaseModel, Base


class Attendance(BaseModel, Base):
    """Tracks attendance for church events"""
    __tablename__ = 'attendance'

    member_id = Column(String(60), ForeignKey('members.id'), nullable=True)
    event_id = Column(String(60), ForeignKey('events.id'), nullable=False)
    status = Column(String(50), nullable=False, default='PRESENT')
    remarks = Column(Text, nullable=True)
    date = Column(Date, nullable=False, default=datetime.now)
    is_guest = Column(Boolean, nullable=False, default=False) # True if the attendee is a guest



    # Relationships
    member = relationship("Member", back_populates="attendance")
    event = relationship("Event", back_populates="attendance")

    def __init__(self, *args, **kwargs):
        """Initializes the Attendance instance"""
        super().__init__(*args, **kwargs)
        self.date = kwargs.get('date', datetime.now())
        self.status = kwargs.get('status', 'Present')

    def __repr__(self):
            return f"<Attendance {self.member_id} - {self.event_id}, Status {self.status}>"

    def __str__(self):
        return f"{self.member_id} - {self.event_id}, Status {self.status}"
