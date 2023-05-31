from flask_login import UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
# from app.routes.helpers import privileged_route
from flask_mail import Message
from threading import Thread
from flask import request, render_template, redirect, url_for, flash
from app import app, loginmanager
from database.models import Members, Organisations, db
from app.forms.accountsform import createm, updatem, login


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if not current_user.is_authenticated:
        loginmanager.login_message = "Please login to access this page"
        loginmanager.login_message_category = "warning"
    return render_template('/accounts/profile/memprofile.html', name=current_user.name)

@loginmanager.user_loader
def load_user(member_email):
    return Members.query.get(member_email)

#login
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
                return redirect(url_for('profile'))

        # elif emp.position == "Admin":
        #     if check_password_hash(emp.password, login_form.password.data):
        #         login_user(emp, remember = login_form.remember.data)
        #         provide_new_login_token(emp.id, "admin")
        #         return redirect(url_for('admin'))

        # elif emp:
        #     if check_password_hash(emp.password, login_form.password.data):
        #         login_user(emp, remember = login_form.remember.data)
        #         provide_new_login_token(emp.id, "emp")
        #         return redirect(url_for('employee'))
        
        
        flash("Invalid email or password", "danger")
    return render_template('login.html', form=login_form)

@app.route('/logout', methods=['GET', 'POST'])
def logout_():
    logout_user()
    return redirect(url_for('login_'))