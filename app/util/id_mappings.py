import hashlib
import uuid
from database.models import Id_Hash_Mappings, Users, Events, SignUps, Leaderboard, LeaderboardContent
from app import db


# Normal Mappings
def get_user_from_id(user_id):
    user = Users.query.get(user_id)
    return user


def get_event_from_id(event_id):
    events = Events.query.get(event_id)
    return events

def get_signups_from_id(signup_id):
    signups = SignUps.query.get(signup_id)
    return signups

def get_leaderboard_from_id(leaderboard_id):
    leaderboard = Leaderboard.query.get(leaderboard_id)
    return leaderboard

def get_leadeerboardcontent_from_id(leaderboardcontent_id):
    leaderboardcontent = LeaderboardContent.query.get(leaderboardcontent_id)
    return leaderboardcontent

# Security
def gen_salt():
    return uuid.uuid4().hex


def hash_object_id(object_id, act):
    salted_value = str(object_id).encode() + gen_salt().encode() + str(act).encode()
    hash_object = hashlib.sha256(salted_value)
    return hash_object.hexdigest()


def store_id_mapping(object_id, hashed_value, act):
    new_object_id = act + '-' + str(object_id)
    mapping = Id_Hash_Mappings(object_id=new_object_id, hashed_value=hashed_value)
    db.session.add(mapping)
    db.session.commit()


def delete_id_mapping(hashed_value):
    mapping = Id_Hash_Mappings.query.filter_by(hashed_value=hashed_value).first()
    if mapping is not None:
        db.session.delete(mapping)
        db.session.commit()

def hash_to_object_id(hashed_value):
    mapping = Id_Hash_Mappings.query.filter_by(hashed_value=hashed_value).first()
    if mapping is None:
        return None
    else:
        return (mapping.object_id).split('-')[1]
    

def object_id_to_hash(object_id, act):
    new_object_id = act + '-' + str(object_id)
    mapping = Id_Hash_Mappings.query.filter_by(object_id=new_object_id).first()
    if mapping is None:
        return None
    else:
        return mapping.hashed_value
    