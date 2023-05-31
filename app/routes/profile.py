from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
# from app.routes.helpers import privileged_route
from flask_mail import Message
from threading import Thread
from flask import request, render_template, redirect, url_for, flash
from app import app
from database.models import Members, Organisations, db
from app.forms.accountsform import createm, updatem


@app.route('/profile')
#@login_required
def profile():
    # if not current_user.is_authenticated:
        # loginmanager.login_message = "Please login to access this page"
        # loginmanager.login_message_category = "warning"
    return render_template('/accounts/profile/memprofile.html', name=current_user.name)