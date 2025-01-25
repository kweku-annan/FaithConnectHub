#!/usr/bin/env python
import unittest
from app.models.group import Group
from app.models.member import Member
from app.models.department import Department

class TestGroup(unittest.TestCase):
    """Test cases for Group model"""

    def setUp(self):
        """Set up test cases"""
        self.group_data = {
            "name": "Youth Ministry",
            "description": "Church youth group",
            "leader_id": "leader123",
            "department_id": "dept123"
        }
        self.group = Group(**self.group_data)

    def test_group_instance(self):
        """Test Group instance creation"""
        self.assertIsInstance(self.group, Group)
        self.assertEqual(self.group.name, self.group_data["name"])
        self.assertEqual(self.group.description, self.group_data["description"])
        self.assertEqual(self.group.leader_id, self.group_data["leader_id"])
        self.assertEqual(self.group.department_id, self.group_data["department_id"])

    def test_group_attributes(self):
        """Test Group model attributes"""
        self.assertTrue(hasattr(self.group, "id"))
        self.assertTrue(hasattr(self.group, "created_at"))
        self.assertTrue(hasattr(self.group, "updated_at"))
        self.assertTrue(hasattr(self.group, "name"))
        self.assertTrue(hasattr(self.group, "description"))
        self.assertTrue(hasattr(self.group, "leader_id"))
        self.assertTrue(hasattr(self.group, "department_id"))

    def test_group_relationships(self):
        """Test Group relationships are defined"""
        self.assertTrue(hasattr(self.group, "members"))
        self.assertTrue(hasattr(self.group, "leader"))
        self.assertTrue(hasattr(self.group, "department"))
        self.assertTrue(hasattr(self.group, "financial_records"))
        self.assertTrue(hasattr(self.group, "event"))

    def test_string_representation(self):
        """Test string representation of Group"""
        expected = f"<Group {self.group_data['name']}>"
        self.assertEqual(str(self.group), expected)

    def test_tablename(self):
        """Test correct table name"""
        self.assertEqual(Group.__tablename__, 'groups')

if __name__ == '__main__':
    unittest.main()