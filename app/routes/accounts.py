from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
# from app.routes.helpers import privileged_route
from flask_mail import Message
from threading import Thread
from flask import request, render_template, redirect, url_for, flash
from app import app, loginmanager
from database.models import Members, Organisations, db, Users
from app.forms.accountsform import createm, updatem, login, createo, updateo
from app.routes.helpers import provide_new_login_token, privileged_route
import bcrypt
from werkzeug.utils import secure_filename
import uuid as uuid
import os

#MEMBERS
@app.route('/members')
def members():
    members = Members.query.all()
    return render_template('/accounts/member/members.html', members=members)


@app.route('/members/create', methods=['GET','POST'])
def createmember():
    createform = createm(request.form)
    if request.method == "POST" and createform.validate():
        print(request.files.get('profile_pic'))
        if request.files.get('profile_pic').filename != '':
            profile_pic = request.files.get('profile_pic')
            print(profile_pic)
            pic_filename = secure_filename(request.files.get('profile_pic').filename)
            print("can file")
            pic_name1 = str(uuid.uuid1()) + "_" + pic_filename
            profile_pic.save(os.path.join(app.config['UPLOAD_FOLDER'], pic_name1))
            pic_name =  "static/uploads/" + pic_name1
        else:
            pic_name = 'static\images\default_profile_pic.png'
        # Process the form data
        emaill = str(createform.email.data).lower()
        usernamee = str(createform.username.data).lower()
        passwordd = bcrypt.hashpw(createform.password.data.encode('utf-8'), bcrypt.gensalt())
        member = Members(name=createform.name.data, email=emaill, username=usernamee, password=passwordd, gender=createform.gender.data, contact=createform.contact.data, points=0, yearlypoints = 0, profile_pic=pic_name)
        db.session.add(member)
        db.session.commit()
        db.session.close()
        return redirect(url_for('members'))
    return render_template('/accounts/member/createm.html', form=createform)

@app.route('/members/update/<id>', methods=['GET','POST'])
def updatemember(id):
    updateform = updatem(request.form)
    oldmem = Members.query.get(id)
    if request.method == "POST" and updateform.validate():
        name = request.form['name']
        username = request.form['username']
        gender = request.form['gender']
        contact = request.form['contact']
        profile_pic = request.files['profile_pic']
    
        if profile_pic.filename == None or profile_pic.filename == '':
            updateform.profile_pic.data = oldmem.profile_pic
        else:
            pic_filename = secure_filename(profile_pic.filename)
            pic_name1 = str(uuid.uuid1()) + "_" + pic_filename
            profile_pic.save(os.path.join(app.config['UPLOAD_FOLDER'], pic_name1))
            pic_name =  "static/uploads/" + pic_name1
            oldmem.profile_pic = pic_name

        oldmem.name = name
        oldmem.username = username
        oldmem.gender = gender
        oldmem.contact = contact

        db.session.commit()
        db.session.close()

        return redirect(url_for('members'))
    else:
        updateform.name.data = oldmem.name
        updateform.username.data = oldmem.username
        updateform.gender.data = oldmem.gender
        updateform.contact.data = oldmem.contact

        return render_template('accounts/member/updatem.html', form=updateform, oldmem=oldmem)

@app.route('/members/delete/<id>')
# @privileged_route("admin")
def deletemember(id):
    member = Members.query.filter_by(id=id).first()
    if member:
        db.session.delete(member)
        db.session.commit()
    return redirect(url_for('members'))


@app.route('/register', methods=['GET', 'POST'])
def registermember():
    registerform = createm(request.form)
    if request.method == "POST" and registerform.validate():
        # Process the form data
        emaill = str(registerform.email.data).lower()
        usernamee = str(registerform.username.data).lower()
        passwordd = bcrypt.hashpw(registerform.password.data.encode('utf-8'), bcrypt.gensalt())
        member = Members(name=registerform.name.data, email=emaill, username=usernamee, password=passwordd, gender=registerform.gender.data, contact=registerform.contact.data, points=0, yearlypoints = 0)
        db.session.add(member)
        db.session.commit()
        db.session.close()
        return redirect(url_for('login_'))

    return render_template('register.html', form=registerform)










'''
@app.route("/confirm/<token>")
def confirm_email(token):
    if current_user.is_confirmed:
        flash("Account already confirmed.", "success")
        return redirect(url_for("core.home"))
    email = confirm_token(token)
    user = User.query.filter_by(email=current_user.email).first_or_404()
    if user.email == email:
        user.is_confirmed = True
        user.confirmed_on = datetime.now()
        db.session.add(user)
        db.session.commit()
        flash("You have confirmed your account. Thanks!", "success")
    else:
        flash("The confirmation link is invalid or has expired.", "danger")
    return redirect(url_for("core.home"))
'''



















