import jwt
import unittest
import json
from datetime import datetime, timedelta
from flask import current_app
import os
import sys

# change the path to the app.py file
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)

from app import create_app, db, bcrypt
from models.dbSchema import User
from models import Notifications

notifications = Notifications.ErrorProcessor()


class AuthLoginTestCase(unittest.TestCase):
    def setUp(self):
        """Set up test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

        # Create all tables
        db.create_all()

        # Create a sample user
        hashed_password = bcrypt.generate_password_hash(
            'TestPass123').decode('utf-8')
        user = User(
            id='test-user-id',
            fname='Test',
            lname='User',
            email='s-test.user@zewailcity.edu.eg',
            password=hashed_password
        )
        db.session.add(user)
        db.session.commit()

        self.register_url = '/auth/register'
        self.login_url = '/auth/login'
        self.logout_url = '/auth/logout'

    def tearDown(self):
        """Clean up after each test."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_register_success_zewail_email(self):
        """Test registering a user with a valid Zewailian email."""
        payload = {
            'fname': 'Jane',
            'lname': 'Doe',
            'email': 's-jane.doe@zewailcity.edu.eg',
            'userPass': 'SecurePass123'
        }
        response = self.client.post(
            self.register_url,
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['message'], notifications.process_error(
            "signup_success")['message'])

    def test_register_success_guest_email(self):
        """Test registering a user with a non-Zewailian email (Guest)."""
        payload = {
            'fname': 'John',
            'lname': 'Smith',
            'email': 'john.smith@example.com',
            'userPass': 'AnotherPass123'
        }
        response = self.client.post(
            self.register_url,
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['message'], "User Registered as a Guest")
        self.assertEqual(data['status'], "success")

    def test_register_missing_fields(self):
        """Test registering with missing fields."""
        payload = {
            'fname': 'Incomplete',
            'email': 'incomplete@example.com',
            # Missing 'lname' and 'userPass'
        }
        response = self.client.post(
            self.register_url,
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(
            data['message'], notifications.process_error("signup_invalid_password")['message'])

    def test_register_existing_email(self):
        """Test registering with an email that already exists."""
        payload = {
            'fname': 'Test',
            'lname': 'User',
            'email': 's-test.user@zewailcity.edu.eg',  # Existing email
            'userPass': 'TestPass123'
        }
        response = self.client.post(
            self.register_url,
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['message'], notifications.process_error(
            "signup_invalid_email")['message'])

    def test_login_success(self):
        """Test logging in with correct credentials."""
        payload = {
            'email': 's-test.user@zewailcity.edu.eg',
            'userPass': 'TestPass123'
        }
        response = self.client.post(
            self.login_url,
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('token', data)
        self.assertEqual(
            data['message'], notifications.process_error("login_success")['message'])

    def test_login_invalid_email(self):
        """Test logging in with an email that does not exist."""
        payload = {
            'email': 'nonexistent@zewailcity.edu.eg',
            'userPass': 'SomePass123'
        }
        response = self.client.post(
            self.login_url,
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(
            data['message'], notifications.process_error("login_invalid")['message'])

    def test_login_wrong_password(self):
        """Test logging in with an incorrect password."""
        payload = {
            'email': 's-test.user@zewailcity.edu.eg',
            'userPass': 'WrongPass123'
        }
        response = self.client.post(
            self.login_url,
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.data)
        self.assertEqual(
            data['message'], notifications.process_error("login_invalid")['message'])

    def test_token_required_protected_route(self):
        """Test accessing a protected route with a valid token."""
        protected_url = '/auth/protected'

        # First, log in to get a token
        payload = {
            'email': 's-test.user@zewailcity.edu.eg',
            'userPass': 'TestPass123'
        }
        login_response = self.client.post(
            self.login_url,
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(login_response.status_code, 200)
        data = json.loads(login_response.data)
        token = data.get('token')

        # Access the protected route with the token
        headers = {
            'x-access-token': token
        }
        response = self.client.get(
            protected_url,
            headers=headers
        )


if __name__ == '__main__':
    unittest.main()
