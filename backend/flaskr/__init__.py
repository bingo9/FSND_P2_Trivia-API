import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

'''
PAGINATE QUESTIONS
return defined number of questions per page
'''


def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page-1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after
    completing the TODOs
    '''
    CORS(app, resources={'/': {'origins': '*'}})
    '''
    @TODO: Use the after_request decorator to set Access-Control-Allow
    '''
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, POST, PATCH, DELETE, OPTIONS')
        return response
    '''
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    '''
    @app.route('/categories')
    def get_categories():

        # Query all categories and add type to dictionary
        categories = Category.query.all()
        cat_dict = {}

        for c in categories:
            cat_dict[c.id] = c.type

        # 404 error if no categories found
        if len(cat_dict) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'categories': cat_dict
        })

    '''
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen
    for three pages.
    Clicking on the page numbers should update the questions.
    '''
    @app.route('/questions')
    def get_questions():

        categories = Category.query.all()
        cat_dict = {}

        for c in categories:
            cat_dict[c.id] = c.type

        # Get and paginate all questions
        questions = Question.query.all()
        total_questions = len(questions)
        current_questions = paginate_questions(request, questions)

        if ((len(current_questions) == 0) or (len(cat_dict) == 0)):
            abort(404)

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': total_questions,
            'categories': cat_dict,
            'current_category': None
        })

    '''
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question
    will be removed.
    This removal will persist in the database and when you refresh the page.
    '''
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            # find question by id
            question = Question.query.filter(
                       Question.id == question_id).one_or_none()

            # abort if there isn't a question id matching the query
            if question is None:
                abort(404)

            # delete question
            question.delete()

            return jsonify({
                "success": True,
                "deleted": question_id
            })

        except:
            abort(422)

    '''
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of
    the last page of the questions list in the "List" tab.

    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    '''

    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()

        # set variables
        new_question = body.get('question', None)
        new_answer = body.get('answer', None)
        new_category = body.get('category', None)
        new_difficulty = body.get('difficulty', None)
        search = body.get('searchTerm', None)

        try:

            # if there was a search submitted try to search for the search term
            if search:

                questions = Question.query.filter(Question.question.
                                                  ilike(f'%{search}%')).all()
                current_questions = paginate_questions(request, questions)

                if((questions is None) or (current_questions is None)):
                    abort(404)

                return jsonify({
                    'success': True,
                    'questions': current_questions,
                    'total_questions': len(Question.query.all())
                })

            # if there was no search submitted, create the new question
            else:
                question = Question(question=new_question,
                                    answer=new_answer,
                                    category=new_category,
                                    difficulty=new_difficulty)

                question.insert()

                return jsonify({
                    "success": True,
                    "created": question.id
                })

        except:
            abort(422)

    '''
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    '''
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_by_category(category_id):

        # get questions query based on category
        try:
            questions = Question.query.filter(
                        Question.category == str(category_id)).all()
            total_questions = len(questions)

            return jsonify({
                'success': True,
                'questions': [q.format() for q in questions],
                'total_questions': total_questions,
                'current_category': category_id
            })

        except:
            abort(404)

    '''
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    '''

    @app.route('/quizzes', methods=['POST'])
    def quiz_game():

        try:
            body = request.get_json()

            # set variables
            prev_questions = body.get('previous_questions')
            quiz_category = body.get('quiz_category')

            # abort if the variables are None
            if(prev_questions is None) or (quiz_category is None):
                abort(400)

            # if category 'all' selected then get all questions
            # that weren't previous questions
            if(quiz_category['id'] == 0):
                questions = Question.query.filter(~Question.id.in_
                                                  (prev_questions)).all()

            # get category quqstions that weren't in previous questions
            else:
                questions = Question.query.filter_by(
                                            category=quiz_category['id'])\
                                            .filter(~Question.id.in_
                                                    (prev_questions)).all()

            # choose random question from the valid questions found
            if(len(questions) > 0):
                next_question = questions[random.randrange(0,
                                          len(questions))].format()
            else:
                next_question = None

            return jsonify({
                'success': True,
                'question': next_question
            })

        except:
            abort(500)

    '''
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    '''

    # ERROR - BAD REQUEST (400)
    @app.errorhandler
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    # ERROR - NOT FOUND (404)
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    # ERROR - METHOD NOT ALLOWED (405)
    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405

    # ERROR - UNPROCESSABLE (422)
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    # ERROR - INTERNAL SERVER ERROR (500)
    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internal server error"
        }), 500

    return app
