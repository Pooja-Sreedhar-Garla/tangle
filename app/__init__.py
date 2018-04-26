from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from multiprocessing import SimpleQueue, Value, Lock

app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)
node_queue = SimpleQueue()
alpha = Value('d', 0.5)
lambd = Value('d', 1.5)
paused = Value('b', True)
lock = Lock()

from app import views, db