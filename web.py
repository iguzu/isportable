import os
from flask import Flask, render_template, request, redirect, url_for
from models import db, RateCenter
import urllib.request
from bs4 import BeautifulSoup
import re

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db.init_app(app)


@app.route('/')
def home():
    return render_template('home.html')


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
            lookup = []
            content = urllib.request.urlopen("http://localcallingguide.com/lca_prefix.php?npa=%s&nxx=%s" % (tn[0:3],tn[3:6])).read()
            soup = BeautifulSoup(content, 'html.parser')
            table = soup.find('tbody')
            rows = table.find_all('tr')
            for row in rows:
                center =row.find('td',{'data-label': "Rate centre"})
                region = row.find('td', {'data-label': "Region"})
                lookup.append({'ratecenter':center.text.strip().upper(), 'region':region.text.strip().upper()})
            print(repr(lookup))
            for item in lookup:
                found += RateCenter.query.filter(RateCenter.rate_center == item['ratecenter']).filter(RateCenter.state == item['region']).count()
            results.append({'number': tn, 'result': 'Portable' if found else 'Not portable'})
    return render_template('lookup_result.html',results=results)


if __name__ == '__main__':
    app.run()
