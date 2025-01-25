#!/usr/bin/env python3
"""Manages financial records and transactions for the church"""
from datetime import datetime

from app.models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Float, ForeignKey, Text, Date
from sqlalchemy.orm import relationship


class FinancialRecord(BaseModel, Base):
    """Tracks and manages financial records and transactions"""
    __tablename__ = 'financial_records'

    type = Column(String(50), nullable=False) # Income or Expense
    amount = Column(Float, nullable=False, default=0.0)
    description = Column(Text, nullable=False)
    category = Column(String(50), nullable=False) # e.g., tithe, offering, donation, salaries, etc
    date = Column(Date, nullable=False, default=datetime.now)

    donor = Column(String(100), nullable=True) # Optional for expenses
    event_id = Column(String(60), ForeignKey('events.id'), nullable=True)
    department_id = Column(String(60), ForeignKey('departments.id'), nullable=True)
    group_id = Column(String(60), ForeignKey('groups.id'), nullable=True)

    # Relationships
    event = relationship("Event", back_populates="financial_records")
    department = relationship("Department", back_populates="financial_records")
    group = relationship("Group", back_populates="financial_records")

    def __init__(self, *args, **kwargs):
        """Initializes the FinancialRecord instance"""
        super().__init__(*args, **kwargs)
        self.date = datetime.now()


    def __repr__(self):
        return f"<FinancialRecord {self.type} - {self.category}, Amount {self.amount}>"

    def __str__(self):
        return f"{self.type} - {self.category}, Amount {self.amount}"

