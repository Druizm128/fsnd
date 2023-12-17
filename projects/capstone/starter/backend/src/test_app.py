import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import Movie, Actor, db, setup_db
from dotenv import load_dotenv

# Unpack envrionment variables
load_dotenv()

CASTING_ASSISTANT = os.environ.get('CASTING_ASSISTANT_JWT')
CASTING_DIRECTOR = os.environ.get('CASTING_DIRECTOR_JWT')
EXECUTIVE_PRODUCER = os.environ.get('EXECUTIVE_PRODUCER_JWT')


class TalentManagementAgencyTestCase(unittest.TestCase):

    # def setUp(self):
    #     """Define test variables and initialize app."""
    #     self.client = self.app.test_client
    #     self.database_name = "test_talentagency"
    #     #self.database_path = "postgresql://localhost:5432/test_talentagency"
    #     self.database_path = "postgresql://{}/{}".format('localhost:5432', self.database_name)
    #     self.app = create_app(self.database_path)

    def setUp(self):
        """Define test variables and initialize app."""
        self.database_name = "test_talentagency"
        #self.database_path = "postgresql://localhost:5432/{}".format(self.database_name)
        self.database_path = "postgresql://localhost:5432/test_talentagency"
        self.app = create_app(database_path=self.database_path)
        self.client = self.app.test_client
        with self.app.app_context():
            db.create_all()

            # Create a sample movie
            movie = Movie(
                title='Terminator',
                release_date=2000
            )

            # Create a sample actor
            actor = Actor(
                name='Arnold Shwarzeneger',
                age=45,
                gender='Male'
            )
            db.session.add(movie)
            db.session.add(actor)
            db.session.commit()

    def tearDown(self):
        # Drop all tables after each test
        with self.app.app_context():
            db.drop_all()
        # pass

    def test_create_movie(self):
        sample_movie = {
            'title': 'The Incredible Hulk',
            'release_date': 2008
        }
        response = self.client().post(
            '/movies',
            json=sample_movie,
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        print(response.data)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(True, True)

    def test_create_actor(self):
        sample_actor = {
            'name': 'Bruce Banner',
            'age': 45,
            'gender': "Male"
        }
        res = self.client().post(
            '/actors',
            json=sample_actor,
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_movies(self):
        res = self.client().get(
            '/movies',
            headers={
                'Authorization': 'Bearer ' + EXECUTIVE_PRODUCER})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_actors(self):
        res = self.client().get(
            '/actors',
            headers={
                'Authorization': 'Bearer ' + EXECUTIVE_PRODUCER})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_update_actor(self):
        update_actor = {
            'name': 'Arnold Shwarzeneger (One and Only)',
            'age': '50',
            'gender': 'Male'
        }
        res = self.client().patch(
            '/actors/1',
            json=update_actor,
            headers={
                'Authorization': 'Bearer ' + EXECUTIVE_PRODUCER})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_update_movie(self):
        update_movie = {
            'title': 'Terminator Genesis',
            'release_date': '2010'
        }
        res = self.client().patch(
            '/movies/1',
            json=update_movie,
            headers={
                'Authorization': 'Bearer ' + EXECUTIVE_PRODUCER})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_actor(self):
        res = self.client().delete(
            '/actors/1',
            headers={
                'Authorization': 'Bearer ' + EXECUTIVE_PRODUCER}
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_movie(self):
        res = self.client().delete(
            '/movies/1',
            headers={
                'Authorization': 'Bearer ' + EXECUTIVE_PRODUCER}
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()