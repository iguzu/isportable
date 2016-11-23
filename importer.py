import csv
import os
from models import RateCenter

APP_ROOT = os.path.dirname(os.path.abspath(__file__))


def clear_data(app, db):
    with app.app_context():
        deleted = db.session.query(RateCenter).delete()
        db.session.commit()
    return 'Deleted %d existing rate center' % deleted


def import_data(app, db):
    with app.app_context():
        if RateCenter.query.count():
            return "Database not empty"
        reader = csv.reader(open(os.path.join(APP_ROOT,'footprint.csv')), delimiter=',',quotechar='"')
        results = list(filter(lambda x: x[4].strip() == 'Y',reader))
        count = 0
        for row in results:
            row = [ item.strip() for item in row ]
            rc = RateCenter()
            rc.state, rc.rate_center, rc.lata, rc.name, rc.coverage = row
            rc.coverage = True if rc.coverage == 'Y' else False
            db.session.add(rc)
            count += 1
            if not count % 100:
                print('committing... %d RateCenters' % count)
                db.session.commit()
                print('commit... Done')
        db.session.commit()
    return 'Done'


def create_all(app,db):
    with app.app_context():
        db.create_all()
    return 'Done'


def count(app):
    with app.app_context():
        return str(RateCenter.query.count())
