import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import Movie, Actor, db
from auth import AuthError, requires_auth

def create_app(database_path,test_config=None):
    app = Flask(__name__)
    CORS(app)
    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI=database_path
    )
    
    if test_config is not None:
        app.config.from_mapping(test_config)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app

database_name = "talentagency"
database_path = "postgresql://{}/{}".format('localhost:5432', database_name)

db = SQLAlchemy()
app = create_app(database_path=database_path,test_config=None)

'''
-------------------------- ENDPOINTS ------------------------------------------
'''

# GET /actors and /movies
@app.route('/actors')
@requires_auth('get:actors')
def get_actors(jwt):
    actors = Actor.query.all()
    return jsonify({
        'success': True,
        'actors': [actors.format() for actors in actors]
    }), 200

@app.route('/movies')
@requires_auth('get:movies')
def get_movies(jwt):
    movies = Movie.query.all()
    return jsonify({
        'success': True,
        'movies': [movie.format() for movie in movies]
    }), 200

# DELETE /actors/ and /movies/
@app.route('/actors/<int:id>', methods=['DELETE'])
@requires_auth('delete:actors')
def delete_actor(jwt, id):
    actor = Actor.query.filter(Actor.id == id).one_or_none()

    if not actor:
        abort(404)

    try:
        actor.delete()

        return jsonify({
            'success': True,
            'delete': id
        }), 200
    except:
        abort(422)

@app.route('/movies/<int:id>', methods=['DELETE'])
@requires_auth('delete:movies')
def delete_movie(jwt, id):
    movie = Movie.query.filter(Movie.id == id).one_or_none()

    if not movie:
        abort(404)

    try:
        movie.delete()

        return jsonify({
            'success': True,
            'delete': id
        }), 200
    except:
        abort(422)


# POST /actors and /movies and
@app.route('/actors', methods=['POST'])
@requires_auth('post:actors')
def create_actor(jwt):
    body = request.get_json()
    name = body.get('name', None)
    age = body.get('age', None)
    gender = body.get('gender', None)

    try:
        actor = Actor(name=name, age=age, gender=gender)
        actor.insert()

        return jsonify({
            'success': True,
            'actor': [actor.format()]
        }), 200
    except:
        abort(422)

@app.route('/movies', methods=['POST'])
@requires_auth('post:movies')
def create_movie(jwt):
    body = request.get_json()
    print(body)
    title = body.get('title', None)
    release_date = body.get('release_date', None)

    try:
        movie = Movie(title=title, release_date=release_date)
        movie.insert()

        return jsonify({
            'success': True,
            'movie': [movie.format()]
        }), 200
    except:
        abort(422)

# PATCH /actors/ and /movies/
@app.route('/actors/<int:id>', methods=['PATCH'])
@requires_auth('patch:actors')
def update_actor(jwt, id):
    actor = Actor.query.filter(Actor.id == id).one_or_none()

    if not actor:
        abort(404)

    body = request.get_json()
    name = body.get('name', None)
    age = body.get('age', None)
    gender = body.get('gender', None)

    try:
        actor.name = name
        actor.age = age
        actor.gender = gender

        actor.update()

        return jsonify({
            'success': True,
            'actor': [actor.format()]
        }), 200
    except:
        abort(422)

@app.route('/movies/<int:id>', methods=['PATCH'])
@requires_auth('patch:movies')
def update_movie(jwt, id):
    movie = Movie.query.filter(Movie.id == id).one_or_none()

    if not movie:
        abort(404)

    body = request.get_json()
    print(f"body: {body}")
    title = body.get('title', None)
    release_date = body.get('release_date', None)

    try:
        movie.title = title
        movie.release_date = release_date

        movie.update()

        return jsonify({
            'success': True,
            'movie': [movie.format()]
        }), 200
    except:
        abort(422)

'''
----------------------------- ERROR HANDLING ----------------------------------
'''


@app.errorhandler(400)
def bad_request(error):
    '''implement error handler for 400'''
    return jsonify({
        "success": False,
        "error": 400,
        "message": "bad request"
    }), 400


@app.errorhandler(404)
def not_found(error):
    '''implement error handler for 404'''
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404


@app.errorhandler(AuthError)
def auth_error(error):
    '''implement AuthError'''
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error['description']
    }), error.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)