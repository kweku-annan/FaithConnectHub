#!/usr/bin/python3
"""Manages and handles groups in the church
Allows creation and managing of groups in the church
"""
from datetime import datetime
from enum import Enum as PyEnum
from sqlite3 import SQLITE_CONSTRAINT_TRIGGER

from sqlalchemy import Column, String, Table, ForeignKey, DateTime, Text, Enum, Time, Integer, Boolean, nullsfirst
from sqlalchemy.orm import relationship, backref

from app.models.base_model import BaseModel, Base

# Association table for group members with roles
group_members = Table(
    'group_members',
    BaseModel.metadata,
    Column('group_id', String(50), ForeignKey('groups.id')),
    Column('member_id', String(50), ForeignKey('members.id')),
    Column('role', String(50), default='member'),  # e.g. 'leader', 'assistant', 'member'
    Column('joined_date', DateTime, default=datetime.utcnow)
)


class GroupStatus(PyEnum):
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    ON_HOLD = 'on_hold'
    DISBANDED = 'disbanded'


class GroupType(PyEnum):
    BIBLE_STUDY = 'bible_study'
    CHOIR = 'choir'
    YOUTH = 'youth'
    PRAYER = 'prayer'
    HOME_CELL = 'home_cell'
    OUTREACH = 'outreach'
    MENS_FELLOWSHIP = 'mens_fellowship'
    WOMENS_FELLOWSHIP = 'womens_fellowship'
    CHILDREN = 'children'


class Group(BaseModel, Base):
    """Manages and handles groups in the church."""
    __tablename__ = 'groups'

    # Basic Information
    name = Column(String(100), nullable=False)
    description = Column(Text)
    group_type = Column(Enum(GroupType), nullable=False)
    status = Column(Enum(GroupStatus), default=GroupStatus.ACTIVE)

    # Meeting Details
    meeting_day = Column(String(50))
    meeting_time = Column(Time)
    meeting_location = Column(String(100))
    meeting_frequency = Column(String(50))  # weekly, bi-weekly, monthly

    # Group Configuration
    max_capacity = Column(Integer)
    min_age = Column(Integer)
    max_age = Column(Integer)
    gender_specific = Column(String(20))  # male, female, mixed
    is_public = Column(Boolean, default=True)  # whether group is an opened or a closed one

    # Leadership
    leader_id = Column(String(50), ForeignKey('members.id'))
    assistant_leader_id = Column(String(50), ForeignKey('members.id'))

    # Department Association
    department_id = Column(String(50), ForeignKey('departments.id'))

    # Relationships
    leader = relationship('Membership', foreign_keys=[leader_id], backref='leading_groups')
    assistant_leader = relationship('Membership', foreign_keys=[assistant_leader_id], backref='assisting_groups')
    department = relationship('Department', back_populates='groups')
    members = relationship(
        'Membership',
        secondary=group_members,
        back_populates='groups',
        lazy='dynamic'
    )
    activities = relationship('GroupActivity', back_populates='group', cascade="all, delete-orphan")
    meetings = relationship('GroupMeeting', back_populates='group', cascade="all, delete-orphan")

    def add_member(self, member, role='member'):
        """Add a member to the group"""
        if self.max_capacity and self.members.count() >= self.max_capacity:
            raise ValueError("Group has reached maximum capacity")

        connection = group_members.insert().values(
            group_id=self.id,
            member_id=member.id,
            role=role,
            joined_date=datetime.utcnow()
        )
        return connection

    def remove_member(self, member):
        """Remove a member from the group"""
        connection = group_members.delete().where(
            group_members.c.group_id == self.id,
            group_members.c.member_id == member.id
        )
        return connection

    def get_member_count(self):
        """Get list of active members in the group"""
        return self.members.filter_by(status='active').all()

    def check_member_eligibility(self, member):
        """Check if a member is eligible to join the group"""
        if self.gender_specific and member.gender != self.gender_specific:
            return False, "Gender requirement not met"

        if self.min_age or self.max_age:
            age = (datetime.now().date() - member.date_of_birth).days // 365
            if (self.min_age and age < self.min_age) or (self.max_age and age > self.max_age):
                return False, "Age requirement not met"
        return True, "Eligible"


class GroupActivity(BaseModel, Base):
    """Tracks activities organized by groups"""
    __tablename__ = 'group_activities'

    group_id = Column(String(50), ForeignKey('groups_id'), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime)
    location = Column(String(100))
    status = Column(String(50))  # planned, ongoing, completed, cancelled
    max_participants = Column(Integer)

    # Relationships
    group = relationship('Group', back_populates='activities')
    attendees = relationship(
        'Membership',
        secondary='activity_attendees',
        back_populates='group_activities'
    )


class GroupMeeting(BaseModel, Base):
    """Tracks regular group meetings"""
    group_id = Column(String(50), ForeignKey('groups.id'), nullable=False)
    meeting_date = Column(DateTime, nullable=False)
    start_time = Column(Time)
    end_time = Column(Time)
    location = Column(String(100))
    topic = Column(String(200))
    notes = Column(Text)

    # Attendance tracking
    total_attendance = Column(Integer, default=0)

    # Relationships
    group = relationship('Group', back_populates='meetings')
    attendees = relationship(
        'Membership',
        secondary='meeting_attendees',
        back_populates='group_meetings'
    )

