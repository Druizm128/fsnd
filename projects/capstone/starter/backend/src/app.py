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

APP = create_app()

# initialize the datbase
setup_db(APP)

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
def create_actor(jwt):
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




if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)