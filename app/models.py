from app import db


class Node(db.Model):
    __tablename__ = 'node'

    id = db.Column(db.Integer, primary_key=True)
    weight = db.Column(db.Integer, default=0)
    next_nodes = db.relationship('Node', foreign_keys='Edge.end_node')

    def __repr__(self):
        return '<Node %r>' % self.id


class Edge(db.Model):
    __tablename__ = 'edge'

    id = db.Column(db.Integer, primary_key=True)
    start_node = db.Column(db.Integer, db.ForeignKey('node.id'), nullable=False)
    end_node = db.Column(db.Integer, db.ForeignKey('node.id'), nullable=False)

    def __repr__(self):
        return '<Edge %r -> %r>' % (self.start_node, self.end_node)


if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    node1 = Node()
    node2 = Node()
    node3 = Node()
    db.session.add(node1)
    db.session.add(node2)
    db.session.add(node3)
    db.session.commit()
    edge1 = Edge(start_node=2, end_node=1)
    edge2 = Edge(start_node=3, end_node=1)
    db.session.add(edge1)
    db.session.add(edge2)
    db.session.commit()
    n = Node.query.get(1)
    print(n)
    print(n.next_nodes)