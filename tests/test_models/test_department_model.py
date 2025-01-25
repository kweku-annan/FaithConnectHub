#!/usr/bin/env python
import unittest
from datetime import datetime
from app.models.department import Department
from app.models.base_model import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class TestDepartment(unittest.TestCase):
    """Test cases for Department model"""

    def setUp(self):
        """Set up test database"""
        self.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def tearDown(self):
        """Clean up test database"""
        Base.metadata.drop_all(self.engine)
        self.session.close()

    def test_create_department(self):
        """Test department creation with valid data"""
        dept = Department(
            name="Youth Ministry",
            description="Ministry for young people",
            leader_id="leader123"
        )
        self.assertEqual(dept.name, "Youth Ministry")
        self.assertEqual(dept.description, "Ministry for young people")
        self.assertEqual(dept.leader_id, "leader123")
        self.assertTrue(hasattr(dept, 'created_at'))
        self.assertTrue(hasattr(dept, 'updated_at'))
        self.assertTrue(hasattr(dept, 'id'))

    def test_department_relationships(self):
        """Test department relationships initialization"""
        dept = Department(
            name="Choir",
            description="Church choir department",
            leader_id="leader456"
        )
        self.assertEqual(dept.members, [])
        self.assertEqual(dept.leader, [])
        self.assertEqual(dept.financial_records, [])

    def test_department_string_representation(self):
        """Test department string representation"""
        dept = Department(
            name="Sunday School",
            description="Sunday school department",
            leader_id="leader789"
        )
        self.assertEqual(str(dept), "<Department Sunday School>")

    def test_department_required_fields(self):
        """Test department required fields validation"""
        with self.assertRaises(TypeError):
            Department()

    def test_department_timestamps(self):
        """Test department timestamps are set correctly"""
        dept = Department(
            name="Media",
            description="Media department",
            leader_id="leader101"
        )
        self.assertIsInstance(dept.created_at, datetime)
        self.assertIsInstance(dept.updated_at, datetime)

if __name__ == '__main__':
    unittest.main()