#ORGANISATIONS
@app.route('/organisations')
def organisations():
    organisations = Organisations.query.all()
    return render_template('/accounts/organisation/orgs.html', organisations=organisations)

@app.route('/organisations/create', methods=['GET','POST'])
def createorganisations():
    createform = createo(request.form)
    if request.method == "POST" and createform.validate():
        print(request.files.get('profile_pic'))
        if request.files.get('profile_pic').filename != '':
            profile_pic = request.files.get('profile_pic')
            print(profile_pic)
            pic_filename = secure_filename(request.files.get('profile_pic').filename)
            print("can file")
            pic_name1 = str(uuid.uuid1()) + "_" + pic_filename
            profile_pic.save(os.path.join(app.config['UPLOAD_FOLDER'], pic_name1))
            pic_name =  "static/uploads/" + pic_name1
        else:
            pic_name = 'static\images\default_profile_pic.png'
        # Process the form data
        emaill = str(createform.email.data).lower()
        usernamee = str(createform.username.data).lower()
        passwordd = bcrypt.hashpw(createform.password.data.encode('utf-8'), bcrypt.gensalt())
        organisation = Organisations(name=createform.name.data, email=emaill, username=usernamee, password=passwordd, address=createform.address.data, description=createform.description.data, contact=createform.contact.data, profile_pic=pic_name)
        db.session.add(organisation)
        db.session.commit()
        db.session.close()
        return redirect(url_for('organisations'))
    return render_template('/accounts/organisation/createo.html', form=createform)

@app.route('/orgnanisations/update/<id>', methods=['GET','POST'])
def updateorganisation(id):
    updateform = updateo(request.form)
    oldorg = Organisations.query.get(id)
    if request.method == "POST" and updateform.validate():
        name = request.form['name']
        username = request.form['username']
        address = request.form['address']
        description = request.form['description']
        contact = request.form['contact']
        profile_pic = request.files['profile_pic']
    
        if profile_pic.filename == None or profile_pic.filename == '':
            updateform.profile_pic.data = oldorg.profile_pic
        else:
            pic_filename = secure_filename(profile_pic.filename)
            pic_name1 = str(uuid.uuid1()) + "_" + pic_filename
            profile_pic.save(os.path.join(app.config['UPLOAD_FOLDER'], pic_name1))
            pic_name =  "static/uploads/" + pic_name1
            oldorg.profile_pic = pic_name

        oldorg.name = name
        oldorg.username = username
        oldorg.description = description
        oldorg.address = address
        oldorg.contact = contact

        db.session.commit()
        db.session.close()

        return redirect(url_for('organisations'))
    else:
        updateform.name.data = oldorg.name
        updateform.username.data = oldorg.username
        updateform.description.data = oldorg.description
        updateform.address.data = oldorg.address
        updateform.contact.data = oldorg.contact

    return render_template('accounts/organisation/updateo.html', form=updateform, oldorg=oldorg)

@app.route('/organisations/delete/<id>')
# @privileged_route("admin")
def deleteorganisation(id):
    organisation = Organisations.query.filter_by(id=id).first()
    if organisation:
        db.session.delete(organisation)
        db.session.commit()
    return redirect(url_for('organisations'))


























# @app.route('/accounts/employees/create/success')
# @privileged_route("admin")
# def createsuccess_emp():
#     return render_template('accounts/emp/createsuccess.html')

# @app.route('/accounts/employees/update/success')
# @privileged_route("admin")
# def updatesuccess_emp():
#     return render_template('accounts/emp/updatesuccess.html')

# @app.route('/accounts/employees/delete/<id>')
# @privileged_route("admin")
# def delete_employee(id):
#     emp = Employee.query.filter_by(id=id).first()
#     if emp:
#         db.session.delete(emp)
#         db.session.commit()
#     return redirect(url_for('retrieve_employees'))

# @app.route('/accounts/employees/update/<id>',methods=["GET","POST"])
# @privileged_route("admin")
# def update_employee(id):
#     form = updateemp(request.form)
#     oldemp = Employee.query.get(id)
#     position_list = ['Full-time', 'Part-time', 'Intern', 'Admin']
#     if request.method == "POST" and form.validate():
#         name = request.form['name']
#         gender = request.form['gender']
#         contact = request.form['contact']
#         if form.position.data == "Others":
#             position = form.positionothers.data
#         else:
#             position = request.form['position']
#         password = request.form['password']
        
#         oldemp.name = name
#         oldemp.gender = gender
#         oldemp.contact= contact
#         oldemp.position = position
#         oldemp.password = generate_password_hash(password)

#         db.session.commit()
#         db.session.close()

