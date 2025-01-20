#!/usr/bin/python3
"""Manages and tracks church events
TODO 1: Create and manage events with details like name, date, and location.
TODO 2: Track attendance by linking attendees (members or guests).
TODO 3: Categorize events by type (e.g., service, workshop).
TODO 4: Send notifications to members about events.
"""
from datetime import datetime, timedelta
from email.policy import default

from sqlalchemy import Column, String, Date, Time, Boolean, Integer, func
from sqlalchemy.orm import relationship

from app.models.attendance import Attendance, AttendanceRole
from app.models.base_model import BaseModel, Base
from app.models.membership import Membership


class Event(BaseModel, Base):
    """Tracks and organizes church events"""
    __tablename__ = 'events'

    # service information
    name = Column(String(100), nullable=False)
    description = Column(String(125), nullable=True)
    date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    is_registration_required = Column(Boolean, default=False, nullable=True)
    is_recurring = Column(Boolean, default=False, nullable=True)

    # Location/Venue Information
    venue = Column(String(100), nullable=False)

    # Relationships
    attendance_record = relationship('Attendance', back_populates='events')
    incomes = relationship('Income', back_populates='event')
    expenses = relationship("Expenses", back_populates="event")

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

    @classmethod
    def get_attendance_trends(cls, session, start_date, end_date):
        """Analyze attendance trends over a period"""
        return session.query(
            cls.date,
            func.count(Attendance.id).label('attendance_count')
        ).join(Attendance).filter(
            cls.date.between(start_date, end_date)
        ).group_by(cls.date).all()

    @classmethod
    def get_member_engagement_score(cls, session, member_id, timeframe_days=90):
        """Calculate member engagement score based on attendance patterns"""
        cutoff_date = datetime.now().date() - timedelta(days=timeframe_days)

        total_services = session.query(func.count(cls.id)).filter(
            cls.date >= cutoff_date
        ).scalar()

        attended_services = session.query(func.count(Attendance.id)).filter(
            Attendance.member_id == member_id,
            Attendance.is_present == True,
            cls.date >= cutoff_date
        ).join(cls).scalar()

        if total_services > 0:
            return (attended_services / total_services) * 100
        return 0

    @classmethod
    def get_disengaged_members(cls, session, threshold_percentage=30, timeframe_days=90):
        """Identify members with low attendance"""
        cutoff_date = datetime.now().date() - timedelta(days=timeframe_days)

        return session.query(Membership).join(Attendance).join(cls).group_by(Membership.id).having(
            func.count(cls.id) * 100 / func.count(cls.id.distinct()) < threshold_percentage
        ).filter(cls.date >= cutoff_date).all()

    def get_unfulfilled_commitments(self):
        """Get list of members who didn't fulfill their assigned duties"""
        return [
            record.member for record in self.attendance_record
            if record.assigned_duties and not record.fufilled_duties
        ]

    def generate_demographic_report(self):
        """Generate detailed demographic participation report"""
        return {
            'total_attendance': self.total_attendance,
            'gender_distribution': {
                'male': self.male_attendance,
                'female': self.female_attendance
            },
            'first_timers': self.first_timeer_count,
            'roles_distribution': {
                role.value: sum(1 for record in self.attendance_record
                                if record.role == role and record.is_present)
                for role in AttendanceRole
            },
            'commitment_fulfillment': {
                'total_assignments': sum(1 for record in self.attendance_record
                                         if record.assigned_duties),
                'fulfilled': sum(1 for record in self.attendance_record
                                 if record.assigned_duties and record.fufilled_duties)
            }
        }




