import os

SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = os.urandom(24)
