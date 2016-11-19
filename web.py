import os
from flask import Flask, render_template, request, redirect, url_for
from models import db, RateCenter
from importer import clear_data, import_data, create_all
import urllib.request
from bs4 import BeautifulSoup
import re

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db.init_app(app)

@app.route('/')
def hello_world():
    return render_template('home.html')

@app.route('/clear')
def clear_handler():
    return clear_data(db)

@app.route('/count')
def count_handler():
    return str(RateCenter.query.count())

@app.route('/import')
def import_handler():
    return import_data(db)


@app.route('/create_all')
def create_all_handler():
    create_all(db)
    return 'Done'

@app.route('/lookup',methods=['POST'])
def lookup_handler():
    results = []
    phonenumbers = request.form['phonenumbers'].strip().translate({ord(i):None for i in '()-. pw#'})
    phonenumbers = re.findall(r'[^,;\s]+', phonenumbers)
    phonenumbers = list(filter(lambda x: len(x), phonenumbers))
    if len(phonenumbers) > 10:
        return 'Maximum of 10 phone numbers per lookup'
    for tn in phonenumbers:
        if len(tn) != 10:
            results.append({'number': tn, 'result': 'Invalid Number'})
        else:
            found = 0
            content = urllib.request.urlopen("http://localcallingguide.com/lca_prefix.php?npa=%s&nxx=%s" % (tn[0:3],tn[3:6])).read()
            soup = BeautifulSoup(content, 'html.parser')
            tds = soup.find_all('td',{'data-label':"Rate centre"})
            lookup = [item.text.strip().upper() for item in tds]
            for item in lookup:
                found += RateCenter.query.filter(RateCenter.rate_center == item).count()
            results.append({'number': tn, 'result': 'Portable' if found else 'Not portable'})
    return render_template('lookup_result.html',results=results)

if __name__ == '__main__':
    app.run()
