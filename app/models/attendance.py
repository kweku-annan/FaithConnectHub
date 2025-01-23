#!/usr/bin/python3
"""Model for tracking and understanding members engagement
TODO 1: Participation Monitoring: Record who attended services, events, or meetings.
TODO 2: Engagement Analysis: Identify highly engaged members and those who need encouragement.
TODO 3: Reporting: Provide insights such as attendance trends, average attendance, and demographic participation.
TODO 4: Accountability: Ensure leaders or participants fulfill their commitments.
"""
from datetime import datetime

from sqlalchemy import Column, ForeignKey, UniqueConstraint, Boolean, String, Time, Enum, DateTime
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum

from app.models.base_model import BaseModel, Base


class AttendanceRole(PyEnum):
    ATTENDEE = 'attendee'
    LEADER = 'leader'
    VOLUNTEER = 'volunteer'
    SPEAKER = 'speaker'


class AttendanceStatus(PyEnum):
    PRESENT =  "present"
    ABSENT =    "absent"
    LATE = "late"


class Attendance(BaseModel, Base):
    """Tracks and understand members engagement"""
    __tablename__ = 'attendance'
    event_id = Column(String(60), ForeignKey('events.id'), nullable=False)
    events = relationship('Event', back_populates='attendance_record')
    member_id = Column(String(60), ForeignKey('members.id'), nullable=False)
    member = relationship('Membership', back_populates='attendance_record', foreign_keys=[member_id])
    comments = Column(String(200)) # Additional notes about participation

    # Attendance Details
    check_in_time = Column(Time)
    check_out_time = Column(Time)
    is_present = Column(Boolean, default=True) # For tracking actual people present for a registered event.
    role = Column(Enum(AttendanceRole), default=AttendanceRole.ATTENDEE)
    attendance_date = Column(DateTime, nullable=False)
    status = Column(Enum(AttendanceStatus), default=AttendanceStatus.PRESENT)

    # Commitment tracking
    assigned_duties = Column(String(200)) # Track responsibilities
    fulfilled_duties = Column(Boolean, default=False)


    __table_args__ = (
        UniqueConstraint('member_id', 'event_id', name='unique_member_service_attendance'),
    )

    @property
    def duration(self):
        """Calculate attendance duration"""
        if self.check_in_time and self.check_out_time:
            return datetime.combine(datetime.today(), self.check_out_time) - \
                datetime.combine(datetime.today(), self.check_in_time)
        return None

