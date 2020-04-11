# Full Stack API Project

This is a trivia game for users to have friendly competition with friends, family and colleagues to see who is the most knowledgeable.  You can also you it to hone your skills, or create add new questions to test others.  The goal of this project was to create a functional API (complete with test code) to implement the following functions:

1) Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer. 
2) Delete questions.
3) Add questions and require that they include question and answer text.
4) Search for questions based on a text query string.
5) Play the quiz game, randomizing either all questions or within a specific category. 

## Getting Started

### Installing Dependencies

This codebase is written in Python.  Devlopers using this codebase should already have Python3 and pip installed on their machine.

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

Though not mandatory for this application to function, it is recommended that developers work within a virtual environment. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### Frontend Dependencies

This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the `frontend` directory of this repository. After cloning, open your terminal and run:

```bash
npm install
```

>_tip_: **npm i** is shorthand for **npm install**

#### Backend Dependencies

Once you have your virtual environment setup and running (optional), install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

The backend database used for testing and developing this app was `PostgreSQL`.  The code is currently setup to function with Postgres.

##### Key Dependencies for the Backend

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Running Your Frontend in Dev Mode

The frontend app was built using create-react-app. In order to run the app in development mode use ```npm start```. You can change the script in the ```package.json``` file. 

Open [http://localhost:3000](http://localhost:3000) to view it in the browser. The page will reload if you make edits.<br>

```bash
npm start
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application.

## Testing

To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

## API Reference

### Base URL and Authentication

- Base URL: The application currently is setup to be locally hosted.  The backend host address is http://127.0.0.1:5000/
- Authentication: The application does not require authentication or API Keys currently.

### Error Handling

Errors are returned in JSON format:
```
{
    'success': False,
    'error': 400,
    'message': 'bad request'
}
```

The API is setup to return the following `http` errors:

- 400 - Bad Request
- 404 - Resource Not Found
- 405 - Method Not Allowed
- 422 - Unprocessable
- 500 - Internal Server Error

### Endpoints

#### GET /categories





#### GET /questions

Gets paginated questions.

`$ curl http://127.0.0.1:5000/questions`

- Returns:

    * A list of questions in JSON format

    * Results are paginated in groups of 10 (can adjust in `__init__.py`)

    * A list of categories.
    
    * Total number of questions.

##### Sample Response:

```JSON
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": null, 
  "questions": [
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
    {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }, 
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }, 
    {
      "answer": "Brazil", 
      "category": 6, 
      "difficulty": 3, 
      "id": 10, 
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }, 
    {
      "answer": "Uruguay", 
      "category": 6, 
      "difficulty": 4, 
      "id": 11, 
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }, 
    {
      "answer": "George Washington Carver", 
      "category": 4, 
      "difficulty": 2, 
      "id": 12, 
      "question": "Who invented Peanut Butter?"
    }, 
    {
      "answer": "Lake Victoria", 
      "category": 3, 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }, 
    {
      "answer": "The Palace of Versailles", 
      "category": 3, 
      "difficulty": 3, 
      "id": 14, 
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ], 
  "success": true, 
  "total_questions": 22
}
```

#### DELETE /questions/<int:question_id>
#### POST /questions
#### GET /categories/<int:category_id>/questions
#### POST /quizzes

- General:

    * Allows users to play trivia game.

    * Requests category and previous question parameters using JSON.

    * Response object is returned with random question that wasn't in the previous questions.

- Example: `curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d
'{"previous_questions": [1, 2], "quiz_category": {"type": "Science", "id": "1"}}'

## Authors
Github user bingo9 was the author of the API(`__init__.py`), the API test code (`test_flaskr.py`), and the README you are currently reading.
All the other project files, including the data models, frontend, and the starter code templates were created by [Udacity](www.udacity.com) as
part of the [Full Stack Developer Nanodegree](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd0044) program.