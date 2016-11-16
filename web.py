import os
from flask import Flask, render_template
from models import db, RateCenter, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db.init_app(app)


@app.route('/')
def hello_world():
    users = User.query.all()
    return render_template('home.html',users=users)

if __name__ == '__main__':
    app.run()
