from flask_sqlalchemy import SQLAlchemy
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