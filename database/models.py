from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template
from sqlalchemy.orm import backref
from flask_login import UserMixin
from sqlalchemy import Enum
import app
import jwt
import datetime

db = SQLAlchemy() # DB Handler

class Posts(db.Model):

    __tablename__ = 'posts'

    id = db.Column(db.Integer,db.Sequence('posts_id_seq'),primary_key=True)
    # author = db.Column(db.Integer, db.ForeignKey('profiles.id', ondelete='CASCADE'), nullable=False)
    timestamp = db.Column(db.DateTime(timezone=True), server_default=db.func.now(), onupdate=db.func.now())
    desc = db.Column(db.Text(), nullable=False)
    image = db.Column(db.String(140))
    comments = db.relationship('Comments', backref='posts', cascade='all, delete, delete-orphan', lazy=True, passive_deletes=True)
    likes = db.relationship('Likes', backref='posts', cascade='all, delete, delete-orphan', lazy=True, passive_deletes=True)
    # associated event

    def __init__(self, desc):
        self.desc = desc


class Comments(db.Model):

    __tablename__ = 'comments'

    id = db.Column(db.Integer, db.Sequence('comments_id_seq'), primary_key=True)
    text = db.Column(db.Text(), nullable=False)
    time = db.Column(db.DateTime(timezone=True), default=db.func.now())
    author = db.Column(db.Integer, db.ForeignKey('profiles.id', ondelete='CASCADE'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id', ondelete='CASCADE'), nullable=False)

    def __init__(self, text, post_id):
        # self.author = author
        self.text = text
        self.post_id = post_id

class Likes(db.Model):

    __tablename__ = 'likes'

    id = db.Column(db.Integer, db.Sequence('likes_id_seq'), primary_key=True)
    time = db.Column(db.DateTime(timezone=True), default=db.func.now())
    # author = db.Column(db.Integer, db.ForeignKey('profiles.id', ondelete='CASCADE'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id', ondelete='CASCADE'), nullable=False)

    def __init__(self, post_id):
        # self.author = author
        self.post_id = post_id

class Profiles(db.Model):

    __tablename__ = 'profiles'

    id = db.Column(db.Integer,db.Sequence('profiles_id_seq'),primary_key=True)
    # posts = db.relationship('Posts', backref='profiles', lazy=True)

class Members(db.Model, UserMixin):

    __tablename__ = 'members'

    id = db.Column(db.Integer, db.Sequence('member_id_seq'), primary_key=True, unique=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(10000))
    name = db.Column(db.String(100))
    gender = db.Column(db.Enum('Male','Female'))
    contact = db.Column(db.Integer)
    points = db.Column(db.Integer)
    yearlypoints = db.Column(db.Integer)
    profilepic = db.Column(db.String(140))

    def get_reset_token(self, expires_sec=1800):
        reset_token = jwt.encode(
            payload=
            {
                "user_id": self.id,
                "exp": datetime.datetime.now(tz=datetime.timezone.utc)
                       + datetime.timedelta(seconds=expires_sec)
            },
            key = app.app.config['SECRET_KEY'],
            algorithm="HS256"
        )
        return reset_token

    def verify_reset_token(token):
        try:
            userid = jwt.decode(token, key = app.app.config['SECRET_KEY'], leeway=datetime.timedelta(seconds=10), algorithms=['HS256', ])["user_id"]
        except:
            return None
        return Members.query.filter_by(id=userid).first()
    
    def get_id(self):
        return self.email
    #db.Column(db.,db.Sequence('member_events_seq'))

    # def __repr__(self):
    #     return f"<Member(id={self.id}, name='{self.name}', email='{self.email}')>"

class Organisations(db.Model, UserMixin):
    __tablename__ = 'organisations'

    id = db.Column(db.Integer, db.Sequence('org_id_seq'), unique=True, primary_key = True)
    name = db.Column(db.String(100))
    address = db.Column(db.String(100))
    contact = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    description = db.Column(db.Text)
    mainpic = db.Column(db.String(140))
    #events

    # def __repr__(self):
    #     return f"<Organization(id={self.id}, name='{self.name}', address='{self.address}', contact='{self.contact}')>"

class Events(db.Model):

    __tablename__ = 'eventsda'

    id = db.Column(db.Integer, db.Sequence('events_id_seq'), primary_key=True)
    organiser = db.Column(db.String(100))
    name = db.Column(db.String(100))
    date = db.Column(db.Text)
    price = db.Column(db.Text)
    # price = db.Column(db.Price)
    # image
    # associated event

    def __init__(self, organiser, name, date, price):
        self.organiser = organiser
        self.name = name
        self.date = date
        self.price = price

class Leaderboard(db.Model):
    __tablename__ = 'leaderboard'

    id = db.Column(db.Integer, db.Sequence('member_id_seq'), primary_key = True)
    url = db.Column(db.String(100))
    name = db.Column(db.String(20))
