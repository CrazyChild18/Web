from datetime import datetime
from LiYunkai import db


class User(db.Model):
    username =db.Column(db.String, index=True, unique=True)
    email = db.Column(db.String, index=True, primary_key=True)
    password = db.Column(db.String, index=True)
    post = db.relationship('Post', backref='author', lazy='dynamic')
    personal = db.relationship('Personal', backref='user', lazy='dynamic')
    create = db.relationship('Algorithm', backref='create', lazy='dynamic')


class Post(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    comment = db.Column(db.String)
    create_date = db.Column(db.DateTime, default=datetime.now)
    post_id = db.Column(db.String, index=True)
    author_id = db.Column(db.String, db.ForeignKey(User.email))


class Personal(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    nickname = db.Column(db.String, index=True)
    fullname = db.Column(db.String, index=True)
    birthday = db.Column(db.String, index=True)
    presentation = db.Column(db.String, index=True)
    gender = db.Column(db.String, index=True)
    avatar = db.Column(db.String, index=True)
    country = db.Column(db.String(256), index=True)
    user_id = db.Column(db.String, db.ForeignKey(User.email))


class Algorithm(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.String, unique=True, index=True)
    code_pic = db.Column(db.String, index=True)
    theory = db.Column(db.String)
    complexity = db.Column(db.String)
    application = db.Column(db.String)
    user_id = db.Column(db.String, db.ForeignKey(User.email))
