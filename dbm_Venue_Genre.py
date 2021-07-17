#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from app import db

#----------------------------------------------------------------------------#
# Venue_Genre - Model
#----------------------------------------------------------------------------#

class Venue_Genre(db.Model):
    __tablename__ = 'Venue_Genre'

    id = db.Column(db.Integer, primary_key=True)
    genre = db.Column(db.String(40))
    venue_id = db.Column(db.Integer,db.ForeignKey('Venue.id'),nullable=False)

    def __repr__(self):
        return f"<Venue_Genre venue_id:{self.venue_id} genre: {self.genre}>"
