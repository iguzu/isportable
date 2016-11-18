import os
from flask import Flask, render_template, request, redirect, url_for
from models import db, RateCenter
from importer import clear_data, import_data, create_all
import urllib.request
from bs4 import BeautifulSoup

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
    phonenumber = request.form['phonenumber'].strip()
    if len(phonenumber) != 10:
        return 'Invalid Number'
    else:
        found = 0
        content = urllib.request.urlopen("http://localcallingguide.com/lca_prefix.php?npa=%s&nxx=%s" % (phonenumber[0:3],phonenumber[3:6])).read()
        soup = BeautifulSoup(content, 'html.parser')
        tds = soup.find_all('td',{'data-label':"Rate centre"})
        lookup = [ele.text.strip().upper() for ele in tds]
        for item in lookup:
            found += RateCenter.query.filter(RateCenter.rate_center == item).count()
        return 'Portable' if found else 'Not portable'

if __name__ == '__main__':
    app.run()
