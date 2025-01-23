#!/usr/bin/python3
"""Manages and keeps track of Departments in the Church
It also manages Department creation and other stuff that concerns the
departments.
Has the ability to create New departments and Ministries
Has the ability to Manage department membership

Features could include:
    Creating, editing, and deleting departments/units/ministries.
    Assigning leaders and tracking members for each department.
    Tracking activities, events, and reports for specific ministries.Features could include:

    Creating, editing, and deleting departments/units/ministries.
    Assigning leaders and tracking members for each department.
    Tracking activities, events, and reports for specific ministries.
"""
from email.policy import default

from sqlalchemy import Column, String, Table, ForeignKey, Boolean, Enum, Text, DateTime, Float
from sqlalchemy.orm import relationship, backref
from enum import Enum as PyEnum

from app.models.base_model import BaseModel, Base


class DepartmentType(PyEnum):
    MINISTRY = "ministry"
    UNIT = "unit"
    COMMITTEE = "committee"
    WORKFORCE = "workforce"


class DepartmentStatus(PyEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    ON_HOLD = "on_hold"

# Association table for activity attendees
activity_attendees = Table(
    'activity_attendees',
    BaseModel.metadata,
    Column('activity_id', String(60), ForeignKey('department_activities.id')),
    Column('member_id', String(60), ForeignKey('members.id')),
    extend_existing=True
)

# Association table for department leaders
department_leaders = Table(
    'department_leaders',
    BaseModel.metadata,
    Column('department_id', String(60), ForeignKey('departments.id')),
    Column('member_id', String(60), ForeignKey('members.id')),
    Column('role', String(50)),
    Column('is_primary', Boolean, default=False),
    extend_existing=True
)


class Department(BaseModel, Base):
    """Manages departments in the church"""
    __tablename__ = 'departments'

    # Basic information
    name = Column(String(100), nullable=False, unique=True)
    description = Column(String(255), nullable=False)
    department_type = Column(Enum(DepartmentType), nullable=False, default=DepartmentType.MINISTRY)
    status = Column(Enum(DepartmentStatus), default=DepartmentStatus.ACTIVE)

    # Department Details
    meeting_schedule = Column(String(200))
    meeting_location = Column(String(100))
    vision_statement = Column(Text)
    mission_statement = Column(Text)


    # Parent Department (for hierarchical structure)
    parent_id = Column(String(60), ForeignKey('departments.id'))

    # Relationship
    from app.models.membership import Membership
    members = relationship('Membership', back_populates='departments', foreign_keys=['Membership.department_id'])
    leaders = relationship(
        'Membership',
        secondary=department_leaders,
        backref="leading_departments"
    )
    activities = relationship("DepartmentActivity", back_populates='department')
    reports = relationship('DepartmentReport', back_populates='department')
    incomes = relationship("Income", back_populates="department")
    expenses = relationship("Expense", back_populates="department")
    budget_items = relationship("BudgetItem", back_populates='department')
    groups = relationship('Group', back_populates='department')
    parent = relationship('Department', remote_side='Department.id')

    def add_leader(self, member, role='Leader', is_primary=False):
        """Add a leader to the department"""
        connection = department_leaders.insert().values(
            department_id=self.id,
            member_id=member.id,
            role=role,
            is_primary=is_primary
        )
        return connection

    def remove_leader(self, member):
        """Remove a leader from the department"""
        connection = department_leaders.delete().where(
            department_leaders.c.department_id == self.id,
            department_leaders.c.member_id == member.id
        )
        return connection

    def get_member_count(self):
        """Get total number of members in the department"""
        return len(self.members)

    def get_active_members(self):
        """Get list of active members in the department"""
        return [member for member in self.members if member.membership_status == 'active']


class DepartmentActivity(BaseModel, Base):
    """Records and tracks the departments activities"""
    __tablename__ ='department_activities'

    department_id = Column(String(60), ForeignKey('departments.id'), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime)
    status = Column(String(50)) # planned, ongoing, completed, cancelled
    location = Column(String(100))
    budget = Column(Float)

    # Relationships
    department = relationship('Department', back_populates='activities')
    attendees = relationship(
        'Membership',
        secondary='activity_attendees',
        back_populates='activities_attended',
        foreign_keys=[activity_attendees.c.activity_id, activity_attendees.c.member_id]
    )


class DepartmentReport(BaseModel, Base):
    """Records departments reports"""
    __tablename__ = 'department_reports'

    department_id = Column(String(60), ForeignKey('departments.id'), nullable=False)
    report_date = Column(DateTime, nullable=False)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    report_type = Column(String(50))
    submitted_by_id = Column(String(60), ForeignKey('members.id'))
    status = Column(String(50))

    department = relationship('Department', back_populates='reports')
    submitted_by = relationship("Membership")

