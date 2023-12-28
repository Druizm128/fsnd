import os
import logging
from logging.handlers import RotatingFileHandler
from flask.logging import default_handler
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import Movie, Actor, db, setup_db
from auth import AuthError, requires_auth
import sqlalchemy as sa

def create_app(database_path, test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app, database_path=database_path)

    #CORS(app, resources={"*": {"origins": "*"}})
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Headers', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response
    
    # Check if the database needs to be initialized
    engine = sa.create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    inspector = sa.inspect(engine)
    if not inspector.has_table("movies"):
        with app.app_context():
            db.drop_all()
            db.create_all()
            app.logger.info('Initialized the database!')
    else:
        app.logger.info('Database already contains the movies table.')

    def configure_logging(app):
        # Logging Configuration
        if app.config['LOG_WITH_GUNICORN']:
            gunicorn_error_logger = logging.getLogger('gunicorn.error')
            app.logger.handlers.extend(gunicorn_error_logger.handlers)
            app.logger.setLevel(logging.DEBUG)
        else:
            file_handler = RotatingFileHandler('instance/flask-talent-management.log',
                                            maxBytes=16384,
                                            backupCount=20)
            file_formatter = logging.Formatter('%(asctime)s %(levelname)s %(threadName)s-%(thread)d: %(message)s [in %(filename)s:%(lineno)d]')
            file_handler.setFormatter(file_formatter)
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)

        # Remove the default logger configured by Flask
        app.logger.removeHandler(default_handler)

        app.logger.info('Starting the Flask Talent Management App...')


    '''
    -------------------------- ENDPOINTS ------------------------------------------
    '''

    # GET /actors and /movies
    @app.route('/actors')
    @requires_auth('get:actors')
    def get_actors(jwt):
        actors = Actor.query.all()

        if len(actors) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'actors': [actors.format() for actors in actors]
        }), 200

    @app.route('/movies')
    @requires_auth('get:movies')
    def get_movies(jwt):
        movies = Movie.query.all()

        if len(movies) == 0:
            abort(404)

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

    @app.errorhandler(403)
    def forbidden(error):
        '''implement error forbidden for 403'''
        return jsonify({
            "success": False,
            "error": 403,
            "message": "forbidden"
        }), 403


    @app.errorhandler(404)
    def not_found(error):
        '''implement error handler for 404'''
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404
    
    @app.errorhandler(405)
    def not_found(error):
        '''implement error handler for 404'''
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 404


    @app.errorhandler(AuthError)
    def auth_error(error):
        '''implement AuthError'''
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error['description']
        }), error.status_code

    return app

database_name = "talentagency"
#database_path = "postgresql://{}/{}".format('localhost:5432', database_name)
database_path="postgresql://talentagency_user:aOKxJHyrMCsFPsQw04q3EPgzmk45QcPn@dpg-cm6ccenqd2ns73et58vg-a/talentagency"
# database_path = os.environ['DATABASE_URL']
# if database_path.startswith("postgres://"):
#   database_path = database_path.replace("postgres://", "postgresql://", 1)

app = create_app(database_path=database_path, test_config=None)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)