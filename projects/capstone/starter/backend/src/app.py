import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Movie, Actor

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  CORS(app)

  return app

app = create_app()

# initialize the datbase
setup_db(app)

'''
-------------------------- ENDPOINTS ------------------------------------------
'''

# GET /actors and /movies
@app.route('/actors')
#@requires_auth('get:actors')
def get_actors(jwt):
    actors = Actor.query.all()
    return jsonify({
        'success': True,
        'drinks': [actors.format() for actors in actors]
    }), 200

@app.route('/movies')
#@requires_auth('get:movies')
def get_movies(jwt):
    movies = Movie.query.all()
    return jsonify({
        'success': True,
        'movies': [movie.format() for movie in movies]
    }), 200

# DELETE /actors/ and /movies/
@app.route('/actors/<int:id>', methods=['DELETE'])
#@requires_auth('delete:actors')
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
#@requires_auth('delete:movies')
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
#@requires_auth('post:actors')
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
#@requires_auth('post:movies')
def create_movie(jwt):
    body = request.get_json()
    title = body.get('title', None)
    release_date = body.get('relase_date', None)

    try:
        movie = Movie(title=title, release_date=release_date)
        movie.insert()

        return jsonify({
            'success': True,
            'actor': [movie.format()]
        }), 200
    except:
        abort(422)

# PATCH /actors/ and /movies/
@app.route('/actors/<int:id>', methods=['PATCH'])
#@requires_auth('patch:actors')
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
#@requires_auth('patch:movies')
def update_movie(jwt, id):
    movie = Movie.query.filter(Movie.id == id).one_or_none()

    if not movie:
        abort(404)

    body = request.get_json()
    title = body.get('title', None)
    release_date = body.get('relase_date', None)

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


if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)