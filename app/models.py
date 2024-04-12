from app import db, manager
from flask_login import UserMixin
import datetime


class Opinion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime,
                     default=datetime.datetime.now)

    def __repr__(self):
        return f'<opinions {self.title}>'


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(128), nullable=False, unique=True)
    psw = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<users {self.title}>'


@manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
