#!/usr/bin/python3
"""Handles income, expenses, budgeting, and financial reporting


TODO 1:  Income Management
     --  Track donations, tithes, offerings, and other sources of income.
     -- Categorize income by type (e.g., general offering, building fund,
        mission donations).
     -- Allow recording of donor details (optional for anonymity).

TODO 2: Expense Management
     -- Track expenditures by category (e.g., salaries, maintenance, events).
     -- Record the purpose and amount for each expense.
     -- Associate expenses with specific events, departments, or projects (optional).
"""
from datetime import datetime

from sqlalchemy import Column, Float, Enum, DateTime, String, ForeignKey, Boolean, Text, func, Integer
from sqlalchemy.orm import relationship

from app.models.base_model import BaseModel, Base
from enum import Enum as PyEnum


class IncomeType(PyEnum):
    TITHE = "tithe"
    OFFERING = "offering"
    SPECIAL_OFFERING = "special_offering"
    BUILDING_FUND = "building_fund"
    MISSION_FUND = "mission_fund"
    DONATION = "donation"
    OTHER = "other"


class PaymentMethod(PyEnum):
    CASH = "cash"
    CHECK = "check"
    BANK_TRANSFER = "bank_transfer"
    CREDIT_CARD = "credit_card"
    MOBILE_MONEY = "mobile_money"
    ONLINE_PAYMENT = "online_payment"


class ExpenseCategory(PyEnum):
    UTILITIES = "utilities"
    SALARY = "salary"
    MAINTENANCE = "maintenance"
    EVENTS = "events"
    MISSIONS = "missions"
    EQUIPMENT = "equipment"
    SUPPLIES = "supplies"
    ADMINISTRATIVE = "administrative"
    OTHER = "other"


class Income(BaseModel, Base):
    __tablename__ = "incomes"

    # Basic Information
    amount = Column(Float, nullable=False)
    income_type = Column(Enum(IncomeType), nullable=False)
    payment_method = Column(Enum(PaymentMethod))
    transaction_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    reference_number = Column(String(50), unique=True)  # For receipts/tracking

    # Source Information
    donor_id = Column(String(50), ForeignKey('members.id')) # Optional for anonymous donations
    is_anonymous = Column(Boolean, default=False)

    # Additional Details
    description = Column(Text)
    purpose = Column(String(200))

    # Department/Event Association
    department_id = Column(String(50), ForeignKey('departments.id'))
    event_id = Column(String(50), ForeignKey('events.id'))

    # Relationships
    donor = relationship("Membership", back_populates="donations")
    department = relationship("Department", back_populates="incomes")
    event = relationship("Event", back_populates="incomes")

    def generate_receipt(self):
        """Generate a receipt for the income"""
        receipt_data = {
            'receipt_number': self.reference_number,
            'date': self.transaction_date,
            'amount': self.amount,
            'type': self.income_type.value,
            'donor': 'Anonymous' if self.is_anonymous else self.donor.get_full_name(),
            'purpose': self.purpose
        }
        return receipt_data

    @classmethod
    def get_total_by_type(cls, session, start_date, end_date, income_type=None):
        """Get total income by type within a date range"""
        query = session.query(func.sum(cls.amount))
        if income_type:
            query = query.filter(cls.income_type == income_type)
        return query.filter(
            cls.transaction_date.between(start_date, end_date)
        ).scalar() or 0.0


class Expense(BaseModel, Base):
    """Tracks Expenses"""
    __tablename__ = 'expenses'

    # Basic information
    amount = Column(Float, nullable=False)
    expense_category = Column(Enum(ExpenseCategory), nullable=False)
    transaction_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    reference_number = Column(String(50), unique=True)

    # Payment details
    payment_method = Column(Enum(PaymentMethod))
    payee = Column(String(100))  # Person or organization paid
    invoice_number = Column(String(50))

    # Description and Purpose
    description = Column(Text, nullable=False)
    purpose = Column(String(200))

    # Association
    department_id = Column(String(50), ForeignKey('departments.id'))
    event_id = Column(String(50), ForeignKey('events.id'))
    approved_by_id = Column(String(50), ForeignKey('members.id'))

    # Relationships
    department = relationship("Department", back_populates="expenses")
    event = relationship("Event", back_populates="expenses")
    approved_by = relationship("Member")

    # Budget Tracking
    budget_item_id = Column(String(50), ForeignKey('budget_items.id'))
    is_budgeted = Column(Boolean, default=False)

    @classmethod
    def get_total_by_category(cls, session, start_date, end_date, category=None):
        """Get total expenses by category within a date range"""
        query = session.query(func.sum(cls.amount))
        if category:
            query = query.filter(cls.expense_category == category)
        return query.filter(
            cls.transaction_date.between(start_date, end_date)
        ).scalar() or 0.0


class BudgetItem(BaseModel, Base):
    """Tracks and manages budget"""
    __tablename__ = 'budget_item'

    # Budget Information
    fiscal_year = Column(Integer, nullable=False)
    category = Column(Enum(ExpenseCategory), nullable=False)
    allocated_amount = Column(Float, nullable=False)


    # Details
    description = Column(Text)
    department_id = Column(String(50), ForeignKey('departments.id'))

    # Tracking
    current_spent = Column(Float, default=0.0)
    last_updated = Column(DateTime, onupdate=datetime.utcnow)

    # Relationships
    expenses = relationship("Expense", back_populates="budget_item")
    department = relationship("Department", back_populates='budget_items')

    def get_remaining_budget(self):
        """Calculate remaining budget"""
        return self.allocated_amount - self.current_spent

    def is_over_budget(self):
        """Check if expenses exceed budget"""
        return self.current_spent > self.allocated_amount


class FinancialReport(BaseModel, Base):
    """Manages Financial Report"""
    __tablename__ = 'financial_reports'

    # Report Information
    title = Column(String(200), nullable=False)
    report_type = Column(String(50))  # monthly, quarterly, annual
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)

    # Content
    summary = Column(Text)
    total_income = Column(Float)
    total_expenses = Column(Float)
    net_amount = Column(Float)

    # Meta
    generated_by_id = Column(String(50), ForeignKey('members.id'))
    generated_at = Column(DateTime, default=datetime.utcnow)

    def generate_summary(self, session):
        """Generate financial summary for the report period"""
        income_total = Income.get_total_by_type(
            session, self.start_date, self.end_date
        )
        expense_total = Expense.get_total_by_category(
            session, self.start_date, self.end_date
        )

        self.total_income = income_total
        self.total_income = expense_total
        self.net_amount = income_total - expense_total

        return {
            'total_income': self.total_income,
            'total_expenses': self.total_expenses,
            'net_amount': self.net_amount,
            'period': f"{self.start_date.date()} to {self.end_date.date()}"
        }



