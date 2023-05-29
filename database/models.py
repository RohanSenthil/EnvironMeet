from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template
from sqlalchemy.orm import backref

db = SQLAlchemy() # DB Handler

class Posts(db.Model):

    __tablename__ = 'posts'

    id = db.Column(db.Integer,db.Sequence('posts_id_seq'),primary_key=True)
    # profile_id = db.Column(db.Integer, db.ForeignKey('profiles.id'), nullable=False)
    timestamp = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
    desc = db.Column(db.Text())
    # image
    # associated event

    def __init__(self, desc):
        self.desc = desc


class Profiles(db.Model):

    __tablename__ = 'profiles'

    id = db.Column(db.Integer,db.Sequence('profiles_id_seq'),primary_key=True)
    # posts = db.relationship('Posts', backref='profiles', lazy=True)

# class Member(db.Model):

#     __tablename__ = 'member'

#     id = db.Column(db.Integer,db.Sequence('member_id_seq'),primary_key=True)
#     email = db.Column()
#     posts = db.relationship('Posts', backref='profiles', lazy=True)


dbevents = SQLAlchemy()

class Events(db.Model):

    __tablename__ = 'events'

    id = dbevents.Column(db.Integer, primary_key = True)
    title = dbevents.Column(db.String(100), nullable=False)
    description = dbevents.Column(db.Text)
    date = dbevents.Column(db.DateTime)
    location = db.Column(db.String(100))
    # image
    # associated event
