import os

SQLALCHEMY_DATABASE_URI = 'sqlite:///tangle.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = os.urandom(24)
