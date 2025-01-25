#!/usr/bin/python3
"""Manages and tracks church events
TODO 1: Create and manage events with details like name, date, and location.
TODO 2: Track attendance by linking attendees (members or guests).
TODO 3: Categorize events by type (e.g., service, workshop).
TODO 4: Send notifications to members about events.
"""
from sqlalchemy import Column, String, Date, Time, Text, ForeignKey

from app.models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship


class Event(BaseModel, Base):
    """Tracks and organizes church events"""
    __tablename__ = 'events'

    name = Column(String(100), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    location = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String(50), nullable=False, default='General')
    department_id = Column(String(60), ForeignKey('departments.id'), nullable=True)  # Optional for non-department
    group_id = Column(String(60), ForeignKey('groups.id'), nullable=True)  # Optional for non-group

    # Relationships
    attendance = relationship("Attendance", back_populates="event")
    financial_records = relationship("FinancialRecord", back_populates="event")
    department = relationship("Department", back_populates="event")
    group = relationship("Group", back_populates="event")

    def __init__(self, *args, **kwargs):
        """Initializes the Event instance"""
        super().__init__(*args, **kwargs)

    def __repr__(self):
        return f"<Event {self.name}, Date: {self.date}, Category: {self.category}>"

    def __str__(self):
        return f"{self.name} on {self.date} at {self.time} in {self.location}"


