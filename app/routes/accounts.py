# from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
# from werkzeug.security import generate_password_hash, check_password_hash
# from app.routes.helpers import privileged_route
# from flask_mail import Message
# from threading import Thread

# #employees
# @app.route('/accounts/employees')
# @privileged_route("admin")
# def retrieve_employees():
#     employees = Employee.query.all()
#     return render_template('accounts/emp/home_employees.html', employees=employees)

# @app.route('/accounts/employees/create/success')
# @privileged_route("admin")
# def createsuccess_emp():
#     return render_template('accounts/emp/createsuccess.html')

# @app.route('/accounts/employees/update/success')
# @privileged_route("admin")
# def updatesuccess_emp():
#     return render_template('accounts/emp/updatesuccess.html')

# @app.route('/accounts/employees/create', methods=["GET","POST"])
# @privileged_route("admin")
# def create_employee():
#     createemployee_form = createemp(request.form)
#     if request.method == "POST" and createemployee_form.validate():
#         hashed_password = generate_password_hash(createemployee_form.password.data)
#         email = str(createemployee_form.email.data).lower()
#         if createemployee_form.position.data == "Others":
#             position = createemployee_form.positionothers.data
#         else:
#             position = createemployee_form.position.data
#         newemployee = Employee(name=createemployee_form.name.data, gender=createemployee_form.gender.data, email=email, password=hashed_password, contact=createemployee_form.contact.data, position=position)
#         db.session.add(newemployee)
#         db.session.commit()
#         db.session.close()
#         return redirect(url_for('createsuccess_emp'))

#     return render_template('accounts/emp/createemp.html',form=createemployee_form)

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









# @app.route('/accounts')
# @privileged_route("admin")
# def go_home():
#     return render_template('accounts/home.html')
















# #CUSTOMERS
# @app.route('/accounts/customers')
# @privileged_route("admin")
# def retrieve_customers():
#     customers = Customer.query.all()
#     return render_template('accounts/cust/home_customers.html', customers=customers)

# @app.route('/accounts/customers/create/success')
# @privileged_route("admin")
# def createsuccess_cust():
#     return render_template('accounts/cust/createsuccess.html')

# @app.route('/accounts/customers/update/success')
# @privileged_route("admin")
# def updatesuccess_cust():
#     return render_template('accounts/cust/updatesuccess.html')

# @app.route('/accounts/customers/create', methods=["GET","POST"])
# @privileged_route("admin")
# def create_customer():
#     createcustomer_form = createcust(request.form)
#     if request.method == "POST" and createcustomer_form.validate():
#         hashed_password = generate_password_hash(createcustomer_form.password.data)
#         email = str(createcustomer_form.email.data).lower()
#         newcustomer = Customer(name=createcustomer_form.name.data, gender=createcustomer_form.gender.data, email=email, password=hashed_password, contact=createcustomer_form.contact.data)
#         db.session.add(newcustomer)
#         db.session.commit()
#         db.session.close()
#         return redirect(url_for('createsuccess_cust'))

#     return render_template('accounts/cust/createcust.html',form=createcustomer_form)

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










# #login
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

# @app.route('/login/create', methods=["GET","POST"])
# def create_customer_login():
#     createcustomer_form = createcust(request.form)
#     if request.method == "POST" and createcustomer_form.validate():
#         hashed_password = generate_password_hash(createcustomer_form.password.data)
#         email = str(createcustomer_form.email.data).lower()
#         newcustomer = Customer(name=createcustomer_form.name.data, gender=createcustomer_form.gender.data, email=email, password=hashed_password, contact=createcustomer_form.contact.data)
#         db.session.add(newcustomer)
#         db.session.commit()
#         db.session.close()
#         return redirect(url_for('createsuccess_login'))

#     return render_template('login/logincreate.html', form=createcustomer_form)

# @app.route('/login/create/success')
# def createsuccess_login():
#     return render_template('login/createsuccess_login.html')

    



# @app.route('/logout', methods=['GET', 'POST'])
# @login_required
# def logout():
#     logout_user()
#     revoke_login_token()
#     return redirect(url_for('login_'))

# @loginmanager.user_loader
# def load_user(user_id):
#     try:
#         return Customer.query.get(int(user_id))
#     except:
#         return Employee.query.get(int(user_id))







# #custdash
# @app.route('/settings')
# @login_required
# def settings():
#     return render_template('accounts/cust/dashboard/settings.html', current_user=current_user)

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

# def sendemail(user):
#     token = user.get_reset_token()
#     msg = Message()
#     msg.subject = "Password Reset"
#     msg.recipients = [user.email]
#     msg.sender = 'admin@odlanahor.store'
#     msg.body = f'''Hello, {user.name}\nWe've received a request to reset your password for your Odlanaccount. 
#     \nYou can reset the password by clicking the link: 
#     {url_for('reset_token', token=token, _external=True)}
#     \nIf you did not request this password reset, please let us know immediately.
#     \nBest regards,
#     The Odlanahor Team
#     '''
#     mail.send(msg)



# @app.route('/forget', methods=['GET', 'POST'])
# def forgetpw():
#     forget_form = forget(request.form)
#     if request.method == "POST" and forget_form.validate():
#         forgetemail = str(forget_form.email.data).lower()
#         cust = Customer.query.filter_by(email=forgetemail).first()
#         if cust:
#             sendemail(cust)
#             flash("Email has been sent! Please check your inbox and junk folder for the reset link.", "success")
#         else:
#             flash("No account with that email exists. Please try again.", "warning")
#             return redirect(url_for('forgetpw'))
#     return render_template('login/forget.html', form=forget_form)


# @app.route('/resetpw/<token>', methods=['GET', 'POST'])
# def reset_token(token):
#     user = Customer.verify_reset_token(token)
#     if not user:
#         flash('That is an invalid token.', "danger")
#         return redirect(url_for('login_'))
#     resetform = reset(request.form)
#     if request.method == "POST" and resetform.validate():
#         hashed_password = generate_password_hash(resetform.password.data)
#         user.password = hashed_password
#         db.session.commit()
#         db.session.close()
#         flash('Your password has been updated! You are now able to log in.','success')
#         return redirect(url_for('login_'))

#     return render_template('login/reset.html', form=resetform)


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

