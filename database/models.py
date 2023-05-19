from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref

db = SQLAlchemy() # Our DB Handler

class Posts(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer,
                   db.Sequence('posts_id_seq'),
                   primary_key=True)
    
    # profile_id = db.Column(db.Integer,
    #                        db.ForeignKey('profiles.id'),
    #                        nullable=False)
    
    timestamp = db.Column(db.DateTime,
                          server_default=db.func.now(),
                          onupdate=db.func.now())
    
    text = db.Column(db.Text())


    def __init__(self, text):
        self.text = text

    # For profile class
    # posts = db.relationship('Posts',
    #                           backref='profiles',
    #                           lazy=True)