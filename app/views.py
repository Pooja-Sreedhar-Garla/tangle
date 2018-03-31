from flask import render_template

from . import app, db
from .models import Node, Edge


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/add/<int: algorithm>', methods=['POST'])
def add(algorithm):
    n = Node()
    db.session.add(n)
    db.session.commit()


    e1 = Edge(start_node=n.id, end_node=)
