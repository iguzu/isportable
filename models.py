from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class RateCenter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(2))
    rate_center = db.Column(db.String(64))
    lata = db.Column(db.String(3))
    name = db.Column(db.String(64))
    coverage = db.Column(db.Boolean())


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True)

    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __repr__(self):
        return '<Name %r>' % self.name
