#!/usr/bin/python3
"""Manages and tracks church events
TODO 1: Create and manage events with details like name, date, and location.
TODO 2: Track attendance by linking attendees (members or guests).
TODO 3: Categorize events by type (e.g., service, workshop).
TODO 4: Send notifications to members about events.
"""

from app.models.base_model import BaseModel


class Event(BaseModel):
    """Tracks and organizes church events"""
    name = ""
    description = ""
    start_date = None
    end_date = None
    start_time = None
    end_time = None
    location = ""
    is_registration_required = None
    event_type = ""
    is_recurring = None
    recurrence_pattern = ""

