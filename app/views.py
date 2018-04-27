import json

from collections import Counter
from flask import render_template, request, jsonify, session

from . import app, db, node_queue, paused, lambd, alpha, lock
from .models import Node, Edge
from .services import serialize


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get_graph')
def get_graph():
    if 'timestamp' not in session:
        session['depth_counts'] = '{}'

    depth_counts = json.loads(session['depth_counts'], object_hook=Counter)
    nodes = Node.query.filter(Node.timestamp > request.args.get('timestamp', 0))
    edges = Edge.query.filter(Node.timestamp > request.args.get('timestamp', 0))

    serialized = jsonify(serialize(nodes, edges, depth_counts))
    session['depth_counts'] = json.dumps(depth_counts)
    return serialized


@app.route('/add', methods=['POST'])
def add():
    n = Node(user_created=True)
    lock.acquire()
    db.session.add(n)
    db.session.commit()
    node_queue.put(n.id)
    lock.release()

    return ''


@app.route('/get-alpha-lambda')
def get_alpha_lambda():
    return jsonify({'alpha': alpha.value, 'lambd': lambd.value})


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
    while not node_queue.empty():
        node_queue.get()

    lock.release()
    return ''
