from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from multiprocessing import SimpleQueue, Value, Lock

app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)
node_queue = SimpleQueue()
alpha = Value('d')
lambd = Value('d', 1.0)
paused = Value('b', True)
lock = Lock()

from app import views, db