from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template
from sqlalchemy.orm import backref
from flask_login import UserMixin
from sqlalchemy import Enum
from app import app
import datetime
from sqlalchemy.ext.declarative import declarative_base
from itsdangerous import URLSafeTimedSerializer as Serializer, SignatureExpired
import jwt
import app

Base = declarative_base()

db = SQLAlchemy() # DB Handler

class Posts(db.Model):

    __tablename__ = 'posts'

    id = db.Column(db.Integer,db.Sequence('posts_id_seq'),primary_key=True)
    author = db.Column(db.Integer, db.ForeignKey('members.user_id', ondelete='CASCADE'), nullable=False)
    timestamp = db.Column(db.DateTime(timezone=True), server_default=db.func.now(), onupdate=db.func.now())
    desc = db.Column(db.Text(), nullable=False)
    image = db.Column(db.String(140))
    comments = db.relationship('Comments', backref='posts', cascade='all, delete, delete-orphan', lazy=True, passive_deletes=True)
    likes = db.relationship('Likes', backref='posts', cascade='all, delete, delete-orphan', lazy=True, passive_deletes=True)
    # associated event

    def __init__(self, author, desc):
        self.author = author
        self.desc = desc


class Comments(db.Model):

    __tablename__ = 'comments'

    id = db.Column(db.Integer, db.Sequence('comments_id_seq'), primary_key=True)
    text = db.Column(db.Text(), nullable=False)
    time = db.Column(db.DateTime(timezone=True), default=db.func.now())
    author = db.Column(db.Integer, db.ForeignKey('members.user_id', ondelete='CASCADE'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id', ondelete='CASCADE'), nullable=False)

    def __init__(self, author, text, post_id):
        self.author = author
        self.text = text
        self.post_id = post_id

class Likes(db.Model):

    __tablename__ = 'likes'

    id = db.Column(db.Integer, db.Sequence('likes_id_seq'), primary_key=True)
    time = db.Column(db.DateTime(timezone=True), default=db.func.now())
    author = db.Column(db.Integer, db.ForeignKey('members.user_id', ondelete='CASCADE'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id', ondelete='CASCADE'), nullable=False)

    def __init__(self, author, post_id):
        self.author = author
        self.post_id = post_id

class Profiles(db.Model):

    __tablename__ = 'profiles'

    id = db.Column(db.Integer,db.Sequence('profiles_id_seq'),primary_key=True)
    # posts = db.relationship('Posts', backref='profiles', lazy=True)

followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('users.id'))
)

class Users(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    username = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(100), unique=True, default='mail@example.com')
    password = db.Column(db.String(10000))
    name = db.Column(db.String(100))
    is_confirmed = db.Column(db.Boolean, nullable=False, default=False)
    profile_pic = db.Column(db.String(1000), nullable=True)
    followed = db.relationship('Users', 
                               secondary=followers, 
                               primaryjoin=(followers.c.follower_id == id), 
                               secondaryjoin=(followers.c.followed_id == id), 
                               backref=db.backref('followers', lazy='dynamic'), 
                               lazy='dynamic')
    
    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
            return self

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)
            return self

    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        return Posts.query.join(followers, (followers.c.followed_id == Posts.author)).filter(followers.c.follower_id == self.id).order_by(Posts.timestamp.desc())
    
    discriminator = db.Column(db.String(50))
    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': discriminator
    }
    '''
    def get_reset_token(self, expires_sec=300):
        serial = Serializer(app.config['SECRET_KEY'])
        expires_in = datetime.utcnow() + timedelta(seconds=expires_sec)
        token = serial.dumps({'user_id': self.id})
        return token, expires_in
    
    @staticmethod
    def verify_reset_token(token):
        serial = Serializer(app.config['SECRET_KEY'])
        try:
            data = serial.loads(token)
            user_id = data['user_id']
            expires_in = data.get('expires_in')  # Optional: If you've updated the get_reset_token method to return expires_in
            if expires_in and datetime.utcnow() > expires_in:
                # Token has expired
                return None
            return Users.query.get(user_id)
        except SignatureExpired:
            # Token has expired
            return None
    
    '''
    def get_reset_token(self, expires_sec=300):
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
        return Users.query.filter_by(id=userid).first()

