from flask import render_template, request, jsonify

from . import app, db, node_queue, paused, lambd, alpha, lock
from .models import Node, Edge


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get_graph')
def get_graph():
    nodes = [node.id for node in Node.query.all()]
    edges = [[edge.start_id, edge.end_id] for edge in Edge.query.all()]
    return jsonify({'nodes': nodes, 'edges': edges})


@app.route('/add', methods=['POST'])
def add():
    n = Node(user_created=True)
    lock.acquire()
    db.session.add(n)
    db.session.commit()
    node_queue.put(n)
    lock.release()

    return ''


@app.route('/update-alpha', methods=['POST'])
def update_alpha():
    alpha.value = float(request.form['alpha'])
    return ''


@app.route('/update-lambda', methods=['POST'])
def update_lambda():
    lambd.value = float(request.form['lambd'])
    return ''


@app.route('/pause', methods=['POST'])
def pause():
    paused.value = not paused.value
    return ''


@app.route('/reset', methods=['POST'])
def reset():
    lock.acquire()
    paused.value = True
    db.drop_all()
    db.create_all()
    node = Node(weight=1)
    db.session.add(node)
    db.session.commit()
    lock.release()
