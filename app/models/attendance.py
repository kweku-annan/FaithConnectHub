#!/usr/bin/python3
"""Model for tracking and understanding members engagement
TODO 1: Participation Monitoring: Record who attended services, events, or meetings.
TODO 2: Engagement Analysis: Identify highly engaged members and those who need encouragement.
TODO 3: Reporting: Provide insights such as attendance trends, average attendance, and demographic participation.
TODO 4: Accountability: Ensure leaders or participants fulfill their commitments.
"""
from app.models.base_model import BaseModel


class Attendance(BaseModel):
    """Tracks and understand members engagement"""
    event_id = ""
    member_id = ""
    attendance_date = ""
    status = ""
