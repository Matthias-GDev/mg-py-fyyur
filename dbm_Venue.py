#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from app import db

#----------------------------------------------------------------------------#
# Venue - Model
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

    def __repr__(self):
        return f"<Venue id:{self.id} name: {self.name} city: {self.city}>"