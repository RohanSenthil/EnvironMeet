from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template
from sqlalchemy.orm import backref
from flask_login import UserMixin
from sqlalchemy import Enum

db = SQLAlchemy() # DB Handler

class Posts(db.Model):

    __tablename__ = 'posts'

    id = db.Column(db.Integer,db.Sequence('posts_id_seq'),primary_key=True)
    # profile_id = db.Column(db.Integer, db.ForeignKey('profiles.id'), nullable=False)
    date = db.Column(db.DateTime)
    desc = db.Column(db.Text())
    image = db.Column(db.String(140))
    # associated event

    def __init__(self, desc):
        self.desc = desc


class Profiles(db.Model):

    __tablename__ = 'profiles'

    id = db.Column(db.Integer,db.Sequence('profiles_id_seq'),primary_key=True)
    # posts = db.relationship('Posts', backref='profiles', lazy=True)

class Members(db.Model, UserMixin):

    __tablename__ = 'members'

    id = db.Column(db.Integer, db.Sequence('member_id_seq'), unique=True)
    email = db.Column(db.String(100),primary_key=True, unique=True)
    password = db.Column(db.String(10000))
    name = db.Column(db.String(100))
    gender = db.Column(db.Enum('Male','Female'))
    contact = db.Column(db.Integer)
    points = db.Column(db.Integer)
    yearlypoints = db.Column(db.Integer)
    profilepic = db.Column(db.String(140))
    #db.Column(db.,db.Sequence('member_events_seq'))

    # def __repr__(self):
    #     return f"<Member(id={self.id}, name='{self.name}', email='{self.email}')>"

class Organisations(db.Model, UserMixin):
    __tablename__ = 'organisations'

    id = db.Column(db.Integer, db.Sequence('org_id_seq'), unique=True)
    name = db.Column(db.String(100))
    address = db.Column(db.String(100))
    contact = db.Column(db.String(100))
    email = db.Column(db.String(100), primary_key = True, unique=True)
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


