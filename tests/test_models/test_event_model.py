#!/usr/bin/python3
"""Unit tests for Event model"""
import unittest
from datetime import date, time
from app.models.event import Event


class TestEvent(unittest.TestCase):
    """Test cases for Event class"""

    def setUp(self):
        """Set up test cases"""
        self.event_data = {
            'name': 'Sunday Service',
            'date': date(2024, 1, 1),
            'time': time(10, 0),
            'location': 'Main Sanctuary',
            'description': 'Weekly worship service',
            'category': 'Service'
        }

    def test_event_creation(self):
        """Test Event instance creation with valid data"""
        event = Event(**self.event_data)
        self.assertEqual(event.name, 'Sunday Service')
        self.assertEqual(event.date, date(2024, 1, 1))
        self.assertEqual(event.time, time(10, 0))
        self.assertEqual(event.location, 'Main Sanctuary')
        self.assertEqual(event.description, 'Weekly worship service')
        self.assertEqual(event.category, 'Service')

    def test_default_category(self):
        """Test default category when not specified"""
        data = self.event_data.copy()
        del data['category']
        event = Event(**data)
        self.assertEqual(event.category, 'General')

    def test_string_representation(self):
        """Test string representation of Event"""
        event = Event(**self.event_data)
        expected = f"<Event Sunday Service, Date: {date(2024, 1, 1)}, Category: Service>"
        self.assertEqual(str(event), expected)

    def test_required_fields(self):
        """Test that required fields raise error when missing"""
        required_fields = ['name', 'date', 'time', 'location', 'description']
        for field in required_fields:
            data = self.event_data.copy()
            del data[field]
            with self.assertRaises(TypeError):
                Event(**data)

    def test_relationship_initialization(self):
        """Test attendance relationship initialization"""
        event = Event(**self.event_data)
        self.assertEqual(event.attendance, [])


if __name__ == '__main__':
    unittest.main()