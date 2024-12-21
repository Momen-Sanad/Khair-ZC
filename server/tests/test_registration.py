# Import necessary models
import unittest
import json
import sys
import os
from flask import url_for
import datetime

# Adjust the path to import the Flask app and models
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)

from app import create_app, db, bcrypt  # Import the Flask app and extensions
from models.dbSchema import User, Campaign, RegisteredCampaign,Charity

class RegistrationTestCase(unittest.TestCase):
    def setUp(self):
        """
        Set up the test environment.
        """
        # Create the Flask app with testing configuration
        self.app = create_app()
        # Ensure TestConfig is correctly referenced
        self.app.config.from_object('config.Config')

        # Create a test client
        self.client = self.app.test_client()

        # Push the application context
        self.app_context = self.app.app_context()
        self.app_context.push()

        # Create all database tables
        db.create_all()

        # Create a regular user
        hashed_password_user = bcrypt.generate_password_hash(
            'UserPass123').decode('utf-8')
        self.user = User(
            id='user-id-123',
            fname='Regular',
            lname='User',
            email='regular.user@example.com',
            password=hashed_password_user
        )
        db.session.add(self.user)

        # Create an admin user
        hashed_password_admin = bcrypt.generate_password_hash(
            'AdminPass123').decode('utf-8')
        self.admin = User(
            id='admin-id-456',
            fname='Admin',
            lname='User',
            email='admin.user@example.com',
            password=hashed_password_admin,
            is_admin=True  # Set admin flag
        )
        db.session.add(self.admin)
        
        # Create a campaign with capacity 1 for testing
        self.campaign = Campaign(
            id=1,
            name='Test Charity',
            address= '6th of october',
            description='A charity for testing purposes',
            category='whatever',
        )

        # Create a campaign with capacity 1 for testing
        self.campaign = Campaign(
            id=1,
            title='Test Campaign',
            description='A campaign for testing purposes.',
            date=datetime.date.today(),
            reward=100,
            charity_id=1,  # Assuming charity with id=1 exists or adjust accordingly
            capacity=1
            
        )
        db.session.add(self.campaign)

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
        Helper method to log in a user and return the test client session.
        """
        return self.client.post(
            '/auth/login',
            data=json.dumps({'email': email, 'userPass': password}),
            content_type='application/json'
        )

    def test_register_user_for_campaign_success(self):
        """
        Test registering a user for a campaign successfully.
        """
        # Log in as the regular user
        response = self.login('regular.user@example.com', 'UserPass123')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        token = data.get('token')
        self.assertIsNotNone(
            token, "Token should not be None after successful login.")

        # Register for the campaign
        response = self.client.post(
            '/registration/register',
            data=json.dumps({'campaign_id': self.campaign.id,
                            'current_id': self.user.id}),
            content_type='application/json',
            headers={'x-access-token': token}
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        # As per ErrorProcessor
        self.assertEqual(data['message'], "campaign_attended")
        self.assertEqual(data['status'], "success")

    # def test_register_user_for_campaign_missing_fields(self):
    #     """
    #     Test registering a user for a campaign with missing fields.
    #     """
    #     # Log in as the regular user
    #     response = self.login('regular.user@example.com', 'UserPass123')
    #     self.assertEqual(response.status_code, 200)
    #     data = json.loads(response.data)
    #     token = data.get('token')
    #     self.assertIsNotNone(
    #         token, "Token should not be None after successful login.")

    #     # Attempt to register without 'campaign_id'
    #     response = self.client.post(
    #         '/registration/register',
    #         data=json.dumps({'current_id': self.user.id}),
    #         content_type='application/json',
    #         headers={'x-access-token': token}
    #     )
    #     self.assertEqual(response.status_code, 400)
    #     data = json.loads(response.data)
    #     self.assertEqual(data['message'], "campaign_id_missing")
    #     self.assertEqual(data['status'], "error")

    # def test_register_user_for_campaign_invalid_campaign(self):
    #     """
    #     Test registering a user for a non-existent campaign.
    #     """
    #     # Log in as the regular user
    #     response = self.login('regular.user@example.com', 'UserPass123')
    #     self.assertEqual(response.status_code, 200)
    #     data = json.loads(response.data)
    #     token = data.get('token')
    #     self.assertIsNotNone(
    #         token, "Token should not be None after successful login.")

    #     # Attempt to register for a campaign that doesn't exist
    #     invalid_campaign_id = 999
    #     response = self.client.post(
    #         '/registration/register',
    #         data=json.dumps(
    #             {'campaign_id': invalid_campaign_id, 'current_id': self.user.id}),
    #         content_type='application/json',
    #         headers={'x-access-token': token}
    #     )
    #     self.assertEqual(response.status_code, 404)
    #     data = json.loads(response.data)
    #     self.assertEqual(data['message'], "campaign_not_found")
    #     self.assertEqual(data['status'], "error")

    # def test_register_user_already_registered(self):
    #     """
    #     Test registering a user for a campaign they're already registered for.
    #     """
    #     # Log in as the regular user
    #     response = self.login('regular.user@example.com', 'UserPass123')
    #     self.assertEqual(response.status_code, 200)
    #     data = json.loads(response.data)
    #     token = data.get('token')
    #     self.assertIsNotNone(
    #         token, "Token should not be None after successful login.")

    #     # Register for the campaign first time
    #     response = self.client.post(
    #         '/registration/register',
    #         data=json.dumps({'campaign_id': self.campaign.id,
    #                         'current_id': self.user.id}),
    #         content_type='application/json',
    #         headers={'x-access-token': token}
    #     )
    #     self.assertEqual(response.status_code, 201)

    #     # Attempt to register again for the same campaign
    #     response = self.client.post(
    #         '/registration/register',
    #         data=json.dumps({'campaign_id': self.campaign.id,
    #                         'current_id': self.user.id}),
    #         content_type='application/json',
    #         headers={'x-access-token': token}
    #     )
    #     self.assertEqual(response.status_code, 400)
    #     data = json.loads(response.data)
    #     self.assertEqual(data['message'], "user_already_registered")
    #     self.assertEqual(data['status'], "error")

    # def test_register_user_campaign_full(self):
    #     """
    #     Test registering a user for a campaign that has reached its capacity.
    #     """
    #     # Log in as the regular user
    #     response = self.login('regular.user@example.com', 'UserPass123')
    #     self.assertEqual(response.status_code, 200)
    #     data = json.loads(response.data)
    #     token = data.get('token')
    #     self.assertIsNotNone(
    #         token, "Token should not be None after successful login.")

    #     # Register for the campaign (capacity is 1)
    #     response = self.client.post(
    #         '/registration/register',
    #         data=json.dumps({'campaign_id': self.campaign.id,
    #                         'current_id': self.user.id}),
    #         content_type='application/json',
    #         headers={'x-access-token': token}
    #     )
    #     self.assertEqual(response.status_code, 201)

    #     # Create another user
    #     hashed_password_another = bcrypt.generate_password_hash(
    #         'AnotherPass123').decode('utf-8')
    #     another_user = User(
    #         id='another-user-id-789',
    #         fname='Another',
    #         lname='User',
    #         email='another.user@example.com',
    #         password=hashed_password_another
    #     )
    #     db.session.add(another_user)
    #     db.session.commit()

    #     # Log in as the new user
    #     response = self.login('another.user@example.com', 'AnotherPass123')
    #     self.assertEqual(response.status_code, 200)
    #     data = json.loads(response.data)
    #     token_another = data.get('token')
    #     self.assertIsNotNone(
    #         token_another, "Token should not be None after successful login.")

    #     # Attempt to register for the full campaign
    #     response = self.client.post(
    #         '/registration/register',
    #         data=json.dumps({'campaign_id': self.campaign.id,
    #                         'current_id': another_user.id}),
    #         content_type='application/json',
    #         headers={'x-access-token': token_another}
    #     )
    #     self.assertEqual(response.status_code, 400)
    #     data = json.loads(response.data)
    #     self.assertEqual(data['message'], "campaign_full")
    #     self.assertEqual(data['status'], "error")

    # def test_remove_user_from_campaign_as_admin_success(self):
    #     """
    #     Test removing a user from a campaign successfully by an admin.
    #     """
    #     # First, log in as the regular user and register for the campaign
    #     login_response = self.login('regular.user@example.com', 'UserPass123')
    #     self.assertEqual(login_response.status_code, 200)
    #     data = json.loads(login_response.data)
    #     user_token = data.get('token')
    #     self.assertIsNotNone(user_token)

    #     # Register for the campaign
    #     response = self.client.post(
    #         '/registration/register',
    #         data=json.dumps({'campaign_id': self.campaign.id,
    #                         'current_id': self.user.id}),
    #         content_type='application/json',
    #         headers={'x-access-token': user_token}
    #     )
    #     self.assertEqual(response.status_code, 201)

    #     # Log in as admin
    #     login_response_admin = self.login(
    #         'admin.user@example.com', 'AdminPass123')
    #     self.assertEqual(login_response_admin.status_code, 200)
    #     data_admin = json.loads(login_response_admin.data)
    #     admin_token = data_admin.get('token')
    #     self.assertIsNotNone(admin_token)

    #     # Remove the user from the campaign
    #     response = self.client.post(
    #         '/registration/remove_user',
    #         data=json.dumps({'campaign_id': self.campaign.id,
    #                         'current_id': self.user.id}),
    #         content_type='application/json',
    #         headers={'x-access-token': admin_token}
    #     )
    #     self.assertEqual(response.status_code, 200)
    #     data = json.loads(response.data)
    #     self.assertEqual(data['message'], "removal_success")
    #     self.assertEqual(data['status'], "success")

    # def test_remove_user_from_campaign_as_admin_invalid_campaign(self):
    #     """
    #     Test removing a user from a non-existent campaign by an admin.
    #     """
    #     # Log in as admin
    #     login_response_admin = self.login(
    #         'admin.user@example.com', 'AdminPass123')
    #     self.assertEqual(login_response_admin.status_code, 200)
    #     data_admin = json.loads(login_response_admin.data)
    #     admin_token = data_admin.get('token')
    #     self.assertIsNotNone(admin_token)

    #     # Attempt to remove a user from a non-existent campaign
    #     invalid_campaign_id = 999
    #     response = self.client.post(
    #         '/registration/remove_user',
    #         data=json.dumps(
    #             {'campaign_id': invalid_campaign_id, 'current_id': self.user.id}),
    #         content_type='application/json',
    #         headers={'x-access-token': admin_token}
    #     )
    #     self.assertEqual(response.status_code, 404)
    #     data = json.loads(response.data)
    #     self.assertEqual(data['message'], "campaign_not_found")
    #     self.assertEqual(data['status'], "error")

    # def test_remove_user_from_campaign_as_admin_user_not_registered(self):
    #     """
    #     Test removing a user who is not registered for the campaign by an admin.
    #     """
    #     # Log in as admin
    #     login_response_admin = self.login(
    #         'admin.user@example.com', 'AdminPass123')
    #     self.assertEqual(login_response_admin.status_code, 200)
    #     data_admin = json.loads(login_response_admin.data)
    #     admin_token = data_admin.get('token')
    #     self.assertIsNotNone(admin_token)

    #     # Attempt to remove a user who isn't registered
    #     response = self.client.post(
    #         '/registration/remove_user',
    #         data=json.dumps({'campaign_id': self.campaign.id,
    #                         'current_id': self.user.id}),
    #         content_type='application/json',
    #         headers={'x-access-token': admin_token}
    #     )
    #     self.assertEqual(response.status_code, 404)
    #     data = json.loads(response.data)
    #     self.assertEqual(data['message'], "user_not_registered")
    #     self.assertEqual(data['status'], "error")

    # def test_remove_user_from_campaign_as_non_admin_forbidden(self):
    #     """
    #     Test removing a user from a campaign by a non-admin user (should fail).
    #     """
    #     # Log in as the regular user
    #     response = self.login('regular.user@example.com', 'UserPass123')
    #     self.assertEqual(response.status_code, 200)
    #     data = json.loads(response.data)
    #     user_token = data.get('token')
    #     self.assertIsNotNone(user_token)

    #     # Attempt to remove a user (self-removal or another user)
    #     response = self.client.post(
    #         '/registration/remove_user',
    #         data=json.dumps({'campaign_id': self.campaign.id,
    #                         'current_id': self.user.id}),
    #         content_type='application/json',
    #         headers={'x-access-token': user_token}  # Non-admin token
    #     )
    #     self.assertEqual(response.status_code, 403)
    #     data = json.loads(response.data)
    #     # As per ErrorProcessor
    #     self.assertEqual(data['message'], "login_invalid")

    # def test_register_user_for_campaign_as_admin(self):
    #     """
    #     Optional: Test that an admin can register a user for a campaign.
    #     """
    #     # Log in as admin
    #     login_response_admin = self.login(
    #         'admin.user@example.com', 'AdminPass123')
    #     self.assertEqual(login_response_admin.status_code, 200)
    #     data_admin = json.loads(login_response_admin.data)
    #     admin_token = data_admin.get('token')
    #     self.assertIsNotNone(admin_token)

    #     # Register another user for the campaign
    #     # Create another user
    #     hashed_password_another = bcrypt.generate_password_hash(
    #         'AnotherPass123').decode('utf-8')
    #     another_user = User(
    #         id='another-user-id-789',
    #         fname='Another',
    #         lname='User',
    #         email='another.user@example.com',
    #         password=hashed_password_another
    #     )
    #     db.session.add(another_user)
    #     db.session.commit()

    #     # Register the new user for the campaign as admin
    #     response = self.client.post(
    #         '/registration/register',
    #         data=json.dumps({'campaign_id': self.campaign.id,
    #                         'current_id': another_user.id}),
    #         content_type='application/json',
    #         headers={'x-access-token': admin_token}
    #     )
    #     self.assertEqual(response.status_code, 201)
    #     data = json.loads(response.data)
    #     self.assertEqual(data['message'], "campaign_attended")
    #     self.assertEqual(data['status'], "success")


if __name__ == '__main__':
    unittest.main()
