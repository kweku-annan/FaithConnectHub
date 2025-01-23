#!/usr/bin/python3
"""Unit tests for BaseModel class"""
import unittest
from datetime import datetime
from app.models.base_model import BaseModel
import uuid


class TestBaseModel(unittest.TestCase):
    """Test cases for BaseModel class"""

    def setUp(self):
        """Set up test cases"""
        self.model = BaseModel()

    def test_init_without_kwargs(self):
        """Test initialization without kwargs"""
        self.assertIsInstance(self.model, BaseModel)
        self.assertIsInstance(self.model.id, str)
        self.assertIsInstance(self.model.created_at, datetime)
        self.assertIsInstance(self.model.updated_at, datetime)

    def test_init_with_kwargs(self):
        """Test initialization with kwargs"""
        dt = datetime.now()
        dt_iso = dt.isoformat()
        model = BaseModel(id="123", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(model.id, "123")
        self.assertEqual(model.created_at, dt)
        self.assertEqual(model.updated_at, dt)

    def test_str_representation(self):
        """Test string representation"""
        string = str(self.model)
        self.assertIn("[BaseModel]", string)
        self.assertIn(self.model.id, string)

    def test_save_method(self):
        """Test save method updates updated_at"""
        old_updated_at = self.model.updated_at
        self.model.save()
        self.assertNotEqual(old_updated_at, self.model.updated_at)

    def test_to_dict_method(self):
        """Test to_dict method"""
        model_dict = self.model.to_dict()
        self.assertIsInstance(model_dict, dict)
        self.assertEqual(model_dict["__class__"], "BaseModel")
        self.assertIsInstance(model_dict["created_at"], str)
        self.assertIsInstance(model_dict["updated_at"], str)
        self.assertEqual(model_dict["id"], self.model.id)

    def test_uuid_generation(self):
        """Test UUID generation is unique"""
        model1 = BaseModel()
        model2 = BaseModel()
        self.assertNotEqual(model1.id, model2.id)
        self.assertTrue(uuid.UUID(model1.id, version=4))

    def test_custom_attributes(self):
        """Test setting custom attributes"""
        model = BaseModel(name="Test", value=123)
        self.assertEqual(model.name, "Test")
        self.assertEqual(model.value, 123)

    def test_invalid_datetime_format(self):
        """Test handling of invalid datetime format"""
        with self.assertRaises(ValueError):
            BaseModel(created_at="invalid-date")


if __name__ == '__main__':
    unittest.main()