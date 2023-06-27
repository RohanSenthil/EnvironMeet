from flask_login import UserMixin, login_user, login_required, logout_user, current_user
# from app.routes.helpers import privileged_route
from flask_mail import Message
from threading import Thread
from flask import request, render_template, redirect, url_for, flash
from app import app, loginmanager, mail
from database.models import Members, Organisations, db, Users, followers
from app.forms.accountsform import createm, updatem, login, forget, reset
from app.routes.helpers import revoke_login_token, provide_new_login_token
import bcrypt


@app.route('/profile', methods=['GET', 'POST'])
def userprofile():
    if not current_user.is_authenticated:
        loggedout = True
    else:
        loggedout = False
    following = 0
    for i in Users.query.all():
        if current_user.is_following(i):
            following += 1
    return render_template('/userprofile.html', current_user=current_user, loggedout=loggedout, following=following)

@loginmanager.user_loader
def load_user(email):
    return Users.query.get(email)
# @loginmanager.user_loader
# def load_user(user_id):
#     try:
#         return Customer.query.get(int(user_id))
#     except:
#         return Employee.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login_():
    login_form = login(request.form)

    if request.method == "POST" and login_form.validate():
        loginemail = str(login_form.email.data).lower()
        user = Users.query.filter_by(email=loginemail).first()
        if not user:
            flash("Invalid email or password", "danger")
            return redirect(url_for('login_'))
        elif user:
            if bcrypt.checkpw(login_form.password.data.encode('utf-8'), user.password.encode('utf-8')):
                #login_user(member, remember = login_form.remember.data)
                #provide_new_login_token(member.email, "member")
                login_user(user)
                flash("Login Successful!", "success")
                return redirect(url_for('userprofile'))
        
        flash("Invalid email or password", "danger")
    return render_template('login.html', form=login_form)

@app.route('/logout', methods=['GET', 'POST'])
def logout_():
    logout_user()
    # revoke_login_token()
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

@app.route('/search')
def search():
    users = Users.query.all()
    return render_template('search.html', users=users)

@app.route('/user/<username>')
def othersprofile(username):
    user = Users.query.filter_by(username=username).first()
    return render_template('profile.html', user=user, current_user=current_user)


@app.route('/follow/<username>')
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
    flash('You are now following ' + username + '!',"success")
    return redirect(url_for('othersprofile', username=username))

@app.route('/unfollow/<username>')
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