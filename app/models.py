from app import db, manager
from flask_login import UserMixin
import datetime


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(128), nullable=False, unique=True)
    psw = db.Column(db.Text, nullable=False)
    opinions = db.relationship('Opinion', backref='author')

    def __repr__(self):
        return f'<Users {self.title}>'


class Opinion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime,
                     default=datetime.datetime.now)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<Opinions {self.title}>'


@manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
