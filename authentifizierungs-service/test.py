import unittest
from unittest.mock import Mock, patch
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.User import User  
from app.services.AuthService import AuthService

class TestAuthService(unittest.TestCase):

    def setUp(self):
        self.mock_db = Mock()
        self.auth_service = AuthService(self.mock_db)

    def test_check_complete_user_incomplete_payload(self):
        incomplete_payload = {"username": "testuser"}
        response, status_code = self.auth_service.check_complete_user(incomplete_payload)
        self.assertEqual(status_code, 400)
        self.assertEqual(response['error'], 'The request payload is incomplete.')

    def test_check_complete_user_complete_payload(self):
        complete_payload = {
            "username": "testuser",
            "first_name": "Test",
            "last_name": "User",
            "password": "password123"
        }
        user = self.auth_service.check_complete_user(complete_payload)
        self.assertIsInstance(user, User)
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.first_name, "Test")
        self.assertEqual(user.last_name, "User")
        self.assertEqual(user.password, "password123")

    def test_check_if_registered_user_exists(self):
        mock_user = Mock()
        self.mock_db.users.find_one.return_value = mock_user
        user = User("testuser", "Test", "User", "password123")
        is_registered = self.auth_service.check_if_registered(user)
        self.assertTrue(is_registered)

    def test_check_if_registered_user_does_not_exist(self):
        self.mock_db.users.find_one.return_value = None
        user = User("testuser", "Test", "User", "password123")
        is_registered = self.auth_service.check_if_registered(user)
        self.assertFalse(is_registered)

    @patch('app.services.AuthService.generate_password_hash')
    def test_add_user(self, mock_generate_password_hash):
        mock_generate_password_hash.return_value = 'hashed_password'
        user = User("testuser", "Test", "User", "password123")
        response, status_code = self.auth_service.add_user(user)
        self.assertEqual(status_code, 201)
        self.assertEqual(response['message'], 'User registered successfully.')
        self.mock_db.users.insert_one.assert_called_once()
        inserted_user = self.mock_db.users.insert_one.call_args[0][0]
        self.assertEqual(inserted_user['username'], "testuser")
        self.assertEqual(inserted_user['password'], 'hashed_password')

    def test_get_user_exists(self):
        user_data = {
            "username": "testuser",
            "first_name": "Test",
            "last_name": "User",
            "password": generate_password_hash("password123")
        }
        self.mock_db.users.find_one.return_value = user_data
        user = self.auth_service.get_user("testuser")
        self.assertIsNotNone(user)
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.first_name, "Test")
        self.assertEqual(user.last_name, "User")
        self.assertTrue(check_password_hash(user.password, "password123"))

    def test_get_user_does_not_exist(self):
        self.mock_db.users.find_one.return_value = None
        user = self.auth_service.get_user("nonexistentuser")
        self.assertIsNone(user)

if __name__ == '__main__':
    unittest.main()