# server/tests/test_campaign_delete.py

import unittest
import json
import sys
import os
from datetime import datetime

# Adjust the path to import the Flask app and models
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)

from app import create_app, db, bcrypt  # Import the Flask app and extensions
from models.dbSchema import User, Charity, Campaign  # Import necessary models
from models import Notifications

notifications = Notifications.ErrorProcessor()

class CampaignDeleteTestCase(unittest.TestCase):
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

        # Create an admin user
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

        # Create a regular user (non-admin)
        hashed_password_user = bcrypt.generate_password_hash('UserPass123').decode('utf-8')
        self.user = User(
            id='user-id-123',
            fname='Regular',
            lname='User',
            email='regular.user@example.com',
            password=hashed_password_user,
            is_admin=False  # Regular user
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

        # Create a campaign to be deleted in tests
        self.campaign = Campaign(
            id=1,
            title='Campaign One',
            reward=100,
            description='Description of Campaign One.',
            charity_id=self.charity.id,
            date= datetime.now().isoformat(),
            capacity=50
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

    def login_admin(self):
        """
        Helper method to log in as admin and obtain the token.
        """
        response = self.client.post(
            '/auth/login',
            data=json.dumps({'email': 'admin.user@example.com', 'userPass': 'AdminPass123'}),
            content_type='application/json'
        )
        data = json.loads(response.data)
        return data.get('token')

    def login_user(self):
        """
        Helper method to log in as regular user and obtain the token.
        """
        response = self.client.post(
            '/auth/login',
            data=json.dumps({'email': 'regular.user@example.com', 'userPass': 'UserPass123'}),
            content_type='application/json'
        )
        data = json.loads(response.data)
        return data.get('token')

    def test_delete_campaign_success(self):
        """
        Test successful deletion of a campaign by an admin user.
        """
        token = self.login_admin()
        self.assertIsNotNone(token, "Admin token should not be None after successful login.")

        # Ensure the campaign exists before deletion
        campaign = Campaign.query.filter_by(id=1).first()
        self.assertIsNotNone(campaign, "Campaign should exist before deletion.")

        # Send DELETE request to delete the campaign
        payload = {'campaignId': 1}
        response = self.client.delete(
            '/Campaign/delete',
            data=json.dumps(payload),
            content_type='application/json',
            headers={'x-access-token': token}
        )

        # Assert response status code
        self.assertEqual(response.status_code, 200)

        # Assert response data
        data = json.loads(response.data)
        self.assertEqual(data['message'], notifications.process_error("admin_campaign_delete")['message'])
        self.assertEqual(data['status'], "success")

        # Verify that the campaign no longer exists in the database
        deleted_campaign = Campaign.query.filter_by(id=1).first()
        self.assertIsNone(deleted_campaign, "Campaign should be deleted from the database.")

    def test_delete_campaign_no_token_unauthorized(self):
        """
        Test deleting a campaign without providing a token (should be unauthorized).
        """
        # Define the payload
        payload = {'campaignId': 1}

        # Send DELETE request without a token
        response = self.client.delete(
            '/Campaign/delete',
            data=json.dumps(payload),
            content_type='application/json'
            # No headers
        )

        # Assert response status code
        self.assertEqual(response.status_code, 403)

        # Assert response data
        data = json.loads(response.data)
        self.assertEqual(data['message'], "Session is missing or invalid!")

        # Verify that the campaign still exists in the database
        campaign = Campaign.query.filter_by(id=1).first()
        self.assertIsNotNone(campaign, "Campaign should still exist in the database.")

    def test_delete_campaign_non_admin_forbidden(self):
        """
        Test deleting a campaign as a non-admin user (should be forbidden).
        """
        token = self.login_user()
        self.assertIsNotNone(token, "User token should not be None after successful login.")

        # Ensure the campaign exists before deletion
        campaign = Campaign.query.filter_by(id=1).first()
        self.assertIsNotNone(campaign, "Campaign should exist before deletion.")

        # Send DELETE request to delete the campaign
        payload = {'campaignId': 1}
        response = self.client.delete(
            '/Campaign/delete',
            data=json.dumps(payload),
            content_type='application/json',
            headers={'x-access-token': token}
        )

        # Assert response status code
        self.assertEqual(response.status_code, 403)

        # Assert response data
        data = json.loads(response.data)
        self.assertEqual(data['message'], "Access denied!")

        # Verify that the campaign still exists in the database
        campaign = Campaign.query.filter_by(id=1).first()
        self.assertIsNotNone(campaign, "Campaign should still exist in the database.")

    def test_delete_campaign_non_existent_campaign_not_found(self):
        """
        Test deleting a non-existent campaign (should return 404 Not Found).
        """
        token = self.login_admin()
        self.assertIsNotNone(token, "Admin token should not be None after successful login.")

        # Define a non-existent campaignId
        non_existent_campaign_id = 999

        # Send DELETE request
        payload = {'campaignId': non_existent_campaign_id}
        response = self.client.delete(
            '/Campaign/delete',
            data=json.dumps(payload),
            content_type='application/json',
            headers={'x-access-token': token}
        )

        # Assert response status code
        self.assertEqual(response.status_code, 404)

        # Assert response data
        data = json.loads(response.data)
        self.assertEqual(data['message'], notifications.process_error("campaign_not_attended")['message'])
        self.assertEqual(data['status'], "error")

    def test_delete_campaign_missing_campaign_id_bad_request(self):
        """
        Test deleting a campaign without providing 'campaignId' (should return 400 Bad Request).
        """
        token = self.login_admin()
        self.assertIsNotNone(token, "Admin token should not be None after successful login.")

        # Send DELETE request without 'campaignId'
        payload = {}
        response = self.client.delete(
            '/Campaign/delete',
            data=json.dumps(payload),
            content_type='application/json',
            headers={'x-access-token': token}
        )

        # Assert response status code
        self.assertEqual(response.status_code, 400)

        # Assert response data
        data = json.loads(response.data)
        self.assertEqual(data['message'], notifications.process_error("campaign_unregister")['message'])

        # Verify that the campaign still exists in the database
        campaign = Campaign.query.filter_by(id=1).first()
        self.assertIsNotNone(campaign, "Campaign should still exist in the database.")

    def test_delete_campaign_invalid_campaign_id_type_bad_request(self):
        """
        Test deleting a campaign with 'campaignId' as a string instead of integer (should return 400 Bad Request).
        """
        token = self.login_admin()
        self.assertIsNotNone(token, "Admin token should not be None after successful login.")

        # Define the payload with 'campaignId' as a string
        payload = {'campaignId': 'one'}

        # Send DELETE request
        response = self.client.delete(
            '/Campaign/delete',
            data=json.dumps(payload),
            content_type='application/json',
            headers={'x-access-token': token}
        )

        # Assert response status code
        self.assertEqual(response.status_code, 400)

        # Assert response data
        data = json.loads(response.data)
        self.assertEqual(data['message'], notifications.process_error("campaign_unregister")['message'])

        # Verify that the campaign still exists in the database
        campaign = Campaign.query.filter_by(id='one').first()
        self.assertIsNone(campaign, "Campaign with invalid ID should not exist in the database.")



if __name__ == '__main__':
    unittest.main()
