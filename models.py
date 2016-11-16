from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class RateCenters(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(2))
    rate_center = db.Column(db.String(64))
    lata = db.Column(db.String(3))
    name = db.Column(db.String(64))
    coverage = db.Column(db.Boolean())