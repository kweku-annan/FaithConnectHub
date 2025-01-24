#!/usr/bin/env python3
"""Model for tracking and understanding members engagement"""
from app.models.base_model import BaseModel, Base
from datetime import datetime
from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship


class Member(BaseModel, Base):
    """Tracks and organizes church members"""
    __tablename__ = 'members'

    # Personal Information
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(120), nullable=False, unique=True)
    phone_number = Column(String(20), nullable=False)
    address = Column(String(120), nullable=False)
    date_of_birth = Column(DateTime, nullable=False)
    gender = Column(String(10), nullable=False)
    marital_status = Column(String(20), nullable=False)

    # Church Information
    status = Column(String(20), nullable=False, default='active')  # active, inactive, suspended
    role = Column(String(20), nullable=False, default='Member')  # member, leader, admin, pastor
    date_joined = Column(DateTime, nullable=False)
    department_id = Column(String(60), ForeignKey('departments.id'), nullable=True)
    group_id = Column(String(60), ForeignKey('groups.id'), nullable=True)

    # Relationships
    user = relationship("User", back_populates="member")
    department = relationship("Department", back_populates="members")
    group = relationship("Group", back_populates="members")
    attendance = relationship("Attendance", back_populates="member")


    def __init__(self, *args, **kwargs):
        """Initializes the Member instance"""
        super().__init__(*args, **kwargs)
        self.date_joined = self.date_joined or datetime.now()
        self.status = self.status or 'active'
        self.role = self.role or 'Member'

    def __repr__(self):
        return f"<Member {self.first_name} {self.last_name}, Role: {self.role}>"