#         return redirect(url_for('updatesuccess_emp'))
#     else:
#         form.name.data = oldemp.name
#         form.gender.data = oldemp.gender
#         form.contact.data = oldemp.contact
#         if oldemp.position not in position_list:
#             form.position.data = 'Others'
#             position_others = oldemp.position
#         else:
#             form.position.data = oldemp.position
#             position_others = ""
#         form.password.data = oldemp.password

#         return render_template('accounts/emp/updateemp.html', form=form, oldemp=oldemp, position_others=position_others)


# @app.route('/accounts/customers/create/success')
# @privileged_route("admin")
# def createsuccess_cust():
#     return render_template('accounts/cust/createsuccess.html')

# @app.route('/accounts/customers/update/success')
# @privileged_route("admin")
# def updatesuccess_cust():
#     return render_template('accounts/cust/updatesuccess.html')


# @app.route('/accounts/customers/delete/<id>')
# @privileged_route("admin")
# def delete_customer(id):
#     cust = Customer.query.filter_by(id=id).first()
#     if cust:
#         db.session.delete(cust)
#         db.session.commit()
#     return redirect(url_for('retrieve_customers'))

# @app.route('/accounts/customers/update/<id>',methods=["GET","POST"])
# @privileged_route("admin")
# def update_customer(id):
#     form = updatecust(request.form)
#     oldcust = Customer.query.get(id)
#     if request.method == "POST" and form.validate():
#         name = request.form['name']
#         gender = request.form['gender']
#         contact = request.form['contact']
        
#         oldcust.name = name
#         oldcust.gender = gender
#         oldcust.contact = contact

#         db.session.commit()
#         db.session.close()

#         return redirect(url_for('updatesuccess_cust'))
#     else:
#         form.name.data = oldcust.name
#         form.gender.data = oldcust.gender
#         form.contact.data = oldcust.contact

#         return render_template('accounts/cust/updatecust.html', form=form, oldcust=oldcust)


# @app.route('/login', methods=['GET', 'POST'])
# def login_():
#     login_form = login(request.form)
    
#     if request.method == "POST" and login_form.validate():
#         loginemail = str(login_form.email.data).lower()
#         unique = Employee.query.filter_by(email=loginemail).first()
#         unique2 = Customer.query.filter_by(email=loginemail).first()
#         user = Customer.query.filter_by(email=loginemail).first()
#         emp = Employee.query.filter_by(email=loginemail).first()
#         if not unique and not unique2:
#             flash("Invalid email or password", "danger")
#             return redirect(url_for('login_'))
#         elif user:
#             if check_password_hash(user.password, login_form.password.data):
#                 login_user(user, remember = login_form.remember.data)
#                 provide_new_login_token(user.id, "cust")
#                 flash("Login Successful!", "success")
#                 return redirect(url_for('dash'))

#         elif emp.position == "Admin":
#             if check_password_hash(emp.password, login_form.password.data):
#                 login_user(emp, remember = login_form.remember.data)
#                 provide_new_login_token(emp.id, "admin")
#                 return redirect(url_for('admin'))

#         elif emp:
#             if check_password_hash(emp.password, login_form.password.data):
#                 login_user(emp, remember = login_form.remember.data)
#                 provide_new_login_token(emp.id, "emp")
#                 return redirect(url_for('employee'))
#         flash("Invalid email or password", "danger")
#     return render_template('login/login.html', form=login_form)


# @app.route('/settings/update', methods=["GET","POST"])
# @login_required
# def updatecust2():
#     form = updatecust(request.form)
#     oldcust = current_user
#     if request.method == "POST" and form.validate():
#         name = request.form['name']
#         gender = request.form['gender']
#         contact = request.form['contact']
        
#         oldcust.name = name
#         oldcust.gender = gender
#         oldcust.contact= contact

#         db.session.commit()
#         db.session.close()
#         flash("Account updated successfully!", "success")
#         return redirect(url_for('settings'))
#     else:
#         form.name.data = oldcust.name
#         form.gender.data = oldcust.gender
#         form.contact.data = oldcust.contact

#         return render_template("accounts/cust/dashboard/updatecust2.html", form=form, oldcust=oldcust)


# #FORGETPASSWORD

# @app.route('/settings/updatepw', methods=['GET', 'POST'])
# @login_required
# def updatepass():
#     newpw = updatepw(request.form)
#     if request.method == "POST" and newpw.validate():
#         if check_password_hash(current_user.password, newpw.current.data):
#             password = generate_password_hash(request.form['password'])
#             current_user.password = password
#             db.session.commit()
#             db.session.close()
#             flash("Password updated successfully!","success")
#             return redirect(url_for('settings'))
#         else:
#             flash("Ensure that current password is correct and new password has a minimum length of 10 characters.","danger")
#             return render_template("accounts/cust/dashboard/custreset.html", form=newpw)
#     else:
#         newpw.password.data = current_user.password
#         return render_template("accounts/cust/dashboard/custreset.html", form=newpw)

