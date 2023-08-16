from flask_login import UserMixin, login_user, login_required, logout_user, current_user
# from app.routes.helpers import privileged_route
from flask_mail import Message
from threading import Thread
from flask import request, render_template, redirect, url_for, flash, Flask, session
from app import app, loginmanager, mail, imagekit, csrf
from database.models import Members, Organisations, db, Users, followers, Posts, Admins
from app.forms.accountsform import createm, updatem, login, forget, reset, createo, updateo, getotp
from app.routes.helpers import revoke_login_token, provide_new_login_token
import bcrypt, pyotp, time, datetime
from werkzeug.utils import secure_filename
import uuid as uuid
import os, datetime
from datetime import datetime, timedelta
from app.util import share, validation, id_mappings, verification
from PIL import Image
from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions
from flask.json import jsonify
from app.util.verification import check_is_confirmed, reset_required
from flask_wtf.csrf import generate_csrf
from app.util.rate_limiting import limiter


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def userprofile():
    numposts = 0
    followers = 0
    numfollowing = 0
    profile_pic = None
    member = False
    organisation = False
    posts = []
    following = []  # Initialize 'following' with an empty list
    if not current_user.is_authenticated:
        loggedout = True
    else:
        loggedout = False

        if isinstance(current_user, Members):
            member = True
        elif isinstance(current_user, Organisations):
            organisation = True

        for i in Posts.query.filter_by(author=current_user.id):
            numposts += 1
            posts.append(i)
        for i in Users.query.all():
            if i.is_following(current_user):
                followers += 1
        for i in Users.query.all():
            if current_user.is_following(i):
                numfollowing += 1
        following = [user.id for user in current_user.followed.all()]
        profile_pic = current_user.profile_pic
    return render_template('userprofile.html', current_user=current_user, loggedout=loggedout, numposts=numposts, followers=followers, following=following, profile_pic=profile_pic, member=member, organisation=organisation, posts=posts, object_id_to_hash=id_mappings.object_id_to_hash, get_user_from_id=id_mappings.get_user_from_id, numfollowing=numfollowing, get_event_from_id=id_mappings.get_event_from_id)

@app.route('/update', methods=['GET','POST'])
@login_required
def profileupdate():
    if not current_user.is_authenticated:
        loggedout = True
    else:
        loggedout = False
        member = False
        organisation = False
        olduser = Users.query.get(current_user.id)
        if isinstance(current_user, Members):
            member = True
            updateform = updatem(request.form)
            if request.method == "POST" and updateform.validate():
                name = request.form['name']
                username = request.form['username']
                gender = request.form['gender']
                contact = request.form['contact']
                profile_pic = request.files['profile_pic']
                if profile_pic.filename == None or profile_pic.filename == '':
                    updateform.profile_pic.data = olduser.profile_pic
                else:
                    pic_filename = secure_filename(profile_pic.filename)
                    pic_name1 = str(uuid.uuid1()) + "_" + pic_filename
                    profile_pic.save(os.path.join(app.config['UPLOAD_FOLDER'], pic_name1))
                    pic_name =  "static/uploads/" + pic_name1
                    olduser.profile_pic = pic_name
                olduser.name = name
                olduser.username = username
                olduser.gender = gender
                olduser.contact = contact

                db.session.commit()
                db.session.close()

                return redirect(url_for('userprofile'))
            else:
                updateform.name.data = olduser.name
                updateform.username.data = olduser.username
                updateform.gender.data = olduser.gender
                updateform.contact.data = olduser.contact

            return render_template('userprofile_update.html', form=updateform, olduser=olduser, loggedout=loggedout, current_user=current_user, member=member)
        elif isinstance(current_user, Organisations):
            organisation = True
            updateform = updateo(request.form)
            if request.method == "POST" and updateform.validate():
                name = request.form['name']
                username = request.form['username']
                address = request.form['address']
                description = request.form['description']
                contact = request.form['contact']
                profile_pic = request.files['profile_pic']
            
                if profile_pic.filename == None or profile_pic.filename == '':
                    updateform.profile_pic.data = olduser.profile_pic
                else:
                    pic_filename = secure_filename(profile_pic.filename)
                    pic_name1 = str(uuid.uuid1()) + "_" + pic_filename
                    profile_pic.save(os.path.join(app.config['UPLOAD_FOLDER'], pic_name1))
                    pic_name =  "static/uploads/" + pic_name1
                    olduser.profile_pic = pic_name

                olduser.name = name
                olduser.username = username
                olduser.description = description
                olduser.address = address
                olduser.contact = contact

                db.session.commit()
                db.session.close()

                return redirect(url_for('userprofile'))
            else:
                updateform.name.data = olduser.name
                updateform.username.data = olduser.username
                updateform.description.data = olduser.description
                updateform.address.data = olduser.address
                updateform.contact.data = olduser.contact

            return render_template('userprofile_update.html', form=updateform, olduser=olduser, loggedout=loggedout, current_user=current_user, organisation=organisation)

