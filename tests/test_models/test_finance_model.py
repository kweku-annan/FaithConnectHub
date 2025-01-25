#!/usr/bin/env python3
"""Unit tests for Financial Record model"""
import unittest
from datetime import datetime
from app.models.finance import FinancialRecord


class TestFinancialRecord(unittest.TestCase):
    """Test cases for FinancialRecord class"""

    def setUp(self):
        """Set up test cases"""
        self.test_record = FinancialRecord(
            type="Income",
            amount=1000.00,
            description="Sunday offering",
            category="offering",
            donor="John Doe"
        )

    def test_init(self):
        """Test initialization of FinancialRecord"""
        self.assertEqual(self.test_record.type, "Income")
        self.assertEqual(self.test_record.amount, 1000.00)
        self.assertEqual(self.test_record.description, "Sunday offering")
        self.assertEqual(self.test_record.category, "offering")
        self.assertEqual(self.test_record.donor, "John Doe")
        self.assertIsInstance(self.test_record.date, datetime)

    def test_str_representation(self):
        """Test string representation"""
        expected = "Income - offering, Amount 1000.0"
        self.assertEqual(str(self.test_record), expected)

    def test_repr_representation(self):
        """Test repr representation"""
        expected = "<FinancialRecord Income - offering, Amount 1000.0>"
        self.assertEqual(repr(self.test_record), expected)

    def test_expense_without_donor(self):
        """Test expense record without donor"""
        expense = FinancialRecord(
            type="Expense",
            amount=500.00,
            description="Office supplies",
            category="supplies"
        )
        self.assertIsNone(expense.donor)
        self.assertEqual(expense.type, "Expense")

    def test_relationships_initialization(self):
        """Test relationship fields initialization"""
        record = FinancialRecord(
            type="Income",
            amount=750.00,
            description="Event donation",
            category="donation"
        )
        self.assertIsNone(record.event)
        self.assertIsNone(record.department)
        self.assertIsNone(record.group)

    def test_amount_float_conversion(self):
        """Test amount stored as float"""
        record = FinancialRecord(
            type="Income",
            amount="1500.50",
            description="Test amount",
            category="tithe"
        )
        self.assertIsInstance(record.amount, float)
        self.assertEqual(record.amount, 1500.50)


if __name__ == '__main__':
    unittest.main()