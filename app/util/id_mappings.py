import hashlib
import uuid
from database.models import Id_Hash_Mappings
from app import db


def gen_salt():
    return uuid.uuid4().hex


def hash_object_id(object_id):
    salted_value = str(object_id).encode() + gen_salt().encode()
    hash_object = hashlib.sha256(salted_value)
    return hash_object.hexdigest()


def store_hashed_value(object_id, hashed_value):
    mapping = Id_Hash_Mappings(object_id=object_id, hashed_value=hashed_value)
    db.session.add(mapping)
    db.session.commit()


def hash_to_object_id(hashed_value):
    mapping = Id_Hash_Mappings.query.filter_by(hashed_value=hashed_value).first()
    if mapping is None:
        return False
    else:
        return mapping.object_id
    

def object_id_to_hash(object_id):
    mapping = Id_Hash_Mappings.query.filter_by(object_id=object_id).first()
    if mapping is None:
        return False
    else:
        return mapping.hashed_value