import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import Movie, Actor, db
from dotenv import load_dotenv

# Unpack envrionment variables
load_dotenv()

CASTING_ASSISTANT = os.environ.get('CASTING_ASSISTANT_JWT')
CASTING_DIRECTOR = os.environ.get('CASTING_DIRECTOR_JWT')
EXECUTIVE_PRODUCER = os.environ.get('EXECUTIVE_PRODUCER_JWT')


class TalentManagementAgencyTestCase(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        self.client = self.app.test_client
        self.database_name = "test_talentagency"
        #self.database_path = "postgresql://localhost:5432/test_talentagency"
        self.database_path = "postgresql://{}/{}".format('localhost:5432', self.database_name)
        self.app = create_app(self.database_path)

    def tearDown(self):
        # Drop all tables after each test
        pass
        # with self.app.app_context():
        #     self.db.drop_all(bind=None)

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
        sample_movie = {
            'title': 'The Incredible Hulk',
            'release_date': 2008
        }

        response = self.client().post(
            '/movies',
            json=sample_movie,
            headers={'Authorization': f'Bearer {CASTING_DIRECTOR}'}
        )
        print(response.data)
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