#!/usr/bin/python3
"""Manages and tracks church events
TODO 1: Create and manage events with details like name, date, and location.
TODO 2: Track attendance by linking attendees (members or guests).
TODO 3: Categorize events by type (e.g., service, workshop).
TODO 4: Send notifications to members about events.
"""
from email.policy import default

from sqlalchemy import Column, String, Date, Time, Boolean, Integer
from sqlalchemy.orm import relationship

from app.models.base_model import BaseModel, Base


class Event(BaseModel, Base):
    """Tracks and organizes church events"""
    __tablename__ = 'events'

    # service information
    name = Column(String(100), nullable=False)
    description = Column(String(125), nullable=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    is_registration_required = Column(Boolean, default=False, nullable=True)
    is_recurring = Column(Boolean, default=False, nullable=True)

    # Location/Venue Information
    venue = Column(String(100), nullable=False)

    # Relationships
    attendance_record = relationship('Attendance', back_populates='events')

    # Statistics tracking
    total_attendance = Column(Integer, default=0)
    male_attendance = Column(Integer, default=0)
    female_attendance = Column(Integer, default=0)
    first_timeer_count = Column(Integer, default=0)

    def update_attendance_stats(self):
        """Update attendance statistics for the service"""
        records = self.attendance_record
        self.total_attendance = sum(1 for record in records if record.is_present)

        # Count by gender
        self.male_attendance = sum(
            1 for record in records
            if record.is_present and record.member.gender == 'male'
        )

        self.female_attendance = sum(
            1 for record in records
            if record.is_present and record.member.gender == 'female'
        )

        # Count first-timers
        self.first_timeer_count = sum(
            1 for record in records
            if record.is_present and record.member.membership_status == 'visitor'
        )


