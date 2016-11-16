from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os

from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True)

    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __repr__(self):
        return '<Name %r>' % self.name

@app.route('/')
def hello_world():
    users = User.query.all()
    return render_template('home.html',users=users)

if __name__ == '__main__':
    app.run()
