#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
import sys
import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from sqlalchemy.exc import SQLAlchemyError
from models import *

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

# TODO: connect to a local postgresql database
app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db.init_app(app)
#migrate = Migrate(app, db)



#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')

#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
  def search_venues(state, city):
    '''Searches for all venues in given state and city.'''
    query=(
      db.session
        .query(
          Venue.city,
          Venue.state,
          Venue.id,
          Venue.name,
        )
        .select_from(Venue)
        .filter(
          Venue.state == state, 
          Venue.city == city)
        .all()
    )
    venues = [{'id': venue[2], 'name': venue[3]} for venue in query]
    return venues

  def search_shows(state, city, venue_id):
    '''Searches shows in a given venue'''
    query=(
      db.session
        .query(
          Venue.city,
          Venue.state,
          Venue.id,
          Venue.name,
        )
        .select_from(Venue)
        .join(Show)
        .filter(
          Venue.state == state, 
          Venue.city == city,
          Show.venue_id == venue_id
        )
        .all()
    )

    num_upcoming_shows = len(query)
    return num_upcoming_shows
  
  # Search for available states and cities
  cities=(
    db.session
      .query(
        Venue.city,
        Venue.state,
      )
      .select_from(Venue)
      .all()
  )
  cities=sorted(set(cities))

  # For each city append the available venues
  data = []
  for city in cities:
    data.append({
      'city':city[0],
      'state':city[1],
      'venues': search_venues(city[1], city[0]),
    })

  # For each Venue insert incoming shows
  for record in data:
    state = record['state']
    city = record['city']
    venues=record['venues'] 
    for venue in venues:
      venue_id=venue['id']
      venue['num_upcoming_shows']= search_shows(state = state, city = city, venue_id = venue_id)

  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on venues with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"

  search_term = request.form.get('search_term')

  search_results=(
    db.session
      .query(
          Venue.id, 
          Venue.name
      )
      .filter(Venue.name.ilike(f'%{search_term}%'))
      .all()
  )

  response = {}
  response['id'] = len(search_results)
  response['data'] = search_results

  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  venue = Venue.query.get(venue_id)
  data=venue.to_dict()

  query_past_shows = (
    db.session
      .query(Show)
      .join(Artist)
      .filter(Show.venue_id==venue_id)
      .filter(Show.start_time<datetime.now())
      .all()
  )

  past_shows = []
  for show in query_past_shows:
    past_shows.append({
      "artist_id": show.artist_venues.id,
      "artist_name": show.artist_venues.name,
      "artist_image_link": show.artist_venues.image_link,
      "start_time": show.start_time.strftime('%Y-%m-%d %H:%M:%S')
    })

  query_upcoming_shows = (
    db.session
      .query(Show)
      .join(Artist)
      .filter(Show.venue_id==venue_id)
      .filter(Show.start_time>=datetime.now())
      .all()
  )
  
  upcoming_shows = []
  for show in query_upcoming_shows:
    upcoming_shows.append({
      "artist_id": show.artist_venues.id,
      "artist_name": show.artist_venues.name,
      "artist_image_link": show.artist_venues.image_link,
      "start_time": show.start_time.strftime('%Y-%m-%d %H:%M:%S')
    })
  
  data['past_shows'] = past_shows
  data['upcoming_shows'] = upcoming_shows
  data['past_shows_count'] = len(past_shows)
  data['upcoming_shows_count'] = len(upcoming_shows)

  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  form = VenueForm(request.form)

  if not form.validate():
    flash(f'Venue {form.name.data} was unsuccessfully listed!')
    return render_template('pages/home.html')
  
  try:
    venue = Venue(
      name = form.name.data,
      city = form.city.data,
      state = form.state.data,
      address = form.address.data,
      phone = form.phone.data,
      genres = form.genres.data,
      facebook_link = form.facebook_link.data,
      image_link = form.image_link.data,
      website_link = form.website_link.data,
      seeking_talent = form.seeking_talent.data,
      seeking_description = form.seeking_description.data
    )
    db.session.add(venue)
    db.session.commit()
    flash('Venue ' + form.name.data + ' was successfully listed!')
  except SQLAlchemyError as e:
     db.session.rollback()
     error=True
     print(sys.exc_info())
     flash('An error occurred. Venue ' + form.name.data + ' could not be listed.')
  finally:
    db.session.close()
  # on successful db insert, flash success
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  try:
    Venue.query.filter_by(id=venue_id).delete()
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()
  return None
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  results=(
    db.session
      .query(
        Artist.id,
        Artist.name
      )
      .select_from(Artist)
      .all()
  )

  data = []
  for result in results:
    data.append({
      'id':result[0],
      'name':result[1]
    })

  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  response={
    "count": 1,
    "data": [{
      "id": 4,
      "name": "Guns N Petals",
      "num_upcoming_shows": 0,
    }]
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id

  artist = Artist.query.get(artist_id)
  data=artist.to_dict()

  query_past_shows = (
    db.session
      .query(Show)
      .join(Venue)
      .filter(Show.artist_id==artist_id)
      .filter(Show.start_time<datetime.now())
      .all()
  )

  past_shows = []
  for show in query_past_shows:
    past_shows.append({
      "venue_id": show.show_venues.id,
      "venue_name": show.show_venues.name,
      "venue_image_link": show.show_venues.image_link,
      "start_time": show.start_time.strftime('%Y-%m-%d %H:%M:%S')
    })

  query_upcoming_shows = (
    db.session
      .query(Show)
      .join(Venue)
      .filter(Show.artist_id==artist_id)
      .filter(Show.start_time>=datetime.now())
      .all()
  )
  
  upcoming_shows = []
  for show in query_upcoming_shows:
    upcoming_shows.append({
      "venue_id": show.show_venues.id,
      "venue_name": show.show_venues.name,
      "venue_image_link": show.show_venues.image_link,
      "start_time": show.start_time.strftime('%Y-%m-%d %H:%M:%S')
    })
  
  data['past_shows'] = past_shows
  data['upcoming_shows'] = upcoming_shows
  data['past_shows_count'] = len(past_shows)
  data['upcoming_shows_count'] = len(upcoming_shows)

  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  artist = Artist.query.get(artist_id)
  form = ArtistForm(obj=artist)
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  # Retrieve the artist from the database based on the artist_id
  form = ArtistForm(request.form)

  try:
    artist = Artist.query.get(artist_id)
    form.populate_obj(artist)
    db.session.commit()
    flash(f"Venue {form.name.data} was successfully edited!")

  except ValueError as e:
    db.session.rollback()
    flash(f"An error occurred in {form.name.data}. Error: {str(e)}")

  finally:
    db.session.close()
  
  return redirect(url_for("show_artist", artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  venue = Venue.query.get(venue_id)
  form = VenueForm(obj=venue)

  # TODO: populate form with values from venue with ID <venue_id>
  return render_template("forms/edit_venue.html", form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes

  form = VenueForm(request.form)

  try:
    venue = Venue.query.get(venue_id)
    form.populate_obj(venue)
    db.session.commit()
    flash(f"Venue {form.name.data} was successfully edited!")

  except ValueError as e:
    db.session.rollback()
    flash(f"An error occurred in {form.name.data}. Error: {str(e)}")

  finally:
    db.session.close()

  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  form = ArtistForm(request.form)

  if not form.validate():
    flash(f'Artist {form.name.data} was unsuccessfully listed!')
    return render_template('pages/home.html')
  
  try:
    artist = Artist(
      name = form.name.data,
      city = form.city.data,
      state = form.state.data,
      phone = form.phone.data,
      genres = form.genres.data,
      facebook_link = form.facebook_link.data,
      image_link = form.image_link.data,
      website_link = form.website_link.data,
      looking_for_venues = form.seeking_venue.data,
      seeking_description = form.seeking_description.data
    )
    db.session.add(artist)
    db.session.commit()
    # on successful db insert, flash success
    flash('Artist ' + form.name.data + ' was successfully listed!')
  except SQLAlchemyError as e:
    db.session.rollback()
    error=True
    print(sys.exc_info())
    # on unsuccessful db insert, flash an error instead.
    flash('An error occurred. Artist ' + form.name.data + ' could not be listed.')
  finally:
    db.session.close()
  return render_template('pages/home.html')



#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  results=(
    db.session
      .query(
        Artist.id,
        Artist.name,
        Venue.id, 
        Venue.name, 
        Artist.image_link, 
        Show.start_time)
      .select_from(Show)
      .join(Artist)
      .join(Venue)
      .all()
  )

  data = []
  for result in results:
    data.append({
      'artist_id':result[0],
      'artist_name':result[1],
      'venue_id':result[2],
      'venue_name':result[3],
      'artist_image_link':result[4],
      'start_time': result[5].strftime('%Y-%m-%d %H:%M:%S')
    })

  return render_template(
    'pages/shows.html', 
    shows=data
  )

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():

  form = ShowForm(request.form)

  if not form.validate():
    flash(f'Show was unsuccessfully listed!')
    return render_template('pages/home.html')
  
  try:
    show = Show(
      artist_id = form.artist_id.data,
      venue_id = form.venue_id.data,
      start_time = form.start_time.data
    )
    db.session.add(show)
    db.session.commit()
    # on successful db insert, flash success
    flash(f'Show was successfully listed!')
  except SQLAlchemyError as e:
    db.session.rollback()
    error=True
    print(sys.exc_info())
    # on unsuccessful db insert, flash an error instead.
    flash(f'An error occurred. Show could not be listed.')
  finally:
    db.session.close()
  return render_template('pages/home.html', form=form)

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
