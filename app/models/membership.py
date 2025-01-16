#!/usr/bin/python3
"""Manages membership of the church
TODO 1: Member Information Tracking:
     -- Maintain basic and detailed records for each member.
     -- Associate members with specific departments/ministries.

TODO 2: Role and Status Management:
     -- Categorize members by roles (e.g., Pastor, Member, Leader).
     -- Track membership status (active, inactive, new, transferred).

TODO 3: Engagement Tracking:
     -- Record participation in events, programs, or groups.

TODO 4: Reporting and Insights:
     -- Generate lists or statistics (e.g., number of active members, distribution by department).
"""
from email.policy import default

from sqlalchemy import Column, String, Date, ForeignKey, Enum
from enum import Enum as PyEnum

from sqlalchemy.orm import relationship

from app.models.base_model import BaseModel, Base


class MembershipStatus(PyEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    VISITOR = "visitor"
    TRANSFERRED = "transferred"


class MaritalStatus(PyEnum):
    SINGLE = "single"
    MARRIED = "married"
    DIVORCED = "divorced"
    WIDOWED = "widowed"


class Membership(BaseModel, Base):
    """Manages membership registration"""
    __tablename__ = 'members'
    # Personal Information
    first_name = Column(String(128), nullable=False)
    last_name = Column(String(128), nullable=False)
    other_names = Column(String(128), nullable=True)
    gender = Column(String(50), nullable=False)
    occupation = Column(String(100), nullable=True)
    marital_status = Column(Enum(MaritalStatus))
    date_of_birth = Column(Date, nullable=True)

    # Contact and Address Information
    email = Column(String(128), unique=False, nullable=True)
    phone_number = Column(String(50), nullable=False)
    address = Column(String(128), nullable=True)
    town_of_residence = Column(String(50), nullable=False)

    # Church Specific Information
    membership_status = Column(Enum(MembershipStatus), default=MembershipStatus.ACTIVE)
    date_joined = Column(Date, nullable=False)
    role_in_church = Column(String(50), nullable=False)
    department_id = Column(ForeignKey('departments.id'), nullable=True)
    departments = relationship('Department', back_populates='members')
    group_id = Column(ForeignKey('groups.id'), nullable=True)
    groups = relationship('Group', back_populates='members')
    last_attendance_date = ""
    attendance = relationship('Attendance', back_populates='member')


