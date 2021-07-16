#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import sys
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
#from flask_wtf import FlaskForm
from forms import *
from flask_migrate import Migrate

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')

# connect to a local postgresql database
db = SQLAlchemy(app)
migrate = Migrate(app, db)


#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    # implement any missing fields, as a database migration using Flask-Migrate
    #Website link
    website_link = db.Column(db.String(120))
    #Looking for talent
    seeking_newtalents = db.Column(db.Boolean,nullable=True,default=False)
    #Seeking Description
    seeking_description = db.Column(db.String(150))
    
    #relations
    genres = db.relationship('Venue_Genre',backref='Venue',lazy=True)

class Venue_Genre(db.Model):
    __tablename__ = 'Venue_Genre'

    id = db.Column(db.Integer, primary_key=True)
    genre = db.Column(db.String(40))
    venue_id = db.Column(db.Integer,db.ForeignKey('Venue.id'),nullable=False)


class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    #Website link
    website_link = db.Column(db.String(120))
    #Looking for talent
    seeking_newvenues = db.Column(db.Boolean,nullable=True,default=False)
    #Seeking Description
    seeking_description = db.Column(db.String(150))

    #relations
    genres = db.relationship('Artist_Genre',backref='Artist',lazy=True)

    #implement any missing fields, as a database migration using Flask-Migrate

class Artist_Genre(db.Model):
    __tablename__ = 'Artist_Genre'

    id = db.Column(db.Integer, primary_key=True)
    genre = db.Column(db.String(40))
    artist_id = db.Column(db.Integer,db.ForeignKey('Artist.id'),nullable=False)

class Show(db.Model):
    __tablename__ = 'Show'

    artistid = db.Column(db.Integer,db.ForeignKey('Artist.id'), primary_key=True)
    venueid = db.Column(db.Integer,db.ForeignKey('Venue.id'), primary_key=True)
    starttime = db.Column(db.DateTime,nullable=False)

# Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format='EE MM, dd, y h:mma'
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
  # replace with real venues data.
  # num_shows should be aggregated based on number of upcoming shows per venue.

  try:
      new_venues_data=[]

      #Get all DISTINCT cities
      cities = db.session.query(Venue.city,Venue.state).distinct(Venue.city,Venue.state).all()

      for city in cities:
        data = {}
        data['city'] = city[0]
        data['state'] = city[1]
        data['venues'] = db.session.query(Venue).filter(Venue.city == city[0]).filter(Venue.state == city[1]).all()
        new_venues_data.append(data)

  except:
    flash('An error occurred loading Venues')
    print(sys.exc_info())

  finally:
    db.session.close()

  return render_template('pages/venues.html', areas=new_venues_data); 

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return 'The Musical Hop'.
  # search for 'Music' should return 'The Musical Hop' and 'Park Square Live Music & Coffee'
  try:
    search_term = request.form.get('search_term')
    searchresult = db.session.query(Venue).filter(Venue.name.ilike(f'%{search_term}%'))
    data=[]

    for venueitem in searchresult:
      upcomingshows = db.session.query(Show).filter(Show.venueid == venueitem.id).filter(Show.starttime >= str(datetime.now()).split('.',1)[0]).all()
      ditem={}
      ditem['id'] = venueitem.id
      ditem['name'] = venueitem.name
      ditem['num_upcoming_shows'] = len(upcomingshows)
      data.append(ditem)
    
    response = {
      'count':len(data),
      'data':data,
    }

  except Exception as error:
    flash('An error occurred. During seach for'+search_term+' Error:'+str(error))
    print(sys.exc_info())

  finally:
    db.session.close()

  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # replace with real venue data from the venues table, using venue_id
  data={}

  try:
    venueitem = db.session.query(Venue).filter(Venue.id==venue_id).all()[0]

    venuesgenres = db.session.query(Venue_Genre).filter(Venue_Genre.venue_id==venue_id).all()

    genresdata = []
    for genreitem in venuesgenres:
      genresdata.append(genreitem.genre)

    datapastshows=[]
    pastshows = db.session.query(Show).filter(Show.venueid == venueitem.id).filter(Show.starttime<=str(datetime.now()).split('.',1)[0] ).all()
    for pastshowitem in pastshows:
      artist=db.session.query(Artist).filter(Artist.id==pastshowitem.artistid).all()[0]
      pastshow={
        'artist_id': artist.id,
        'artist_image_link': artist.image_link,
        'start_time': pastshowitem.starttime
      }
      datapastshows.append(pastshow)

    dataupcumingshows=[]
    upcomingshows = db.session.query(Show).filter(Show.venueid == venueitem.id).filter(Show.starttime>=str(datetime.now()).split('.',1)[0]).all()
    for showitem in upcomingshows:
      artist=db.session.query(Artist).filter(Artist.id==showitem.artistid).all()[0]
      upshow={
        'artist_id': artist.id,
        'artist_image_link': artist.image_link,
        'start_time': showitem.starttime
      }
      dataupcumingshows.append(upshow)

    data = {
        'id': venueitem.id,
        'name': venueitem.name,
        'genres': genresdata,
        'address': venueitem.address,
        'city': venueitem.city,
        'state': venueitem.state,
        'phone': venueitem.phone,
        'website': venueitem.website_link,
        'facebook_link': venueitem.facebook_link,
        'seeking_talent': venueitem.seeking_newtalents,
        'image_link': venueitem.image_link,
        'past_shows': datapastshows,
        'upcoming_shows': dataupcumingshows,
        'past_shows_count': len(datapastshows),
        'upcoming_shows_count': len(dataupcumingshows),
    }

  except Exception as error:
    flash('An error occurred loading Venue with id:'+str(venue_id)+' Error:'+str(error))
    print(sys.exc_info())

  finally:
    db.session.close()

  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  try:

    #form data
    new_name = request.form.get('name') 
    new_city = request.form.get('city') 
    new_state = request.form.get('state') 
    new_address = request.form.get('address') 
    new_phone = request.form.get('phone') 
    new_image_link = request.form.get('image_link') 
    new_website_link = request.form.get('website_link') 
    new_facebook_link = request.form.get('facebook_link') 
    new_seeking_newtalents = request.form.get('seeking_talent')
    new_seeking_description = request.form.get('description')

    if new_seeking_newtalents == 'y':
      new_seeking_newtalents=True
    else:
      new_seeking_newtalents=False

    newvenuedata = Venue(
      name=new_name,
      city=new_city,
      state=new_state,
      address=new_address,
      phone=new_phone,
      image_link=new_image_link,
      facebook_link=new_facebook_link,
      website_link=new_website_link,
      seeking_newtalents=new_seeking_newtalents,
      seeking_description=new_seeking_description,
    )

    db.session.add(newvenuedata)
    db.session.flush()
        
    #geners
    newgenres = request.form.getlist('genres')
    
    for genreitem in newgenres:
      new_genre = Venue_Genre(genre=genreitem)
      new_genre.venue_id = newvenuedata.id
      db.session.add(new_genre)
      #array_venues.append(new_genre)
    
    db.session.commit()
    db.session.refresh(newvenuedata)
    flash('Venue + Genres: ' + newvenuedata.name + ' was successfully listed!')

  except:
    db.session.rollback()
    flash('An error occurred. Venue ' + new_name + ' could not be listed.')
    print(sys.exc_info())

  finally:
    db.session.close()
  
  return render_template('pages/home.html')
  # insert form data as a new Venue record in the db, instead
  # modify data to be the data object returned from db insertion

  # on successful db insert, flash success
  #flash('Venue ' + request.form['name'] + ' was successfully listed!')
  # on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  try:
    venue = db.session.query(Venue).filter(Venue.id==venue_id).all()
    venue_name=venue.name
    venue.delete()
    db.session.commit()
    flash('Deleting Venue:' + venue_name + ' successful!')
  except:
    db.session.rollback()
    flash('An error occurred. Deleting Venue: ' + new_name + ' failed.')
    print(sys.exc_info())
  finally:
    db.session.close()

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # replace with real data returned from querying the database
  try:
    new_artists_data=[]

    artists = db.session.query(Artist.id,Artist.name).all()

    for artistitem in artists:
      data={}
      data['id'] = artistitem[0]
      data['name'] = artistitem[1]
      new_artists_data.append(data)

  except:
    flash('An error occurred loading Artists')
    print(sys.exc_info())
  finally:
    db.session.close()

  return render_template('pages/artists.html', artists=new_artists_data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for 'A' should return 'Guns N Petals', 'Matt Quevado', and 'The Wild Sax Band'.
  # search for 'band' should return 'The Wild Sax Band'.

  try:
    search_term = request.form.get('search_term')
    searchresult = db.session.query(Artist).filter(Artist.name.ilike(f'%{search_term}%'))
    data=[]

    for artistitem in searchresult:
      upcomingshows = db.session.query(Show).filter(Show.artistid == artistitem.id).filter(Show.starttime >= str(datetime.now()).split('.',1)[0]).all()
      ditem={}
      ditem['id'] = artistitem.id
      ditem['name'] = artistitem.name
      ditem['num_upcoming_shows'] = len(upcomingshows)
      data.append(ditem)

    response = {
      'count':len(data),
      'data':data,
    }

  except Exception as error:
    flash('An error occurred. During seach for'+search_term+' Error:'+str(error))
    print(sys.exc_info())
  
  finally:
    db.session.close()

  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # replace with real artist data from the artist table, using artist_id

  data={}

  try:
    artist=db.session.query(Artist).filter(Artist.id==artist_id).all()[0]
    artistgenres=db.session.query(Artist_Genre).filter(Artist_Genre.artist_id==artist_id)

    genres=[]
    for genreitem in artistgenres:
      genres.append(genreitem.genre)

    datapastshows=[]
    pastshows = db.session.query(Show).filter(Show.artistid == artist_id).filter(Show.starttime<=str(datetime.now()).split('.',1)[0] ).all()
    for pastshowitem in pastshows:
      venue=db.session.query(Venue).filter(Venue.id==pastshowitem.venueid).all()[0]
      pastshow={
        'venue_id': venue.id,
        'venue_name': venue.name,
        'venue_image_link': venue.image_link,
        'start_time': pastshowitem.starttime
      }
      datapastshows.append(pastshow)

    dataupcumingshows=[]
    upcomingshows = db.session.query(Show).filter(Show.artistid == artist_id).filter(Show.starttime>=str(datetime.now()).split('.',1)[0]).all()
    for showitem in upcomingshows:
      venue=db.session.query(Venue).filter(Venue.id==pastshowitem.venueid).all()[0]
      upshow={
        'venue_id': venue.id,
        'venue_name': venue.name,
        'venue_image_link': venue.image_link,
        'start_time': showitem.starttime
      }
      dataupcumingshows.append(upshow)

    data={
      'id': artist.id,
      'name': artist.name,
      'genres': genres,
      'city': artist.city,
      'state': artist.state,
      'phone': artist.phone,
      'website': artist.website_link,
      'facebook_link': artist.facebook_link,
      'seeking_venue': artist.seeking_newvenues,
      'seeking_description': artist.seeking_description,
      'image_link': artist.image_link,
      'past_shows':datapastshows,
      'upcoming_shows': dataupcumingshows,
      'past_shows_count': len(datapastshows),
      'upcoming_shows_count': len(dataupcumingshows),
    }

  except Exception as error:
    flash('An error occurred. During loading artist with id'+str(artist_id)+' Error:'+str(error))
    print(sys.exc_info())

  finally:
    db.session.close()

  return render_template('pages/show_artist.html', artist=data)


#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  data={}

  try:
    artist=db.session.query(Artist).filter(Artist.id==artist_id).all()[0]
    artistgenres=db.session.query(Artist_Genre).filter(Artist_Genre.artist_id==artist_id)

    genres=[]
    for genreitem in artistgenres:
      genres.append(genreitem.genre)

    data = {
      'id': artist.id,
      'name': artist.name,
      'genres': genres,
      'city': artist.city,
      'state': artist.state,
      'phone': artist.phone,
      'website': artist.website_link,
      'facebook_link': artist.facebook_link,
      'seeking_venue': artist.seeking_newvenues,
      'seeking_description': artist.seeking_description,
      'image_link': artist.image_link
    }

    flash(data)

  except Exception as error:
    flash('An error occurred. During loading artist with id'+str(artist_id)+' Error:'+str(error))
    print(sys.exc_info())

  finally:
    db.session.close()
 
  # populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=data)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  try:
    updateartist=db.session.query(Artist).filter(Artists.id==artist_id).all()[0]

    new_name = request.form.get('name') 
    new_city = request.form.get('city') 
    new_state = request.form.get('state') 
    new_phone = request.form.get('phone') 
    new_image_link = request.form.get('image_link') 
    new_website_link = request.form.get('website_link') 
    new_facebook_link = request.form.get('facebook_link') 
    new_seeking_venues = request.form.get('seeking_venue')
    new_seeking_description = request.form.get('seeking_description')

    if new_seeking_venues == 'y':
      new_seeking_venues=True
    else:
      new_seeking_venues=False

    updateartist.name=new_name,
    updateartist.city=new_city,
    updateartist.state=new_state,
    updateartist.phone=new_phone,
    updateartist.image_link=new_image_link,
    updateartist.facebook_link=new_facebook_link,
    updateartist.website_link=new_website_link,
    updateartist.seeking_newvenues=new_seeking_venues,
    updateartist.seeking_description=new_seeking_description,

    db.session.add(updateartist)
    db.session.commit()

    db.session.refresh(updateartist)
    flash("Artist update successfull! Artist:"+updateartist.name)

  except Exception as error:
    db.session.rollback()
    flash('An error occurred. During editing artist with id'+str(artist_id)+' Error:'+str(error))
    print(sys.exc_info())

  finally:
    db.session.close()

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue = Venue.query.get(venue_id)

  # populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes

  try:

    venue = db.session.query(Venue).filter(Venue.id==venue_id).all()[0]

    #form data
    update_name = request.form.get('name') 
    update_city = request.form.get('city') 
    update_state = request.form.get('state') 
    update_address = request.form.get('address') 
    update_phone = request.form.get('phone') 
    update_image_link = request.form.get('image_link') 
    update_website_link = request.form.get('website_link') 
    update_facebook_link = request.form.get('facebook_link') 
    update_seeking_newtalents = request.form.get('seeking_talent')
    update_seeking_description = request.form.get('description')

    if update_seeking_newtalents == 'y':
      update_seeking_newtalents=True
    else:
      update_seeking_newtalents=False

    venue.name=update_name
    venue.city=update_city
    venue.state=update_state
    venue.address=update_address
    venue.phone=update_phone
    venue.image_link=update_image_link
    venue.facebook_link=update_facebook_link
    venue.website_link=update_website_link
    venue.seeking_newtalents=update_seeking_newtalents
    venue.seeking_description=update_seeking_description

    db.session.add(venue)
    db.session.commit()

    db.session.refresh(venue)
    flash("Venue update successfull! Venue:"+venue.name)

  except Exception as error:
    db.session.rollback()
    flash('An error occurred. During editing venue with id'+str(venue_id)+' Error:'+str(error))
    print(sys.exc_info())

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
  # insert form data as a new artist record in the db, instead
  # modify data to be the data object returned from db insertion
  try:
    #form data
    new_name = request.form.get('name') 
    new_city = request.form.get('city') 
    new_state = request.form.get('state') 
    new_phone = request.form.get('phone') 
    new_image_link = request.form.get('image_link') 
    new_website_link = request.form.get('website_link') 
    new_facebook_link = request.form.get('facebook_link') 
    new_seeking_venues = request.form.get('seeking_venue')
    new_seeking_description = request.form.get('seeking_description')

    if new_seeking_venues == 'y':
      new_seeking_venues=True
    else:
      new_seeking_venues=False

    newartist = Artist(
      name=new_name,
      city=new_city,
      state=new_state,
      phone=new_phone,
      image_link=new_image_link,
      facebook_link=new_facebook_link,
      website_link=new_website_link,
      seeking_newvenues=new_seeking_venues,
      seeking_description=new_seeking_description,
    )

    db.session.add(newartist)
    db.session.flush()

    #geners
    newgenres = request.form.getlist('genres')
    
    for genreitem in newgenres:
      new_genre = Artist_Genre(genre=genreitem)
      new_genre.artist_id = newartist.id
      db.session.add(new_genre)
    
    db.session.commit()
    db.session.refresh(new_genre)

    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  except:
    db.session.rollback()
    flash('An error occurred. New Artist: ' + new_name + ' could not be listed.')
    print(sys.exc_info())
  finally:
    db.session.close()
  
  return render_template('pages/home.html')

  # on successful db insert, flash success
  # on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # replace with real venues data.
  
  data=[]

  try:

    showsresult = db.session.query(Show).all()

    for showitem in showsresult:
      artist_id=showitem.artistid
      venue_id=showitem.venueid
      starttime=showitem.starttime

      artist=db.session.query(Artist).filter(Artist.id==artist_id).all()[0]
      venue=db.session.query(Venue).filter(Venue.id==venue_id).all()[0]

      showdataitem = {
        'venue_id':venue.id,
        'venue_name': venue.name,
        'artist_id': artist.id,
        'artist_name': artist.name,
        'artist_image_link': artist.image_link,
        'start_time': str(starttime)
      }
      data.append(showdataitem)

  except Exception as error:
    flash('An error occurred.Load all Shows - Error:'+str(error))
    print(sys.exc_info())
  
  finally:
    db.session.close()

  return render_template('pages/shows.html', shows=data)  

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # insert form data as a new Show record in the db, instead
  try:

    new_artist_id = request.form.get('artist_id') 
    new_venue_id = request.form.get('venue_id') 
    new_start_time = request.form.get('start_time') 

    new_show = Show(
      artistid = new_artist_id,
      venueid = new_venue_id,
      starttime = new_start_time,
    )
    
    db.session.add(new_show)
    db.session.commit()
    
    flash('Show was successfully listed!')    
  except Exception as error:
    db.session.rollback()
    flash('An error occurred. New Show could not be listed. Error:'+str(error))
    print(sys.exc_info())

  finally:
    db.session.close()

  # on successful db insert, flash success
  
  # on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

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
