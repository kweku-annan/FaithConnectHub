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
from app.models.base_model import BaseModel


class Income(BaseModel):
    """Tracks Income"""
    date = None
    amount = ""
    source = ""
    payment_method = ""
    notes = ""


class Expense(BaseModel):
    """Tracks Expenses"""
    date = None
    amount = ""
    category = ""
    description = ""


