from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True)
    name = db.Column(db.String)
    password_hash = db.Column(db.String())
    age = db.Column(db.Integer)
    sex = db.Column(db.String(10))
    about_me = db.Column(db.String)
    posts = db.relationship('Post')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.email}>'


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String)
    date_created = db.Column(db.DateTime)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship('User')

    def __repr__(self):
        return f'<Post text={self.text}>'


