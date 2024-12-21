import unittest
import json
import sys
import os
from datetime import datetime

# Adjust the path to import the Flask app and models
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)

from app import create_app, db, bcrypt  # Import the Flask app and extensions
from models.dbSchema import User, Charity  # Import necessary models
from models import Notifications

notifications = Notifications.ErrorProcessor()


class CharityTestCase(unittest.TestCase):
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

        # Create a non-admin user
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

    def test_create_charity_success(self):
        """
        Test creating a charity successfully by an admin user.
        """
        # Log in as admin to obtain the token
        token = self.login('admin.user@example.com', 'AdminPass123')
        self.assertIsNotNone(
            token, "Admin token should not be None after successful login.")

        # Define the payload with a single charity
        payload = [
            {
                'charId': 1,
                'charName': 'Charity One',
                'charAdd': '123 Charity St.',
                'charDesc': 'Description of Charity One.',
                'charCat': 'Health'
            }
        ]

        # Send POST request to create charities
        response = self.client.post(
            '/charity/create',
            data=json.dumps(payload),
            content_type='application/json',
            headers={'x-access-token': token}
        )

        # Assert response status code
        self.assertEqual(response.status_code, 201)

        # Assert response data
        data = json.loads(response.data)
        self.assertIn('charities', data)
        self.assertEqual(data['message'], "Charities created successfully")
        self.assertEqual(len(data['charities']), 1)
        self.assertEqual(data['charities'][0]['charityId'], 1)
        self.assertEqual(data['charities'][0]['charityName'], 'Charity One')

        # Verify that the charity exists in the database
        charity = Charity.query.filter_by(id=1).first()
        self.assertIsNotNone(charity)
        self.assertEqual(charity.name, 'Charity One')

    def test_create_charity_multiple_success(self):
        """
        Test creating multiple charities successfully by an admin user.
        """
        # Log in as admin to obtain the token
        token = self.login('admin.user@example.com', 'AdminPass123')
        self.assertIsNotNone(
            token, "Admin token should not be None after successful login.")

        # Define the payload with multiple charities
        payload = [
            {
                'charId': 2,
                'charName': 'Charity Two',
                'charAdd': '456 Charity Ave.',
                'charDesc': 'Description of Charity Two.',
                'charCat': 'Education'
            },
            {
                'charId': 3,
                'charName': 'Charity Three',
                'charAdd': '789 Charity Blvd.',
                'charDesc': 'Description of Charity Three.',
                'charCat': 'Environment'
            }
        ]

        # Send POST request to create charities
        response = self.client.post(
            '/charity/create',
            data=json.dumps(payload),
            content_type='application/json',
            headers={'x-access-token': token}
        )

        # Assert response status code
        self.assertEqual(response.status_code, 201)

        # Assert response data
        data = json.loads(response.data)
        self.assertIn('charities', data)
        self.assertEqual(data['message'], "Charities created successfully")
        self.assertEqual(len(data['charities']), 2)
        self.assertEqual(data['charities'][0]['charityId'], 2)
        self.assertEqual(data['charities'][0]['charityName'], 'Charity Two')
        self.assertEqual(data['charities'][1]['charityId'], 3)
        self.assertEqual(data['charities'][1]['charityName'], 'Charity Three')

        # Verify that the charities exist in the database
        charity_two = Charity.query.filter_by(id=2).first()
        charity_three = Charity.query.filter_by(id=3).first()
        self.assertIsNotNone(charity_two)
        self.assertEqual(charity_two.name, 'Charity Two')
        self.assertIsNotNone(charity_three)
        self.assertEqual(charity_three.name, 'Charity Three')

    def test_create_charity_invalid_input_not_list(self):
        """
        Test creating charities with invalid input (not a list).
        """
        # Log in as admin to obtain the token
        token = self.login('admin.user@example.com', 'AdminPass123')
        self.assertIsNotNone(
            token, "Admin token should not be None after successful login.")

        # Define the payload as a dictionary instead of a list
        payload = {
            'charId': 4,
            'charName': 'Charity Four',
            'charAdd': '101 Charity Ln.',
            'charDesc': 'Description of Charity Four.',
            'charCat': 'Arts'
        }

        # Send POST request to create charities
        response = self.client.post(
            '/charity/create',
            data=json.dumps(payload),
            content_type='application/json',
            headers={'x-access-token': token}
        )

        # Assert response status code
        self.assertEqual(response.status_code, 400)

        # Assert response data
        data = json.loads(response.data)
        self.assertEqual(data['message'], notifications.process_error("charity_invalid_input")['message'])
        self.assertEqual(data['status'], "error")

        # Verify that the charity does not exist in the database
        charity = Charity.query.filter_by(id=4).first()
        self.assertIsNone(charity)
        

    def test_create_charity_missing_fields(self):
        """
        Test creating a charity with missing required fields.
        """
        # Log in as admin to obtain the token
        token = self.login('admin.user@example.com', 'AdminPass123')
        self.assertIsNotNone(
            token, "Admin token should not be None after successful login.")

        # Define the payload with missing 'charAdd' field
        payload = [
            {
                'charId': 5,
                'charName': 'Charity Five',
                # 'charAdd' is missing
                'charDesc': 'Description of Charity Five.',
                'charCat': 'Health'
            }
        ]

        # Send POST request to create charities
        response = self.client.post(
            '/charity/create',
            data=json.dumps(payload),
            content_type='application/json',
            headers={'x-access-token': token}
        )

        # Assert response status code
        self.assertEqual(response.status_code, 400)

        # Assert response data
        data = json.loads(response.data)
        self.assertEqual(data['message'], notifications.process_error("charity_missing_fields")['message'])
        self.assertEqual(data['status'], "error")

        # Verify that the charity does not exist in the database
        charity = Charity.query.filter_by(id=5).first()
        self.assertIsNone(charity)

    def test_create_charity_duplicate_name(self):
        """
        Test creating a charity with a name that already exists.
        """
        # Log in as admin to obtain the token
        token = self.login('admin.user@example.com', 'AdminPass123')
        self.assertIsNotNone(
            token, "Admin token should not be None after successful login.")

        # First, create a charity successfully
        payload = [
            {
                'charId': 6,
                'charName': 'Charity Six',
                'charAdd': '202 Charity Rd.',
                'charDesc': 'Description of Charity Six.',
                'charCat': 'Community'
            }
        ]
        response = self.client.post(
            '/charity/create',
            data=json.dumps(payload),
            content_type='application/json',
            headers={'x-access-token': token}
        )
        self.assertEqual(response.status_code, 201)

        # Attempt to create another charity with the same name
        payload_duplicate = [
            {
                'charId': 7,
                'charName': 'Charity Six',  # Duplicate name
                'charAdd': '303 Charity Blvd.',
                'charDesc': 'Another description.',
                'charCat': 'Health'
            }
        ]
        response = self.client.post(
            '/charity/create',
            data=json.dumps(payload_duplicate),
            content_type='application/json',
            headers={'x-access-token': token}
        )
        self.assertEqual(response.status_code, 400)

        # Assert response data
        data = json.loads(response.data)
        self.assertEqual(data['message'], notifications.process_error("charity_exists", name='Charity Six')['message'])
        self.assertEqual(data['status'], notifications.process_error("charity_exists", name='Charity Six')['status'])

        # Verify that the second charity was not created
        charity = Charity.query.filter_by(id=7).first()
        self.assertIsNone(charity)

    def test_create_charity_non_admin_forbidden(self):
        """
        Test creating a charity as a non-admin user (should be forbidden).
        """
        # Log in as a regular user to obtain the token
        token = self.login('regular.user@example.com', 'UserPass123')
        self.assertIsNotNone(
            token, "User token should not be None after successful login.")

        # Define the payload
        payload = [
            {
                'charId': 8,
                'charName': 'Charity Eight',
                'charAdd': '404 Charity St.',
                'charDesc': 'Description of Charity Eight.',
                'charCat': 'Education'
            }
        ]

        # Attempt to create a charity as a non-admin user
        response = self.client.post(
            '/charity/create',
            data=json.dumps(payload),
            content_type='application/json',
            headers={'x-access-token': token}
        )

        # Assert response status code
        self.assertEqual(response.status_code, 403)

        # Assert response data
        data = json.loads(response.data)
        # As per ErrorProcessor for admin_required
        self.assertEqual(data['message'], "Access denied!")
        self.assertEqual(data['notification'], "You do not have sufficient privileges.")

        # Verify that the charity was not created
        charity = Charity.query.filter_by(id=8).first()
        self.assertIsNone(charity)

    def test_create_charity_empty_list(self):
        """
        Test creating charities with an empty list.
        """
        # Log in as admin to obtain the token
        token = self.login('admin.user@example.com', 'AdminPass123')
        self.assertIsNotNone(
            token, "Admin token should not be None after successful login.")

        # Define the payload as an empty list
        payload = []

        # Send POST request to create charities
        response = self.client.post(
            '/charity/create',
            data=json.dumps(payload),
            content_type='application/json',
            headers={'x-access-token': token}
        )

        # Assert response status code
        self.assertEqual(response.status_code, 400)

        # Assert response data
        data = json.loads(response.data)
        self.assertEqual(data['message'], notifications.process_error("charity_invalid_input")['message'])
        self.assertEqual(data['status'], "error")

    def test_create_charity_duplicate_charId(self):
        """
        Test creating a charity with a duplicate charId.
        """
        # Log in as admin to obtain the token
        token = self.login('admin.user@example.com', 'AdminPass123')
        self.assertIsNotNone(
            token, "Admin token should not be None after successful login.")

        # First, create a charity successfully
        payload = [
            {
                'charId': 9,
                'charName': 'Charity Nine',
                'charAdd': '505 Charity Ave.',
                'charDesc': 'Description of Charity Nine.',
                'charCat': 'Health'
            }
        ]
        response = self.client.post(
            '/charity/create',
            data=json.dumps(payload),
            content_type='application/json',
            headers={'x-access-token': token}
        )
        self.assertEqual(response.status_code, 201)

        # Attempt to create another charity with the same charId but different name
        payload_duplicate_id = [
            {
                'charId': 9,  # Duplicate ID
                'charName': 'Charity Ten',
                'charAdd': '606 Charity Blvd.',
                'charDesc': 'Description of Charity Ten.',
                'charCat': 'Environment'
            }
        ]
        response = self.client.post(
            '/charity/create',
            data=json.dumps(payload_duplicate_id),
            content_type='application/json',
            headers={'x-access-token': token}
        )
        self.assertEqual(response.status_code, 400)

        # Assert response data
        data = json.loads(response.data)
        self.assertEqual(data['message'], notifications.process_error("charity_id_exists", id=9)['message'])
        self.assertEqual(data['status'], "error")

        # Verify that the second charity was not created
        charity = Charity.query.filter_by(id=9).first()
        self.assertIsNotNone(charity)
        # Original charity remains
        self.assertEqual(charity.name, 'Charity Nine')



if __name__ == '__main__':
    unittest.main()
