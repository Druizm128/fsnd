from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
db = SQLAlchemy()
migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    genres = db.Column(db.ARRAY(db.String(120)), nullable=False)
    facebook_link = db.Column(db.String(120), nullable=True)
    image_link = db.Column(db.String(500), nullable=True)
    website_link = db.Column(db.String(120), nullable=True)
    seeking_talent = db.Column(db.Boolean(), nullable=False, default=False)
    seeking_description = db.Column(db.String(500), nullable=False)
    shows = db.relationship('Show', backref='show_venues', lazy='joined', cascade='all, delete')
    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    
    def to_dict(self):
      return {
        'id': self.id,
        'name': self.name,
        'city': self.city,
        'state': self.state,
        'address': self.address,
        'phone': self.phone,
        'genres': self.genres,
        'facebook_link': self.facebook_link,
        'image_link': self.image_link,
        'website': self.website_link,
        'seeking_talent': self.seeking_talent,
        'seeking_description': self.seeking_description
      }
    
    def __repr__(self):
      return f'<Venue Id: {self.id}, Name: {self.name}>'
class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String(120)), nullable=False)
    facebook_link = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    website_link = db.Column(db.String(120))
    looking_for_venues = db.Column(db.Boolean(), nullable=False, default=False)
    seeking_description = db.Column(db.String(500))    
    shows = db.relationship('Show', backref='artist_venues', lazy='joined', cascade='all, delete')

    def to_dict(self):
      return {
        'id': self.id,
        'name': self.name,
        'city': self.city,
        'state': self.state,
        'phone': self.phone,
        'genres': self.genres,
        'facebook_link': self.facebook_link,
        'image_link': self.image_link,
        'website': self.website_link,
        'seeking_for_venues': self.looking_for_venues,
        'seeking_description': self.seeking_description
      }
    
    def __repr__(self):
      return f'<Artist Id: {self.id}, Name: {self.name}>'
    
    # TODO: implement any missing fields, as a database migration using Flask-Migrate
class Show(db.Model):
    
    __tablename__ = 'Show'
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)

    def to_dict(self):
      return {
        'id': self.id,
        'artist_id': self.artist_id,
        'venue_id': self.venue_id,
        'start_time': self.start_time
      }

    def __repr__(self):
      return f'<Show Id: {self.id}, Artist: {self.artist_id}, Venue: {self.venue_id}>'

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
