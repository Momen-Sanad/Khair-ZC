# server/tests/test_join_charity.py

import unittest
import json
import sys
import os
from datetime import datetime

# Adjust the path to import the Flask app and models
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)

from app import create_app, db, bcrypt  # Import the Flask app and extensions
from models.dbSchema import User, Charity, FollowedCharity  # Import necessary models
from models import Notifications

notifications = Notifications.ErrorProcessor()


class JoinCharityTestCase(unittest.TestCase):
    def setUp(self):
        """
        Set up the test environment.
        """
        # Create the Flask app with testing configuration
        self.app = create_app()
        self.app.config.from_object('config.Config')  # Ensure TestConfig is correctly referenced

        # Create a test client
        self.client = self.app.test_client()

        # Push the application context
        self.app_context = self.app.app_context()
        self.app_context.push()

        # Create all database tables
        db.create_all()

        # Create an admin user (if needed for other tests)
        hashed_password_admin = bcrypt.generate_password_hash('AdminPass123').decode('utf-8')
        self.admin = User(
            id='admin-id-456',
            fname='Admin',
            lname='User',
            email='admin.user@example.com',
            password=hashed_password_admin,
            is_admin=True  # Set admin flag
        )
        db.session.add(self.admin)

        # Create a regular user
        hashed_password_user = bcrypt.generate_password_hash('UserPass123').decode('utf-8')
        self.user = User(
            id='user-id-123',
            fname='Regular',
            lname='User',
            email='regular.user@example.com',
            password=hashed_password_user
        )
        db.session.add(self.user)

        # Create a charity for testing
        self.charity = Charity(
            id=1,
            name='Charity One',
            address='123 Charity St.',
            description='A charity for testing purposes.',
            category='Health'
        )
        db.session.add(self.charity)

        # Commit all changes to the database
        db.session.commit()

    def tearDown(self):
        """
        Clean up after each test.
        """
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def login(self, email, password):
        """
        Helper method to log in a user and obtain a JWT token.
        """
        response = self.client.post(
            '/auth/login',
            data=json.dumps({'email': email, 'userPass': password}),
            content_type='application/json'
        )
        data = json.loads(response.data)
        return data.get('token')

    def test_join_charity_success(self):
        """
        Test successfully following a charity.
        """
        # Log in as regular user to obtain the token
        token = self.login('regular.user@example.com', 'UserPass123')
        self.assertIsNotNone(token, "Token should not be None after successful login.")

        # Define the payload
        payload = {
            'user_id': self.user.id,
            'charity_id': self.charity.id
        }

        # Send POST request to follow the charity
        response = self.client.post(
            '/join/charity',
            data=json.dumps(payload),
            content_type='application/json',
            headers={'x-access-token': token}
        )

        # Assert response status code
        self.assertEqual(response.status_code, 200)

        # Assert response data
        data = json.loads(response.data)
        self.assertEqual(data['message'], "User successfully followed the charity")
        self.assertEqual(data['status'], "success")  # Assuming the status is included

        # Verify that the FollowedCharity entry exists
        followed = FollowedCharity.query.filter_by(user_id=self.user.id, charity_id=self.charity.id).first()
        self.assertIsNotNone(followed, "FollowedCharity entry should exist in the database.")

    def test_join_charity_missing_user_id(self):
        """
        Test following a charity with missing 'user_id' field.
        """
        # Log in as regular user to obtain the token
        token = self.login('regular.user@example.com', 'UserPass123')
        self.assertIsNotNone(token, "Token should not be None after successful login.")

        # Define the payload without 'user_id'
        payload = {
            # 'user_id': self.user.id,  # Missing
            'charity_id': self.charity.id
        }

        # Send POST request to follow the charity
        response = self.client.post(
            '/join/charity',
            data=json.dumps(payload),
            content_type='application/json',
            headers={'x-access-token': token}
        )

        # Assert response status code
        self.assertEqual(response.status_code, 400)

        # Assert response data
        data = json.loads(response.data)
        self.assertEqual(data['message'], notifications.process_error("user_id_required")['message'])
        self.assertEqual(data['status'], "error")

        # Verify that no FollowedCharity entry was created
        followed = FollowedCharity.query.filter_by(charity_id=self.charity.id).all()
        self.assertEqual(len(followed), 0, "No FollowedCharity entry should exist in the database.")

    def test_join_charity_missing_charity_id(self):
        """
        Test following a charity with missing 'charity_id' field.
        """
        # Log in as regular user to obtain the token
        token = self.login('regular.user@example.com', 'UserPass123')
        self.assertIsNotNone(token, "Token should not be None after successful login.")

        # Define the payload without 'charity_id'
        payload = {
            'user_id': self.user.id
            # 'charity_id': self.charity.id  # Missing
        }

        # Send POST request to follow the charity
        response = self.client.post(
            '/join/charity',
            data=json.dumps(payload),
            content_type='application/json',
            headers={'x-access-token': token}
        )

        # Assert response status code
        self.assertEqual(response.status_code, 400)

        # Assert response data
        data = json.loads(response.data)
        self.assertEqual(data['message'], notifications.process_error("charity_id_required")['message'])
        self.assertEqual(data['status'], "error")

        # Verify that no FollowedCharity entry was created
        followed = FollowedCharity.query.filter_by(user_id=self.user.id).all()
        self.assertEqual(len(followed), 0, "No FollowedCharity entry should exist in the database.")

    def test_join_charity_charity_not_found(self):
        """
        Test following a charity that does not exist.
        """
        # Log in as regular user to obtain the token
        token = self.login('regular.user@example.com', 'UserPass123')
        self.assertIsNotNone(token, "Token should not be None after successful login.")

        # Define the payload with a non-existent charity_id
        non_existent_charity_id = 999  # Assuming this ID does not exist
        payload = {
            'user_id': self.user.id,
            'charity_id': non_existent_charity_id
        }

        # Send POST request to follow the charity
        response = self.client.post(
            '/join/charity',
            data=json.dumps(payload),
            content_type='application/json',
            headers={'x-access-token': token}
        )

        # Assert response status code
        self.assertEqual(response.status_code, 404)

        # Assert response data
        data = json.loads(response.data)
        self.assertEqual(data['message'], notifications.process_error("charity_not_found")['message'])
        self.assertEqual(data['status'], "error")

        # Verify that no FollowedCharity entry was created
        followed = FollowedCharity.query.filter_by(user_id=self.user.id, charity_id=non_existent_charity_id).first()
        self.assertIsNone(followed, "FollowedCharity entry should not exist in the database.")

    def test_join_charity_already_following(self):
        """
        Test following a charity that the user is already following.
        """
        # Log in as regular user to obtain the token
        token = self.login('regular.user@example.com', 'UserPass123')
        self.assertIsNotNone(token, "Token should not be None after successful login.")

        # Define the payload
        payload = {
            'user_id': self.user.id,
            'charity_id': self.charity.id
        }

        # First, follow the charity
        response = self.client.post(
            '/join/charity',
            data=json.dumps(payload),
            content_type='application/json',
            headers={'x-access-token': token}
        )
        self.assertEqual(response.status_code, 200)

        # Attempt to follow the same charity again
        response = self.client.post(
            '/join/charity',
            data=json.dumps(payload),
            content_type='application/json',
            headers={'x-access-token': token}
        )

        # Assert response status code
        self.assertEqual(response.status_code, 400)

        # Assert response data
        data = json.loads(response.data)
        self.assertEqual(data['message'], notifications.process_error("already_following_charity")['message'])
        self.assertEqual(data['status'], "error")

        # Verify that only one FollowedCharity entry exists
        followed = FollowedCharity.query.filter_by(user_id=self.user.id, charity_id=self.charity.id).all()
        self.assertEqual(len(followed), 1, "Only one FollowedCharity entry should exist in the database.")


if __name__ == '__main__':
    unittest.main()
