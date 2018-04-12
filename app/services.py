import math
import time
import random

from . import db, node_queue, alpha, lambd, paused, lock
from .models import Node, Edge


def weighted_random_walk():
    cur = Node.query.get(1)
    while cur.parents:
        nodes = list()
        weights = list()

        for edge in cur.parents:
            nodes.append(edge.start_node)
            weights.append(edge.start_node.weight)

        max_weight = max(weights)
        weights = [math.exp(alpha.value * (x - max_weight)) for x in weights]
        total_weight = sum(weights)
        random_weight = random.random() * total_weight

        for i in range(len(weights)):
            random_weight -= weights[i]
            if i <= 0:
                cur = nodes[i]
                break

    return cur


def update_graph():

    while True:
        time.sleep(0.8)
        lock.acquire()
        if not paused.value:
            nodes = list()
            approvees = list()
            while not node_queue.empty():
                nodes.append(node_queue.get())

            for _ in nodes:
                approvees.append((weighted_random_walk(), weighted_random_walk()))

            for node_id, approvee in zip(nodes, approvees):
                edge = Edge(start_id=node_id, end_id=approvee[0].id)
                db.session.add(edge)

                if approvee[0].id != approvee[1].id:
                    edge = Edge(start_id=node_id, end_id=approvee[1].id)
                    db.session.add(edge)

                visited = set()
                stack = [Node.query.get(node_id)]
                while stack:
                    cur = stack.pop()
                    if cur.id not in visited:
                        visited.add(cur.id)
                        cur.weight += 1
                        db.session.add(cur)
                        for i in cur.children:
                            if i.end_id not in visited:
                                stack.append(i.end_node)

            db.session.commit()

        lock.release()


def generate_nodes():
    while True:
        time.sleep(1.0 / lambd.value)
        node = Node()
        lock.acquire()
        db.session.add(node)
        db.session.commit()
        node_queue.put(node.id)
        lock.release()