@loginmanager.user_loader
def load_user(email):
    return Users.query.get(email)

INACTIVITY_THRESHOLD = 60 * 60 #1 minute of inactivity
def check_user_activity():
    last_activity = session.get('last_activity')
    if last_activity:
        elapsed_time = time.time() - last_activity
        if elapsed_time > INACTIVITY_THRESHOLD:
            session.clear()
            flash("You have been logged out due to inactivity")

@app.before_request
def before_request():
    if 'user_id' in session:
        check_user_activity()
        session['last_activity'] = time.time()

@app.route('/reset_activity', methods=['POST'])
@csrf.exempt
@limiter.exempt
def reset_activity():
    if 'user_id' in session:

        csrf_token = generate_csrf()

        session['last_activity'] = time.time()
    return ''

@app.route('/login', methods=['GET', 'POST'])
@limiter.limit('5/second')
def login_():
    object_id_to_hash = id_mappings.object_id_to_hash
    login_form = login(request.form)
    if request.method == "POST" and login_form.validate():
        loginemail = str(login_form.email.data).lower()
        user = Users.query.filter_by(email=loginemail).first()

        if not user:
            flash("Invalid email or password", "danger")
            return redirect(url_for('login_'))

        if user.is_locked:
            if user.last_failed_attempt is not None:
                elapsed_time = datetime.now() - user.last_failed_attempt
            else:
                elapsed_time = timedelta(minutes=1)
                
            if elapsed_time < timedelta(minutes=10):
                app.logger.warning('Attempt to login during account lockout', extra={'security_relevant': True, 'http_status_code': 401, 'flagged': True})
                flash("Account is locked. Please try again later.", "danger")
                return redirect(url_for('login_'))
            else:
                # Reset failed login attempts after 10 minutes
                user.failed_login_attempts = 0
                user.last_failed_attempt = None
                user.is_locked = False
                db.session.commit()

        if bcrypt.checkpw(login_form.password.data.encode('utf-8'), user.password.encode('utf-8')):
            if user.is_active:
                flash("Unable to login as another user is logged in on this account")
                return redirect(url_for('login_'))

            user.is_active = True
            session['user_id'] = user.id
            session['last_activity'] = time.time()  # Reset last activity upon successful login
            session.permanent = True

            # Reset failed login attempts on successful login
            user.failed_login_attempts = 0
            user.last_failed_attempt = None
            user.is_locked = False
            db.session.commit()

            if isinstance(user, Members):
                return redirect(url_for('fotp', hashedid=object_id_to_hash(object_id=user.id, act='member')))
            elif isinstance(user, Organisations):
                return redirect(url_for('fotp', hashedid=object_id_to_hash(object_id=user.id, act='organisation')))
            elif isinstance(user, Admins):
                return redirect(url_for('fotp', hashedid=object_id_to_hash(object_id=user.id, act='admin')))

            return redirect(url_for('fotp', id=user.id))

        else:
            # Failed login attempt
            user.failed_login_attempts += 1
            user.last_failed_attempt = datetime.now()

            # Check if the account should be locked
            if user.failed_login_attempts >= 3:
                app.logger.warning('Too many failed login attempts', extra={'security_relevant': True, 'http_status_code': 401, 'flagged': True})
                flash("Too many failed login attempts. Account is locked for 10 minutes.", "danger")
                user.is_locked = True

            db.session.commit()

            flash("Invalid email or password", "danger")
            return redirect(url_for('login_'))

    # Check for elapsed time and reset failed_login_attempts after 10 minutes
    if 'user_id' in session and 'last_activity' in session:
        elapsed_time = time.time() - session['last_activity']
        if elapsed_time > 600:
            user = Users.query.filter_by(id=session['user_id']).first()
            if user:
                user.failed_login_attempts = 0
                user.last_failed_attempt = None
                user.is_locked = False
                db.session.commit()

    session['last_activity'] = time.time()
    generate_csrf()  # Add CSRF token to the session

    return render_template('login.html', form=login_form)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout_():
    user = current_user
    user.set_inactive()
    db.session.commit()
    logout_user()

    # revoke_login_token()
    session.pop('user_id', None)
    session.pop('last_activity', None)
    return redirect(url_for('login_'))

