import sys

from app import app, db, services, models
from multiprocessing import Process

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'createdb':
        db.drop_all()
        db.create_all()
        n = models.Node(weight=1)
        db.session.add(n)
        db.session.commit()

    else:
        models.Node.query.filter_by(weight=0).delete()
        db.session.commit()
        p1 = Process(target=services.generate_nodes)
        p2 = Process(target=services.update_graph)
        p1.start()
        p2.start()
        app.run()
