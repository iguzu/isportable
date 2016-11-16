import logging
import csv

from models import RateCenters

deleted = RateCenters.query.delete()
logging.info('Deleted %d existing rate center' % deleted)


with open('eggs.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        logging.info(row)