@app.route('/forget', methods=['GET', 'POST'])
def forgetpw():
    forget_form = forget(request.form)
    if request.method == "POST" and forget_form.validate():
        forgetemail = str(forget_form.email.data).lower()
        user = Users.query.filter_by(email=forgetemail).first()
        if user:
            sendemail(user)
            flash("Email has been sent! Please check your inbox and junk folder for the reset link.", "success")
        else:
            flash("No account with that email exists. Please try again.", "warning")
            return redirect(url_for('forgetpw'))
    return render_template('forgotpassword.html', form=forget_form)

def sendemail(user):
    token = user.get_reset_token()
    msg = Message()
    msg.subject = "Password Reset"
    msg.recipients = [user.email]
    msg.sender = 'environmeet@outlook.com'
    msg.body = f'''Hello, {user.name}\nWe've received a request to reset your password for your Environmeet Account. 
    \nYou can reset the password by clicking the link: \n{url_for('reset_token', token=token, _external=True)}
    \nIf you did not request this password reset, please let us know immediately.
    \nBest regards,\nThe Environmeet Team
    '''
    mail.send(msg)

@app.route('/reset/<token>', methods=['GET', 'POST'])
def reset_token(token):
    user = Users.verify_reset_token(token)
    if not user:
        flash('That is an invalid token.', "danger")
        return redirect(url_for('login_'))
    resetform = reset(request.form)
    if request.method == "POST" and resetform.validate():
        passwordd = bcrypt.hashpw(resetform.password.data.encode('utf-8'), bcrypt.gensalt())
        user.password = passwordd
        db.session.commit()
        db.session.close()
        flash('Your password has been updated! You are now able to log in.','success')
        return redirect(url_for('login_'))

    return render_template('reset.html', form=resetform)


@app.route('/otp/<hashedid>', methods=['GET', 'POST'])
def fotp(hashedid):
    id = id_mappings.hash_to_object_id(hashedid)
    form = getotp(request.form)
    user = Users.query.get(id)
    totp = pyotp.TOTP('base32secret3232')
    if request.method == "POST" and form.validate():
        stored_token = user.otp_token
        if stored_token and stored_token == form.num.data and is_otp_token_valid(user):
            login_user(user)
            flash("Login Successful!", "success")
            temp = user.login_before
            user.login_before = True
            user.last_login = datetime.now()
            db.session.commit()
            if temp == False:
                return redirect(url_for('firstreset'))
            elif isinstance(user, Members) or isinstance(user, Organisations):
                return redirect(url_for('userprofile'))
            elif isinstance(user, Admins):
                return redirect(url_for('admin'))
        else:
            app.logger.warning('Wrong OTP given', extra={'security_relevant': True, 'http_status_code': 401, 'flagged': True})
            flash("Wrong OTP. Please try again", "warning")

    token = generate_otp_token(user, totp)
    print(token)
    # send_otp_email(user, token)

    flash("OTP has been sent to your email! Please check your inbox and junk folder for the OTP.", "primary")
    return render_template('otp.html', form=form, valid=5*60)

