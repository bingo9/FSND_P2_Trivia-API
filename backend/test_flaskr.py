import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}/{}".format('localhost:5432',
                                                         self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.new_question = {
            'question': 'Is this a test question?',
            'answer': 'This is a test question!',
            'difficulty': 1,
            'category': 1
        }

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful
    operation and for expected errors.
    """
    def test_get_categories(self):
        # get categories
        res = self.client().get('/categories')
        data = json.loads(res.data)

        # test assertions
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])

    def test_404_category_request_out_of_range(self):
        # get category out of range
        res = self.client().get('/categories/5000')
        data = json.loads(res.data)

        # test assertions
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_get_questions(self):
        # get questions
        res = self.client().get('/questions')
        data = json.loads(res.data)

        # test assertions
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])

    def test_404_question_request_out_of_range(self):
        # get question out of range
        res = self.client().get('/questions?page=5000')
        data = json.loads(res.data)

        # test assertions
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_delete_question(self):

        # add new question to test delete
        new_question = Question(question=self.new_question['question'],
                                answer=self.new_question['answer'],
                                category=self.new_question['category'],
                                difficulty=self.new_question['difficulty'])
        new_question.insert()
        prev_num_of_questions = len(Question.query.all())

        # delete question and load data
        res = self.client().delete(f'/questions/{new_question.id}')
        data = json.loads(res.data)

        # Get num of quetsions after delete and query
        # to make sure question deleted
        num_of_questions = len(Question.query.all())
        question = Question.query.filter(Question.id == new_question.id)\
                                 .one_or_none()

        # test assertions
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], new_question.id)
        self.assertEqual(question, None)
        self.assertTrue(prev_num_of_questions-num_of_questions == 1)

    def test_404_if_question_does_not_exist(self):
        # delete question out of range
        res = self.client().delete('/questions/5000')
        data = json.loads(res.data)

        # test assertions
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_create_question(self):
        num_of_questions_before = len(Question.query.all())

        # post new question
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        # test assertions
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(Question.query.all()),
                         num_of_questions_before + 1)

    def test_search_with_results(self):
        # post question search
        res = self.client().post('/questions', json={'searchTerm': 'a'})
        data = json.loads(res.data)

        # test assertions
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']) > 0)
        self.assertTrue(data['total_questions'])

    def test_404_search_not_found(self):
        # post question search that won't be found
        res = self.client().post('/questions', json={'searchTerm': 'asdfkda'})
        data = json.loads(res.data)

        # test assertions
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 0)

    def test_get_questions_by_category(self):
        # get questions by category
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        # test assertions
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])

    def test_404_get_questions_by_category(self):
        # get category that doesn't exist
        res = self.client().get('categories/test/questions')
        data = json.loads(res.data)

        # test assertions
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "resource not found")

    def test_quiz_game(self):
        # play quiz
        res = self.client().post('/quizzes', json={
                                 'previous_questions': [5, 6],
                                 'quiz_category': {'id': 1,
                                                   'type': 'Science'}})
        data = json.loads(res.data)

        # test assertions
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_500_internal_server_error_quiz_game(self):
        # play quiz with no data
        res = self.client().post('/quizzes')
        data = json.loads(res.data)

        # test assertions
        self.assertEqual(res.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'internal server error')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
