import unittest
from app.models.user import User
from app.models import storage
from werkzeug.security import generate_password_hash

class TestUser(unittest.TestCase):
    def setUp(self):
        self.user = User()
        self.user.username = "testuser"
        self.user.email = "test@example.com"
        self.user.set_password("password123")
        self.user.role = "Member"

    def test_password_hashing(self):
        """Test password hashing and verification"""
        user = User()
        user.set_password('test123')
        self.assertNotEqual(user.password, 'test123')
        self.assertTrue(user.check_password('test123'))
        self.assertFalse(user.check_password('wrongpass'))

    def test_user_creation(self):
        """Test basic user creation with default values"""
        user = User()
        self.assertTrue(user.is_active)
        self.assertEqual(user.role, 'Member')

    def test_duplicate_username_check(self):
        """Test duplicate username detection"""
        user1 = User()
        user1.username = "unique_user"
        user1.email = "user1@test.com"
        user1.set_password("pass123")
        user1.save()

        user2 = User()
        user2.username = "unique_user"
        user2.email = "user2@test.com"
        user2.set_password("pass123")

        with self.assertRaises(ValueError):
            user2.save()

    def test_duplicate_email_check(self):
        """Test duplicate email detection"""
        user1 = User()
        user1.username = "user1"
        user1.email = "same@test.com"
        user1.set_password("pass123")
        user1.save()

        user2 = User()
        user2.username = "user2"
        user2.email = "same@test.com"
        user2.set_password("pass123")

        with self.assertRaises(ValueError):
            user2.save()

    def test_user_representation(self):
        """Test string representation of User"""
        user = User()
        user.username = "testuser"
        user.role = "MEMBER"
        expected = "<User testuser, Role: Admin>"
        self.assertEqual(str(user), expected)

    def test_custom_role_assignment(self):
        """Test custom role assignment"""
        user = User()
        user.username = "admin"
        user.email = "admin@test.com"
        user.role = "Admin"
        self.assertEqual(user.role, "Admin")

    def tearDown(self):
        """Clean up after each test"""
        try:

            storage.query(User).delete()
            storage.save()
        except Exception as e:
            print(f"Error during tearDown: {e}")

if __name__ == '__main__':
    unittest.main()