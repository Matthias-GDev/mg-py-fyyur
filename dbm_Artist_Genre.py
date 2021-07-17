#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from app import db

#----------------------------------------------------------------------------#
# Artist_Genre - Model
#----------------------------------------------------------------------------#

class Artist_Genre(db.Model):
    __tablename__ = 'Artist_Genre'

    id = db.Column(db.Integer, primary_key=True)
    genre = db.Column(db.String(40))
    artist_id = db.Column(db.Integer,db.ForeignKey('Artist.id'),nullable=False)