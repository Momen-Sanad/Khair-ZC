# server/tests/test_campaign_create.py

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

class CampaignCreateTestCase(unittest.TestCase):
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

    def test_create_single_campaign_success(self):
        """
        Test successful creation of a single campaign by an admin user.
        """
        token = self.login_admin()
        self.assertIsNotNone(token, "Admin token should not be None after successful login.")

        payload = [
            {
                'userId': self.admin.id,
                'campaignId': 1,
                'campaignName': 'Campaign One',
                'campaignRe': 100,
                'campaignDesc': 'Description of Campaign One.',
                'campaignDate': datetime.now().isoformat(),
                'campaignCap': 50,
                'charId': self.charity.id
            }
        ]

        response = self.client.post(
            '/Campaign/create',
            data=json.dumps(payload),
            content_type='application/json',
            headers={'x-access-token': token}
        )

        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['message'], notifications.process_error("admin_campaign_create")['message'])
        self.assertEqual(data['status'], "success")

        # Verify that the campaign exists in the database
        campaign = Campaign.query.filter_by(id=1).first()
        self.assertIsNotNone(campaign)
        self.assertEqual(campaign.title, 'Campaign One')

    def test_create_multiple_campaigns_success(self):
        """
        Test successful creation of multiple campaigns by an admin user.
        """
        token = self.login_admin()
        self.assertIsNotNone(token, "Admin token should not be None after successful login.")

        payload = [
            {
                'userId': self.admin.id,
                'campaignId': 2,
                'campaignName': 'Campaign Two',
                'campaignRe': 200,
                'campaignDesc': 'Description of Campaign Two.',
                'campaignDate': datetime.now().isoformat(),
                'campaignCap': 100,
                'charId': self.charity.id
            },
            {
                'userId': self.admin.id,
                'campaignId': 3,
                'campaignName': 'Campaign Three',
                'campaignRe': 150,
                'campaignDesc': 'Description of Campaign Three.',
                'campaignDate': datetime.now().isoformat(),
                'campaignCap': 75,
                'charId': self.charity.id
            }
        ]

        response = self.client.post(
            '/Campaign/create',
            data=json.dumps(payload),
            content_type='application/json',
            headers={'x-access-token': token}
        )

        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['message'], notifications.process_error("admin_campaign_create")['message'])
        self.assertEqual(data['status'], "success")

        # Verify that both campaigns exist in the database
        campaign_two = Campaign.query.filter_by(id=2).first()
        campaign_three = Campaign.query.filter_by(id=3).first()
        self.assertIsNotNone(campaign_two)
        self.assertEqual(campaign_two.title, 'Campaign Two')
        self.assertIsNotNone(campaign_three)
        self.assertEqual(campaign_three.title, 'Campaign Three')

    def test_create_campaign_invalid_payload_not_list(self):
        """
        Test creating a campaign with an invalid payload (not a list).
        """
        token = self.login_admin()
        self.assertIsNotNone(token, "Admin token should not be None after successful login.")

        # Define the payload as a dictionary instead of a list
        payload = {
            'userId': self.admin.id,
            'campaignId': 4,
            'campaignName': 'Campaign Four',
            'campaignRe': 250,
            'campaignDesc': 'Description of Campaign Four.',
            'campaignDate': datetime.now().isoformat(),
            'campaignCap': 80,
            'charId': self.charity.id
        }

        response = self.client.post(
            '/Campaign/create',
            data=json.dumps(payload),
            content_type='application/json',
            headers={'x-access-token': token}
        )

        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['message'], notifications.process_error("search_invalid")['message'])
        self.assertEqual(data['status'], "error")

        # Verify that the campaign was not created
        campaign = Campaign.query.filter_by(id=4).first()
        self.assertIsNone(campaign)

    def test_create_campaign_missing_required_fields(self):
        """
        Test creating a campaign with missing required fields.
        """
        token = self.login_admin()
        self.assertIsNotNone(token, "Admin token should not be None after successful login.")

        # Missing 'campaignName'
        payload = [
            {
                'userId': self.admin.id,
                'campaignId': 5,
                # 'campaignName': 'Campaign Five',  # Missing
                'campaignRe': 300,
                'campaignDesc': 'Description of Campaign Five.',
                'campaignDate': '2025-04-05T16:00:00Z',
                'campaignCap': 60,
                'charId': self.charity.id
            }
        ]

        response = self.client.post(
            '/Campaign/create',
            data=json.dumps(payload),
            content_type='application/json',
            headers={'x-access-token': token}
        )

        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['message'], notifications.process_error("admin_campaign_create")['message'])

        # Verify that the campaign was not created
        campaign = Campaign.query.filter_by(id=5).first()
        self.assertIsNone(campaign)

    def test_create_campaign_duplicate_campaign_name(self):
        """
        Test creating a campaign with a name that already exists.
        """
        token = self.login_admin()
        self.assertIsNotNone(token, "Admin token should not be None after successful login.")

        # First, create a campaign successfully
        payload = [
            {
                'userId': self.admin.id,
                'campaignId': 6,
                'campaignName': 'Campaign Six',
                'campaignRe': 350,
                'campaignDesc': 'Description of Campaign Six.',
                'campaignDate': datetime.now().isoformat(),
                'campaignCap': 90,
                'charId': self.charity.id
            }
        ]
        response = self.client.post(
            '/Campaign/create',
            data=json.dumps(payload),
            content_type='application/json',
            headers={'x-access-token': token}
        )
        self.assertEqual(response.status_code, 201)

        # Attempt to create another campaign with the same name
        duplicate_payload = [
            {
                'userId': self.admin.id,
                'campaignId': 7,
                'campaignName': 'Campaign Six',  # Duplicate name
                'campaignRe': 400,
                'campaignDesc': 'Another description.',
                'campaignDate': datetime.now().isoformat(),
                'campaignCap': 100,
                'charId': self.charity.id
            }
        ]
        response = self.client.post(
            '/Campaign/create',
            data=json.dumps(duplicate_payload),
            content_type='application/json',
            headers={'x-access-token': token}
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['message'], notifications.process_error("campaign_follow")['message'])

        # Verify that the duplicate campaign was not created
        campaign = Campaign.query.filter_by(id=7).first()
        self.assertIsNone(campaign)

    def test_create_campaign_duplicate_campaign_id(self):
        """
        Test creating a campaign with a duplicate campaignId.
        """
        token = self.login_admin()
        self.assertIsNotNone(token, "Admin token should not be None after successful login.")

        # First, create a campaign successfully
        payload = [
            {
                'userId': self.admin.id,
                'campaignId': 8,
                'campaignName': 'Campaign Eight',
                'campaignRe': 450,
                'campaignDesc': 'Description of Campaign Eight.',
                'campaignDate': datetime.now().isoformat(),
                'campaignCap': 70,
                'charId': self.charity.id
            }
        ]
        response = self.client.post(
            '/Campaign/create',
            data=json.dumps(payload),
            content_type='application/json',
            headers={'x-access-token': token}
        )
        self.assertEqual(response.status_code, 201)

        # Attempt to create another campaign with the same campaignId
        duplicate_id_payload = [
            {
                'userId': self.admin.id,
                'campaignId': 8,  # Duplicate campaignId
                'campaignName': 'Campaign Nine',
                'campaignRe': 500,
                'campaignDesc': 'Description of Campaign Nine.',
                'campaignDate': datetime.now().isoformat(),
                'campaignCap': 80,
                'charId': self.charity.id
            }
        ]
        response = self.client.post(
            '/Campaign/create',
            data=json.dumps(duplicate_id_payload),
            content_type='application/json',
            headers={'x-access-token': token}
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['message'], notifications.process_error("campaign_follow")['message'])

        # Verify that the duplicate campaign was not created
        campaign = Campaign.query.filter_by(id=8).first()
        self.assertIsNotNone(campaign)
        self.assertEqual(campaign.title, 'Campaign Eight')



if __name__ == '__main__':
    unittest.main()
