from database.models import Users
from app import db


def get_following(current_user):
    following = []
    users = Users.query.all()
    for user in users:
        if current_user.is_following(user):
            following.append(user.id)

    return following