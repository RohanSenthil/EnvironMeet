from database.models import db, Users
from flask import redirect, url_for, flash, session
from flask_login import logout_user
import app
from flask_socketio import emit


def flag_user(user_id):

    if user_id is not None:
        user = Users.query.get(user_id)

        if user is not None:
            times_flagged = user.flags
            times_flagged += 1

            user.flags = times_flagged
            db.session.commit()

            if times_flagged >= 5:
                user.is_locked = True
                user.set_inactive()
                db.session.commit()
                logout_user()

                # revoke_login_token()
                session.pop('user_id', None)
                session.pop('last_activity', None)
                flash('Account locked due to suspicious activity')
                try:
                    emit('flag')
                except Exception as e:
                    print(e)
                    return redirect(url_for('login_'))
