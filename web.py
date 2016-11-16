from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os

from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)


@app.route('/')
def hello_world():

    return render_template('home.html')

if __name__ == '__main__':
    app.run()
