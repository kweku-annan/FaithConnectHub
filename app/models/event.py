#!/usr/bin/python3
"""Manages and tracks church events
TODO 1: Create and manage events with details like name, date, and location.
TODO 2: Track attendance by linking attendees (members or guests).
TODO 3: Categorize events by type (e.g., service, workshop).
TODO 4: Send notifications to members about events.
"""
from sqlalchemy import Column, String, Date

from app.models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship


class Event(BaseModel, Base):
    """Tracks and organizes church events"""
    __tablename__ = 'events'

    name = Column(String(100), nullable=False)
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)
    location = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String(50), nullable=False, default='General')

    # Relationships
    attendance = relationship("Attendance", back_populates="event")

    def __init__(self, *args, **kwargs):
        """Initializes the Event instance"""
        super().__init__(*args, **kwargs)

    def __repr__(self):
        return f"<Event {self.name}, Date: {self.date}, Category: {self.category}>"


