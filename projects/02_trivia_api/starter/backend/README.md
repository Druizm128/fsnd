# Backend - Full Stack Trivia API 

### Installing Dependencies for the Backend

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)


2. **Virtual Enviornment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


3. **PIP Dependencies** - Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:
```bash
pip install -r requirements.txt
```
This will install all of the required packages we selected within the `requirements.txt` file.


4. **Key Dependencies**
 - [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

 - [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

 - [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

### Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

### Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## ToDo Tasks
These are the files you'd want to edit in the backend:

1. *./backend/flaskr/`__init__.py`*
2. *./backend/test_flaskr.py*


One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 


2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 


3. Create an endpoint to handle GET requests for all available categories. 


4. Create an endpoint to DELETE question using a question ID. 


5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 


6. Create a POST endpoint to get questions based on category. 


7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 


8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 


9. Create error handlers for all expected errors including 400, 404, 422 and 500. 



## API Documentation


`GET '/categories'`

* Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category

* **Request Arguments:** None

* **Returns:** An object with a single key, categories, that contains an object of id: category_string key: value pairs.

    ```json
    {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
    }
    ```

`GET '/questions'`

TODO: Refine current_category

* Fetches a dictionary that includes all the questions and categories.  Results are paginated.

* **Request Arguments:**
    - `page` (int)

* **Returns:** A list of categories, a list of questions, the total number of questions.

    ```json
    {
        "categories": [
            {
                "id": 1,
                "type": "Science"
            },
            {
                "id": 2,
                "type": "Art"
            },
            {
                "id": 3,
                "type": "Geography"
            },
            {
                "id": 4,
                "type": "History"
            },
            {
                "id": 5,
                "type": "Entertainment"
            },
            {
                "id": 6,
                "type": "Sports"
            }
        ],
        "code": "200",
        "message": "OK",
        "questions": [
            {
                "answer": "Apollo 13",
                "category": 5,
                "difficulty": 4,
                "id": 2,
                "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
            },
            {
                "answer": "Maya Angelou",
                "category": 4,
                "difficulty": 2,
                "id": 5,
                "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
            },

            ...

            {
                "answer": "Agra",
                "category": 3,
                "difficulty": 2,
                "id": 15,
                "question": "The Taj Mahal is located in which Indian city?"
            }
        ],
        "success": true,
        "total_questions": 10
    }
    ```

`DELETE '/questions/<int:question_id>'`

* Deletes a question using the question ID. 
  
* **Request Arguments:** 
  - `question_id`(int)
  - `page` (int)

* **Returns:** A list of categories, a list of questions, the total number of questions.


    ```json
    {
        'code': '200',
        'deleted': 2,
        'message': 'OK',
        'questions': [{'answer': 'Muhammad Ali',
                    'category': 4,
                    'difficulty': 1,
                    'id': 9,
                    'question': "What boxer's original name is Cassius Clay?"},
                    {'answer': 'Brazil',
                    'category': 6,
                    'difficulty': 3,
                    'id': 10,
                    'question': 'Which is the only team to play in every soccer '
                                'World Cup tournament?'},

                        ...

                    {'answer': 'One',
                    'category': 2,
                    'difficulty': 4,
                    'id': 18,
                    'question': 'How many paintings did Van Gogh sell in his '
                                'lifetime?'}],
        'success': True,
        'total_questions': 10
    }
    ```
  


`POST '/questions'`

* Create an endpoint to POST a new question.

* **Request Arguments:** Requires the question and answer text, 
category, and difficulty score.

    ```json
    {
    'question': 'What is the heaviest organ in the human body?'
    'answer': 'The Liver'
    'category': 1
    'difficulty': 4
    }
    ```
* **Returns:** A list of categories, a list of questions, the total number of 
questions.

    ```json
    {
    'code': '200',
    'created': 24,
    'message': 'OK',
    'questions': [{'answer': 'Apollo 13',
                    'category': 5,
                    'difficulty': 4,
                    'id': 2,
                    'question': 'What movie earned Tom Hanks his third straight '
                                'Oscar nomination, in 1996?'},
                    {'answer': 'Tom Cruise',
                    'category': 5,
                    'difficulty': 4,
                    'id': 4,
                    'question': 'What actor did author Anne Rice first denounce, '
                                'then praise in the role of her beloved Lestat?'},

                    ...

                    {'answer': 'The Palace of Versailles',
                    'category': 3,
                    'difficulty': 3,
                    'id': 14,
                    'question': 'In which royal palace would you find the Hall of '
                                'Mirrors?'}],
    'success': True,
    'total_questions': 10
    }
    ```

`POST '/api/v1.0/search'`

* Searches questions based on a search term. Results return N questions that
 contain the search term. 

* **Request Arguments:** 
  - `searchTerm` (str)
  - `page` (int)

* **Returns:** A list of categories, a list of questions, the total number of 
questions.

    ```json
    {
    'code': '200',
    'message': 'OK',
    'questions': [{'answer': 'Agra',
                    'category': 3,
                    'difficulty': 2,
                    'id': 15,
                    'question': 'The Taj Mahal is located in which Indian city?'}],
    'success': True,
    'total_questions': 1
    }
    ```

`GET '/categories/<int:category_id>/questions'`
      
* Gets questions based on category. 

* **Request Arguments:** 
  - `question_id`(int)

* **Returns:** A list of categories, a list of questions, the total number of questions.

    ```json
    {
    'code': '200',
    'message': 'OK',
    'questions': [{'answer': 'The Liver',
                    'category': 1,
                    'difficulty': 4,
                    'id': 20,
                    'question': 'What is the heaviest organ in the human body?'},
                    {'answer': 'Alexander Fleming',
                    'category': 1,
                    'difficulty': 3,
                    'id': 21,
                    'question': 'Who discovered penicillin?'},
                    {'answer': 'Blood',
                    'category': 1,
                    'difficulty': 4,
                    'id': 22,
                    'question': 'Hematology is a branch of medicine involving the '
                                'study of what?'}],
    'success': True,
    'total_questions': 3
    }
    ```

`POST '/quizzes'`

* Get questions to play the quiz. The endpoint should take category and previous 
question parameters and return a random questions within the given category, 
if provided, and that is not one of the previous questions. 

* **Request Arguments:** 
  - `category` (int)
  - `previous_questions` (list)

* **Returns:** A list of categories, a list of questions, the total number of questions.

    ```json
    {
    "code": "200", 
    "message": "OK", 
    "question": {
        "answer": "Blood", 
        "category": 1, 
        "difficulty": 4, 
        "id": 22, 
        "question": "Hematology is a branch of medicine involving the study of what?"
    }, 
    "success": true
    }
    ```

* Example: `curl -X POST -H "Content-Type: application/json" -d '{"previous_questions": [20], "category": 1}' http://127.0.0.1:5000/quizzes`


## Testing

To run the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
