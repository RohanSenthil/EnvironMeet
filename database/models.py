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

class Members(db.Model):

    __tablename__ = 'members'

    id = db.Column(db.Integer,db.Sequence('member_id_seq'))
    email = db.Column(db.String(100),db.Sequence('member_email_seq'),primary_key=True)
    name = db.Column(db.Text,db.Sequence('member_name_seq'))
    gender = db.Column(db.Boolean,db.Sequence('member_gender_seq'))
    contact = db.Column(db.Integer,db.Sequence('member_contact_seq'))

# class Organisations(db.Model):

#     __tablename__ = 'organisations'

dbevents = SQLAlchemy()

class Events(db.Model):

    __tablename__ = 'events'

    id = db.Column(db.Integer,db.Sequence('events_id_seq'),primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    date = db.Column(db.DateTime)
    location = db.Column(db.String(100))
    # image
    # associated event


