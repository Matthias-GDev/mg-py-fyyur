#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from app import db

#----------------------------------------------------------------------------#
# Artist - Model
#----------------------------------------------------------------------------#

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
