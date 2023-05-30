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
    image = db.Column(db.String(140))
    # associated event

    def __init__(self, desc):
        self.desc = desc


class Profiles(db.Model):

    __tablename__ = 'profiles'

    id = db.Column(db.Integer,db.Sequence('profiles_id_seq'),primary_key=True)
    # posts = db.relationship('Posts', backref='profiles', lazy=True)

class Members(db.Model):

    __tablename__ = 'members'

    id = db.Column(db.Integer,db.Sequence('member_id_seq'), unique=True)
    email = db.Column(db.String(100),db.Sequence('member_email_seq'),primary_key=True, unique=True)
    password = db.Column(db.String(100),db.Sequence('member_password_seq'))
    name = db.Column(db.String(100),db.Sequence('member_name_seq'))
    gender = db.Column(db.Enum('Male','Female'),db.Sequence('member_gender_seq'))
    contact = db.Column(db.Integer,db.Sequence('member_contact_seq'))
    points = db.Column(db.Integer,db.Sequence('member_points_seq'))
    #db.Column(db.,db.Sequence('member_events_seq'))

    # def __repr__(self):
    #     return f"<Member(id={self.id}, name='{self.name}', email='{self.email}')>"

class Organisations(db.Model):
    __tablename__ = 'organisations'

    id = db.Column(db.Integer, db.Sequence('org_id_seq'), primary_key=True)
    name = db.Column(db.String(100),db.Sequence('org_name_seq'))
    address = db.Column(db.String(100),db.Sequence('org_address_seq'))
    contact = db.Column(db.String(100),db.Sequence('org_contact_seq'))
    email = db.Column(db.String(100),db.Sequence('org_email_seq'))
    password = db.Column(db.String(100),db.Sequence('org_password_seq'))
    #events

    # def __repr__(self):
    #     return f"<Organization(id={self.id}, name='{self.name}', address='{self.address}', contact='{self.contact}')>"

dbevents = SQLAlchemy()

class Events(db.Model):

    __tablename__ = 'events'

    id = db.Column(db.Integer,db.Sequence('events_id_seq'),primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    datetime = db.Column(db.DateTime)
    # price = db.Column(db.Price)
    organiser = db.Column(db.String(100))
    # image
    # associated event


