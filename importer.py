import logging
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
        csvfile = open(os.path.join(APP_ROOT,'footprint.csv'))
        reader = csv.reader(csvfile, delimiter=',',quotechar='"')
        count = 0
        results = list(filter(lambda x: x[4].strip() == 'Y',reader))
        for row in results:
            state, rate_center, lata, name, coverage = row
            state = state.strip()
            rated_center = rate_center.strip()
            lata = lata.strip()
            name = name.strip()
            coverage = coverage.strip()
            rc = RateCenter()
            rc.state = state
            rc.rate_center = rate_center
            rc.name = name
            rc.lata = lata
            rc.coverage = True if coverage == 'Y' else False
            db.session.add(rc)
            count = count + 1
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


def count(app,db):
    with app.app_context():
        return str(RateCenter.query.count())
