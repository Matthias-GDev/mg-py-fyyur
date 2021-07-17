#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from app import db

#----------------------------------------------------------------------------#
# Show - Model
#----------------------------------------------------------------------------#

class Show(db.Model):
    __tablename__ = 'Show'

    artistid = db.Column(db.Integer,db.ForeignKey('Artist.id'), primary_key=True)
    venueid = db.Column(db.Integer,db.ForeignKey('Venue.id'), primary_key=True)
    starttime = db.Column(db.DateTime,nullable=False)

    def __repr__(self):
        return f"<Show artistid:{self.artistid} venueid: {self.venueid} - starttime: {self.starttime}>"
