import logging
import csv

from models import RateCenter

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db.init_app(app)

deleted = RateCenter.query.delete()
logging.info('Deleted %d existing rate center' % deleted)


with open('eggs.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        logging.info(row)


