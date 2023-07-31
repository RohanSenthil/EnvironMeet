from flask_login import current_user
from flask import request, render_template, redirect, url_for, flash
from functools import wraps
from flask.json import jsonify
from database.models import Members, Organisations, db, Users, Admins

def check_is_confirmed(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.is_confirmed == False:
            flash("Please confirm your account!", "warning")
            return redirect(url_for("userprofile"))
        return func(*args, **kwargs)

    return decorated_function

def admin_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if isinstance(current_user, Admins):
            return func(*args, **kwargs)
        else:
            return jsonify({'error': 'Unallowed'}), 403
    return decorated_function