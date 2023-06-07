from flask_login import UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
# from app.routes.helpers import privileged_route
from flask_mail import Message
from threading import Thread
from flask import request, render_template, redirect, url_for, flash
from app import app, loginmanager, mail
from database.models import Members, Organisations, db
from app.forms.accountsform import createm, updatem, login, forget, reset
from app.routes.helpers import revoke_login_token, provide_new_login_token


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    # if not current_user.is_authenticated:
    #     loginmanager.login_message = "Please login to access this page"
    #     loginmanager.login_message_category = "danger"
    return render_template('/accounts/profile/memprofile.html')#, name=current_user.name

@loginmanager.user_loader
def load_user(email):
    return Members.query.get(email)
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
        member = Members.query.filter_by(email=loginemail).first()
        # organisation = Organisations.query.filter_by(email=loginemail).first()
        if not member: # and not organisation
            flash("Invalid email or password", "danger")
            return redirect(url_for('login_'))
        elif member:
            if check_password_hash(member.password, login_form.password.data):
                #login_user(member, remember = login_form.remember.data)
                #provide_new_login_token(member.email, "member")
                login_user(member)
                flash("Login Successful!", "success")
                print(current_user)
                return redirect(url_for('profile'))
        
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
        member = Members.query.filter_by(email=forgetemail).first()
        if member:
            sendemail(member)
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
    msg.sender = 'admin@odlanahor.store'
    msg.body = f'''Hello, {user.name}\nWe've received a request to reset your password for your Odlanaccount. 
    \nYou can reset the password by clicking the link: 
    {url_for('reset_token', token=token, _external=True)}
    \nIf you did not request this password reset, please let us know immediately.
    \nBest regards,
    The Odlanahor Team
    '''
    mail.send(msg)

@app.route('/resetpw/<token>', methods=['GET', 'POST'])
def reset_token(token):
    user = Members.verify_reset_token(token)
    if not user:
        flash('That is an invalid token.', "danger")
        return redirect(url_for('login_'))
    resetform = reset(request.form)
    if request.method == "POST" and resetform.validate():
        hashed_password = generate_password_hash(resetform.password.data)
        user.password = hashed_password
        db.session.commit()
        db.session.close()
        flash('Your password has been updated! You are now able to log in.','success')
        return redirect(url_for('login_'))

    return render_template('reset.html', form=resetform)
