from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import os

db = SQLAlchemy()

class RateCenter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(2))
    rate_center = db.Column(db.String(64))
    lata = db.Column(db.String(5))
    name = db.Column(db.String(64))
    coverage = db.Column(db.Boolean())


