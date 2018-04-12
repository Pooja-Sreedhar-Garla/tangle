from app import db


class Node(db.Model):
    __tablename__ = 'node'

    id = db.Column(db.Integer, primary_key=True)
    weight = db.Column(db.Integer, default=0)
    parents = db.relationship('Edge', foreign_keys='Edge.end_id', back_populates='start_node')
    children = db.relationship('Edge', foreign_keys='Edge.start_id', back_populates='end_node')
    user_created = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<Node %r, %r>' % (self.id, self.weight)


class Edge(db.Model):
    __tablename__ = 'edge'

    start_id = db.Column(db.Integer, db.ForeignKey('node.id'), primary_key=True)
    end_id = db.Column(db.Integer, db.ForeignKey('node.id'), primary_key=True)
    start_node = db.relationship('Node', primaryjoin='Edge.start_id == Node.id', back_populates='parents')
    end_node = db.relationship('Node', primaryjoin='Edge.end_id == Node.id', back_populates='children')

    def __repr__(self):
        return '<Edge %r -> %r>' % (self.start_node, self.end_node)


if __name__ == '__main__':
    print(Node.query.all())
    print(Edge.query.all())