@app.route('/firstreset', methods=['GET', 'POST'])
@login_required
def firstreset():
    resetform = reset(request.form)
    if current_user.reset_before:
        flash('You have already done this first reset.', "info")
        return redirect(url_for('userprofile'))
    if request.method == "POST" and resetform.validate():
        passwordd = bcrypt.hashpw(resetform.password.data.encode('utf-8'), bcrypt.gensalt())
        current_user.password = passwordd
        current_user.reset_before = True
        db.session.commit()
        db.session.close()
        if isinstance(current_user, Admins):
            return redirect(url_for('admin'))
        else:
            flash('Your password has been updated! You are now able to log in using the new password','success')
            return redirect(url_for('userprofile'))
    return render_template('reset.html', form=resetform)

def send_otp_email(user, token):
    msg = Message()
    msg.subject = "Account Login"
    msg.recipients = [user.email]
    msg.sender = 'environmeet@outlook.com'
    msg.body = f'''Hello, {user.name}\nHere's your OTP: \n{token}\nThe OTP will expire at {datetime.now() + timedelta(minutes = 5)}
    \nBest regards,\nThe Environmeet Team
    '''
    mail.send(msg)

def is_otp_token_valid(user):
    # Check if the stored OTP token is still valid (within the expiration time)
    expiration_time = user.otp_token_expiration
    current_time = datetime.now()
    return expiration_time is not None and current_time <= expiration_time

def generate_otp_token(user, totp):
    token = totp.now()  # Generate the OTP token
    # Store the token and its expiration time for the user
    user.otp_token = token
    user.otp_token_expiration = datetime.now() + timedelta(minutes=5)  # Set expiration time to 5 minutes from now
    db.session.commit()
    return token

@app.route('/search')
def search():
    users = []
    for i in Users.query.all():
        if not isinstance(i, Admins):
            users.append(i)
    return render_template('search.html', users=users)

@app.route('/user/<username>')
def othersprofile(username):
    user = Users.query.filter_by(username=username).first()
    posts = 0
    for i in Posts.query.filter_by(author=user.id):
        posts += 1
    followers = 0
    for i in Users.query.all():
        if i.is_following(user):
            followers += 1
    following = 0
    for i in Users.query.all():
        if user.is_following(i):
            following += 1
            
    if not current_user.is_authenticated:
        loggedout = True
    else:
        loggedout = False
    return render_template('profile.html', user=user, current_user=current_user, posts=posts, followers=followers, following=following, loggedout=loggedout)


@app.route('/follow/<username>')
@login_required
def follow(username):
    user = Users.query.filter_by(username=username).first()
    if user is None:
        flash('User %s not found.' % username)
        return redirect(url_for('search'))
    u = current_user.follow(user)
    if u is None:
        flash('Cannot follow ' + username + '.')
        return redirect(url_for('othersprofile', username=username))
    db.session.add(u)
    db.session.commit()
    flash('You are now following ' + username + '!',"info")
    return redirect(url_for('othersprofile', username=username))

@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = Users.query.filter_by(username=username).first()
    if user is None:
        flash('User %s not found.' % username)
        return redirect(url_for('feed'))
    u = current_user.unfollow(user)
    if u is None:
        flash('Cannot unfollow ' + username + '.')
        return redirect(url_for('othersprofile', username=username))
    db.session.add(u)
    db.session.commit()
    flash('You have stopped following ' + username + '.',"info")
    return redirect(url_for('othersprofile', username=username))

@app.route("/settings")
@reset_required
def settings():
    return render_template('settings.html')