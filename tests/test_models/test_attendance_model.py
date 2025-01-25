#!/usr/bin/python3
import unittest
from datetime import datetime
from app.models.attendance import Attendance
from app.models.base_model import BaseModel

class TestAttendance(unittest.TestCase):
    """Test cases for Attendance class"""

    def setUp(self):
        """Set up test cases"""
        self.attendance = Attendance()
        self.attendance.member_id = "test_member_id"
        self.attendance.event_id = "test_event_id"

    def test_attendance_instance(self):
        """Test Attendance instance creation"""
        self.assertIsInstance(self.attendance, Attendance)
        self.assertIsInstance(self.attendance, BaseModel)

    def test_attendance_attributes(self):
        """Test Attendance attributes"""
        self.assertEqual(self.attendance.member_id, "test_member_id")
        self.assertEqual(self.attendance.event_id, "test_event_id")
        self.assertEqual(self.attendance.status, "Present")
        self.assertIsNone(self.attendance.remarks)
        self.assertIsInstance(self.attendance.date, datetime)

    def test_string_representations(self):
        """Test string representations"""
        expected_str = "test_member_id - test_event_id, Status Present"
        expected_repr = "<Attendance test_member_id - test_event_id, Status Present>"

        self.assertEqual(str(self.attendance), expected_str)
        self.assertEqual(repr(self.attendance), expected_repr)

    def test_custom_status(self):
        """Test setting custom status"""
        attendance = Attendance(status="Absent")
        self.assertEqual(attendance.status, "Absent")

    def test_custom_remarks(self):
        """Test setting remarks"""
        attendance = Attendance(remarks="Test remarks")
        self.assertEqual(attendance.remarks, "Test remarks")

    def test_date_auto_set(self):
        """Test date is automatically set on creation"""
        attendance = Attendance()
        self.assertIsInstance(attendance.date, datetime)
        self.assertLessEqual((datetime.now() - attendance.date).total_seconds(), 1)

if __name__ == '__main__':
    unittest.main()