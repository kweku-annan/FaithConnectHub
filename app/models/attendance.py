#!/usr/bin/python3
"""Model for tracking and understanding members engagement
TODO 1: Participation Monitoring: Record who attended services, events, or meetings.
TODO 2: Engagement Analysis: Identify highly engaged members and those who need encouragement.
TODO 3: Reporting: Provide insights such as attendance trends, average attendance, and demographic participation.
TODO 4: Accountability: Ensure leaders or participants fulfill their commitments.
"""
from sqlalchemy import Column, ForeignKey, UniqueConstraint, Boolean
from sqlalchemy.orm import relationship

from app.models.base_model import BaseModel, Base


class Attendance(BaseModel, Base):
    """Tracks and understand members engagement"""
    __tablename__ = 'attendance'
    event_id = Column(ForeignKey('events.id'), nullable=False)
    events = relationship('Event', back_populates='attendance_record')
    member_id = Column(ForeignKey('members.id'), nullable=False)
    member = relationship('Membership', back_populates='attendance_record')
    attendance_date = ""
    status = ""

    is_present = Column(Boolean, default=True) # For tracking actual people present for a registered event.


    __table_args__ = (
        UniqueConstraint('member_id', 'event_id', name='unique_member_service_attendance')
    )


