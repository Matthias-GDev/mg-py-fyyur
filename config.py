import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database


# IMPLEMENT DATABASE URL

SQLALCHEMY_TRACK_MODIFICATIONS = False
DB_HOST = os.getenv('DB_HOST', 'localhost:5433')
DB_USER = os.getenv('DB_USER', 'matthias')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'matthias')
DB_NAME = os.getenv('DB_NAME', 'fyyur')

SQLALCHEMY_DATABASE_URI='postgresql+psycopg2://{}:{}@{}/{}'.format(DB_USER, DB_PASSWORD, DB_HOST, DB_NAME)
#SQLALCHEMY_DATABASE_URI = 'postgresql://matthias:matthias@localhost:5433/fyyur'