class Members(Users):

    __tablename__ = 'members'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    gender = db.Column(db.Enum('Male','Female'))
    contact = db.Column(db.Integer)
    points = db.Column(db.Integer)
    yearlypoints = db.Column(db.Integer)

    __mapper_args__ = {
        'polymorphic_identity': 'member',
    }

    #db.Column(db.,db.Sequence('member_events_seq'))

    def __repr__(self):
        return f"<Member(id={self.id}, name='{self.name}', email='{self.email}')>"

class Organisations(Users):
    __tablename__ = 'organisations'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    address = db.Column(db.String(100))
    contact = db.Column(db.String(100))
    description = db.Column(db.Text)
    # events

    __mapper_args__ = {
        'polymorphic_identity': 'organisation',
    }

    def __repr__(self):
        return f"<Organization(id={self.id}, name='{self.name}', address='{self.address}', contact='{self.contact}')>"

class Events(db.Model):

    __tablename__ = 'events3'

    id = db.Column(db.Integer, db.Sequence('events_id_seq'), primary_key=True)
    organiser = db.Column(db.String(100))
    name = db.Column(db.String(100))
    date = db.Column(db.Text)
    time = db.Column(db.Text)
    price = db.Column(db.Text)
    points = db.Column(db.Integer)
    image = db.Column(db.String(140))
    # price = db.Column(db.Price)
    # image
    # associated event

    def __init__(self, organiser, name, date, time, price, points, image):
        self.organiser = organiser
        self.name = name
        self.date = date
        self.time = time
        self.price = price
        self.points = points
        self.image = image

class SignUps(db.Model):

    __tablename__ = 'signups2'

    id = db.Column(db.Integer, db.Sequence('eventssignup_id_seq'), unique=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), primary_key=True, unique=True)
    eventname = db.Column(db.Enum('events3.name'))
    # eventname = db.Column(db.String(300))
    # price = db.Column(db.Price)
    # image
    # associated event

    def __init__(self, name, email, eventname):
        self.name = name
        self.email = email
        self.eventname = eventname

class Attendance(db.Model):

    __tablename__ = 'attendance'

    id = db.Column(db.Integer, db.Sequence('attendance_id_seq'), unique=True, primary_key = True)
    event = db.Column(db.Integer, db.ForeignKey('events3.id'), nullable=False)
    member = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, event, member):
        self.event = event
        self.member = member



class Leaderboard(db.Model):
    __tablename__ = 'leaderboard'

    id = db.Column(db.Integer, db.Sequence('leaderboard_id_seq'), primary_key = True, unique=True)
    name = db.Column(db.String(20))
    desc = db.Column(db.String(20))
    username = db.Column(db.String(20))


class Id_Hash_Mappings(db.Model):

    __tablename__ = 'id_hash_mappings'

    id = db.Column(db.Integer,db.Sequence('mappings_id_seq'),primary_key=True)
    object_id = db.Column(db.String(256), unique=True)
    hashed_value = db.Column(db.String(256), unique=True)

    def __init__(self, object_id, hashed_value):
        self.object_id = object_id
        self.hashed_value = hashed_value


# class RateLimit(db.Model):

#     __tablename__ = 'rate_limit'

#     id = db.Column(db.Integer,db.Sequence('rate_limit_id_seq'),primary_key=True)
#     endpoint = db.Column(db.String(255), nullable=False)
#     ip = db.Column(db.String(45), nullable=False)
#     limit = db.Column(db.String(100), nullable=False)
#     period = db.Column(db.String(10), nullable=False)
#     last_hit = db.Column(db.DateTime, nullable=False)