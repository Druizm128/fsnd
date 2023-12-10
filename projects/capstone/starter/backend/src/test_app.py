import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Movie, Actor
from dotenv import load_dotenv

# Unpack envrionment variables
load_dotenv()

CASTING_ASSISTANT = os.environ.get('CASTING_ASSISTANT_JWT')
CASTING_DIRECTOR = os.environ.get('CASTING_DIRECTOR_JWT')
EXECUTIVE_PRODUCER = os.environ.get('EXECUTIVE_PRODUCER_JWT')

class TalentManagementAgencyTestCase(unittest.TestCase):
    def setUp(self):
        # Define test variables and initialize app.
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "test_talentagency"
        self.database_path = "postgresql://{}:{}@{}:{}/{}".format(
            'postgres', 'Psqlpass!', 'localhost', '5432', self.database_name)
        setup_db(self.app, self.database_path)

        # Binds the app to the current context
        #with self.app.app_context():
            #self.db = SQLAlchemy()
            #self.db.init_app(self.app)
            # create all tables
            #self.db.create_all(bind=None)

        # Sample movie data for testing
        self.sample_movie = {
            'title': 'Test Movie',
            'release_date': '2023-01-01'
        }

    def tearDown(self):
        # Drop all tables after each test
        with self.app.app_context():
            self.db.drop_all(bind=None)

    # def test_get_actors(self):
    #     res = {}
    #     data = json.loads(res.data)
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)

    # def test_get_movies(self):
    #     res = {}
    #     data = json.loads(res.data)
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)

    # def test_delete_actor(self):
    #     res = {}
    #     data = json.loads(res.data)
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)

    # def test_delete_movie(self):
    #     res = {}
    #     data = json.loads(res.data)
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)

    # def test_create_actor(self):
    #     res = {}
    #     data = json.loads(res.data)
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    
    def test_create_movie(self):
        response = self.client().post(
            '/movies',
            json=self.sample_movie,
            headers={'Authorization': f'Bearer {CASTING_DIRECTOR}'}
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        #self.assertIsNotNone(data['movie'])
        # Optional: Assert specific details of the created movie
        #self.assertEqual(data['movie']['title'], self.sample_movie['title'])

    # def test_update_actor(self):
    #     res = {}
    #     data = json.loads(res.data)
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)

    # def test_update_movie(self):
    #     res = {}
    #     data = json.loads(res.data)
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()