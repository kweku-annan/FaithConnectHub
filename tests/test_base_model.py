import unittest

from app.models import storage
from app.models.base_model import BaseModel
from datetime import datetime

class TestBaseModel(unittest.TestCase):

    def test_initializes_attributes_correctly(self):
        model = BaseModel(name="Test Model", my_number=42)
        self.assertEqual(model.name, "Test Model")
        self.assertEqual(model.my_number, 42)
        self.assertIsNotNone(model.id)
        self.assertIsInstance(model.created_at, datetime)
        self.assertIsInstance(model.updated_at, datetime)

    def test_string_representation_is_correct(self):
        model = BaseModel(name="Test Model")
        expected_str = f"[BaseModel] ({model.id}) {model.__dict__}"
        self.assertEqual(str(model), expected_str)

    def test_soft_delete_sets_correct_attributes(self):
        model = BaseModel()
        model.soft_delete(deleted_by_id="user_123")
        self.assertTrue(model.is_deleted)
        self.assertIsNotNone(model.deleted_at)
        self.assertEqual(model.deleted_by_id, "user_123")

    def test_save_updates_updated_at(self):
        model = BaseModel()
        old_updated_at = model.updated_at
        model.save()
        self.assertNotEqual(model.updated_at, old_updated_at)

    def test_to_dict_returns_correct_dict(self):
        model = BaseModel(name="Test Model")
        model_dict = model.to_dict()
        self.assertEqual(model_dict["name"], "Test Model")
        self.assertEqual(model_dict["__class__"], "BaseModel")
        self.assertEqual(model_dict["id"], model.id)
        self.assertEqual(model_dict["created_at"], model.created_at.isoformat())
        self.assertEqual(model_dict["updated_at"], model.updated_at.isoformat())

    def test_delete_removes_instance_from_storage(self):
        model = BaseModel()
        model.delete()
        self.assertNotIn(model, storage.all().values())

if __name__ == "__main__":
    unittest.main()