#!/usr/bin/python3
"""Unit tests for BaseModel class"""
import unittest
from datetime import datetime
from unittest.mock import patch
import uuid

from app.models.base_model import BaseModel
from app import models


class TestBaseModel(unittest.TestCase):
    """Test cases for BaseModel class"""

    def setUp(self):
        """Set up test cases"""
        self.base_model = BaseModel()

    def test_instance_creation(self):
        """Test if BaseModel instance is created correctly"""
        self.assertIsInstance(self.base_model, BaseModel)
        self.assertTrue(hasattr(self.base_model, 'id'))
        self.assertTrue(hasattr(self.base_model, 'created_at'))
        self.assertTrue(hasattr(self.base_model, 'updated_at'))

    def test_id_generation(self):
        """Test if id is generated as UUID string"""
        self.assertIsInstance(self.base_model.id, str)
        # Verify it's a valid UUID
        uuid.UUID(self.base_model.id)

    def test_timestamps(self):
        """Test if timestamps are datetime objects"""
        self.assertIsInstance(self.base_model.created_at, datetime)
        self.assertIsInstance(self.base_model.updated_at, datetime)

    def test_str_representation(self):
        """Test string representation of BaseModel"""
        string = str(self.base_model)
        self.assertIn("[BaseModel]", string)
        self.assertIn(self.base_model.id, string)

    @patch('app.models.storage')
    def test_save_method(self, mock_storage):
        """Test save method updates timestamp and calls storage"""
        old_updated_at = self.base_model.updated_at
        self.base_model.save()

        self.assertNotEqual(old_updated_at, self.base_model.updated_at)
        mock_storage.new.assert_called_once_with(self.base_model)
        mock_storage.save.assert_called_once()

    def test_to_dict_method(self):
        """Test dictionary representation of BaseModel"""
        base_dict = self.base_model.to_dict()

        self.assertIsInstance(base_dict, dict)
        self.assertEqual(base_dict['__class__'], 'BaseModel')
        self.assertIn('id', base_dict)
        self.assertNotIn('_sa_instance_state', base_dict)

    @patch('app.models.storage')
    def test_delete_method(self, mock_storage):
        """Test delete method calls storage delete"""
        self.base_model.delete()
        mock_storage.delete.assert_called_once_with(self.base_model)


if __name__ == '__main__':
    unittest.main()
