#!/usr/bin/env python3
import unittest
from datetime import datetime
from app.models.member import Member

class TestMember(unittest.TestCase):
    """Test cases for Member model"""

    def setUp(self):
        """Set up test cases"""
        self.valid_member_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'phone_number': '1234567890',
            'address': '123 Main St',
            'date_of_birth': datetime(1990, 1, 1),
            'gender': 'Male',
            'marital_status': 'Single'
        }

    def test_member_initialization(self):
        """Test member creation with valid data"""
        member = Member(**self.valid_member_data)
        self.assertEqual(member.first_name, 'John')
        self.assertEqual(member.last_name, 'Doe')
        self.assertEqual(member.email, 'john.doe@example.com')
        self.assertEqual(member.status, 'active')
        self.assertEqual(member.role, 'Member')
        self.assertIsInstance(member.date_joined, datetime)

    def test_default_values(self):
        """Test default values are set correctly"""
        member = Member(**self.valid_member_data)
        self.assertEqual(member.status, 'active')
        self.assertEqual(member.role, 'Member')
        self.assertIsNotNone(member.date_joined)

    def test_custom_role_and_status(self):
        """Test setting custom role and status"""
        data = self.valid_member_data.copy()
        data.update({'role': 'pastor', 'status': 'inactive'})
        member = Member(**data)
        self.assertEqual(member.role, 'pastor')
        self.assertEqual(member.status, 'inactive')

    def test_string_representation(self):
        """Test the string representation of Member"""
        member = Member(**self.valid_member_data)
        expected_str = f"<Member John Doe, Role: Member>"
        self.assertEqual(str(member), expected_str)

    def test_date_joined_override(self):
        """Test custom date_joined value"""
        custom_date = datetime(2020, 1, 1)
        data = self.valid_member_data.copy()
        data['date_joined'] = custom_date
        member = Member(**data)
        self.assertEqual(member.date_joined, custom_date)

if __name__ == '__main__':
    unittest.main()