import os
import unittest
import json
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from flaskr import create_app
from models import setup_db, Question, Category
import pprint

QUESTIONS_PER_PAGE = 10
class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_paginate_questions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)
        #print(data)
        self.assertEqual(res.status_code, 200)

    def test_get_categories(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'OK')
        self.assertEqual(data['code'], '200')

    def test_error_get_categories(self):
        res = self.client().get("/categories/99")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_get_questions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'OK')
        self.assertEqual(data['code'], '200')
        self.assertEqual(data['total_questions'], QUESTIONS_PER_PAGE)

    def test_error_get_questions(self):
        res = self.client().get("/questions?page=10")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')
        self.assertEqual(data['success'], False)


    def test_delete_question(self):
        res = self.client().delete('/questions/2')
        data = json.loads(res.data)
        #pprint.pprint(data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'OK')
        self.assertEqual(data['code'], '200')
        self.assertEqual(data['total_questions'], QUESTIONS_PER_PAGE)

    def test_error_delete_question(self):
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], 'unprocessable')
        self.assertEqual(data['success'], False)

    def test_create_question(self):
        new_question = {
            'question': 'What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?',
            'answer': 'Edward Scissorhands',
            'category': '3',
            'difficulty': '5'
        }
        res = self.client().post('/questions', json=new_question)
        data = json.loads(res.data)
        #pprint.pprint(data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'OK')
        self.assertEqual(data['code'], '200')
        self.assertEqual(data['total_questions'], QUESTIONS_PER_PAGE)

    def test_error_create_question(self):
        new_question = {
            'question': 'What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?',
            'answer': 'Edward Scissorhands',
            'category': '3',
            'difficulty': 'hello'
        }
        res = self.client().post('/questions', json=new_question)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_search_questions(self):
        search_term = {
            'searchTerm': 'Taj'
        }
        res = self.client().post('/questions/search', json=search_term)
        data = json.loads(res.data)
        #pprint.pprint(data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'OK')
        self.assertEqual(data['code'], '200')
        self.assertEqual(data['total_questions'], 1)

    def test_error_search_questions(self):
        search_term = {
            'searchTerm': 'Dante'
        }
        res = self.client().post('/questions/search', json=search_term)
        data = json.loads(res.data)
        #pprint.pprint(data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_get_questions_by_category(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)
        #pprint.pprint(data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'OK')
        self.assertEqual(data['code'], '200')
        self.assertEqual(data['total_questions'], 3)
        #self.assertEqual(data['current_category'], 'Science')

    def test_error_get_questions_by_category(self):
        res = self.client().get('/categories/1000/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_get_quiz_question(self):
        data = {
            'previous_questions': [1, 2, 3, 4, 5],
            'quiz_category': {'type': 'Science', 'id': '1'}
        }
        res = self.client().post('/quizzes', json=data)
        data = json.loads(res.data)
        pprint.pprint(data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'OK')
        self.assertEqual(data['code'], '200')
        self.assertIsNotNone(data['question'])

    def test_error_get_quiz_question(self):
        data = {
            'previous_questions': [
                1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 
                11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 
                21, 22, 23, 24, 25, 26, 27, 28, 29, 30
            ],
            'quiz_category': {'type': 'AI', 'id': '99'}
        }
        res = self.client().post('/quizzes', json=data)
        data = json.loads(res.data)
        #pprint.pprint(data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()