from app import app, mail
from database.models import Members, db,Leaderboard, Users, LeaderboardContent, UserIP, AllowedCountries
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from sqlalchemy import desc
from app.routes.accounts import generate_token
from app.forms.leaderboardform import InviteForm, LeaderboardJoin, AllowedCountriesForm
from app.util import id_mappings
from app.util.id_mappings import get_user_from_id
from app.util.rate_limiting import limiter
from flask_mail import Message
import requests
import socket
import time
import os

def is_valid_leaderboard(leaderboardname):
    leaderboard = LeaderboardContent.query.filter_by(leaderboardname=leaderboardname).first()
    return leaderboard is not None

@app.route('/leaderboard/global')
def leaderboardglobal():
    hostname = socket.gethostname()
    ipaddr = socket.gethostbyname(hostname)
    print(ipaddr)
    db.session()
    pp = time.localtime()
    print(pp)
    print(time.asctime(pp))
    members = Members.query.order_by(desc(Members.points)).all()
    yearlymembers = Members.query.order_by(desc(Members.yearlypoints)).all()
    if pp.tm_year == 2023 and pp.tm_hour == 9 and pp.tm_yday == 160 and pp.tm_min == 48 and pp.tm_sec < 10:
        for member in members:
            print('poopoo')
            print(member.name)
            member.yearlypoints = 0
            db.session.commit()
        db.session.close()

    return render_template('leaderboardglobal.html', members=members, yearlymembers=yearlymembers)

@app.route('/leaderboard/invite', methods=["GET","POST"])
@limiter.limit('3/second')
@login_required
def leaderboardinvite():
    leaderboards = Leaderboard.query.all()
    leaderboardcontents = LeaderboardContent.query.all()
    user = current_user
    createinv = InviteForm(request.form)
    if request.method == "POST" and createinv.validate() :
        print('lol')
        invleaderboard = Leaderboard(name=createinv.name.data, desc=createinv.desc.data, username=user.username)
        db.session.add(invleaderboard)
        db.session.commit()
        leaderboardcontent = LeaderboardContent(leaderboardid=invleaderboard.id, leaderboardname=createinv.name.data, owner=user.username, memberid=user.id, memberpoints=user.points)
        db.session.add(leaderboardcontent)
        db.session.commit()

        hashed_id = id_mappings.hash_object_id(object_id=invleaderboard.id, act='leaderboard')
        id_mappings.store_id_mapping(object_id=invleaderboard.id, hashed_value=hashed_id, act='leaderboard')
        return redirect(url_for('leaderboardinvite'))

    return render_template('leaderboardinvite.html', user=user, form=createinv, leaderboards=leaderboards, leaderboardcontents=leaderboardcontents, get_leaderboard_from_id=id_mappings.get_leaderboard_from_id)

@app.route('/leaderboard/invite/<leaderboardname>', methods=["GET","POST"])
@limiter.limit('3/second')
@login_required

def leaderboardshit(leaderboardname):
    if not is_valid_leaderboard(leaderboardname):
        return render_template('404.html')
    isinleaderboard = False
    user = current_user
    leaderboardin = LeaderboardContent.query.filter_by(leaderboardname=leaderboardname)
    leaderboardaa = LeaderboardContent.query.filter_by(leaderboardname=leaderboardname).first()
    form = LeaderboardJoin(request.form)
    print(leaderboardin)
    for i in LeaderboardContent.query.all():
        if request.method == 'POST' and form.validate() and current_user.id == i.memberid and leaderboardname == i.leaderboardname:
            isinleaderboard = True
            flash("You cannot join a leaderboard you're in!", "danger")
            print('aaa')
    if request.method == 'POST' and form.validate() and isinleaderboard == False:
            leaderboardjoin = LeaderboardContent(leaderboardid=leaderboardaa.leaderboardid, leaderboardname=leaderboardname, owner=leaderboardaa.owner, memberid=user.id, memberpoints=user.points)
            db.session.add(leaderboardjoin)
            db.session.commit()


    return render_template('leaderboarduser.html', leaderboardin=leaderboardin, get_user_from_id=id_mappings.get_user_from_id, form=form)



#
# google map api AIzaSyDBgogdayxPGrvpirHufoJSP3upFEr_-Jo
@app.route('/allowcountry',  methods=["GET","POST"])
@limiter.limit('3/second')
@login_required
def maps():
    form = AllowedCountriesForm(request.form)
    googlekey = os.environ.get('googlemaps_key')


    user = current_user
    api_url = os.environ.get('geolocation_url')
    api_key = os.environ.get('geolocation_key')

    params = {
        'api_key': api_key,
         # 'ip_address': validated_ip_address
    }


    try:
        response = requests.get(api_url, params=params)
        print(response.content)
        data = response.json()
        ipaddress = data['ip_address']
        country = data['country']
        city = data['city']
        latitude = str(data['latitude'])
        longitude = str(data['longitude'])
        location = str(data['latitude']) + ', ' + str(data['longitude'])
        print(country)
        print(city)
        print(ipaddress)
        print(location)
        # readgooglemapsimage()
        # sendverificationemail(user)



        # userinfo = UserIP(user=user.id, country=country, city=city, location=location, ipaddress=ipaddress)
        # db.session.add(userinfo)
        # db.session.commit()


    except requests.exceptions.RequestException as api_error:
        print(f"There was an error contacting the Geolocation API: {api_error}")
        raise SystemExit(api_error)

    if request.method == 'POST' and form.validate():
        allowedcountry = AllowedCountries(user=user.id, country=form.country.data)
        db.session.add(allowedcountry)
        db.session.commit()


    return render_template('maps.html', location=location, user=user, latitude=latitude, longitude=longitude, googlekey=googlekey, form=form)

#
# def sendgeolocationemail(user):
#         token = generate_token(user.email)
#         msg = Message()
#         msg.subject = "Verify Account"
#         msg.recipients = [user.email]
#         msg.sender = 'environmeet@outlook.com'
#         msg.body = f'''Hello, {user.name}\n
#
#         '''
#         mail.send(msg)
# def login_():
#     object_id_to_hash = id_mappings.object_id_to_hash
#     login_form = login(request.form)
#     inallowedcountry = False
#     api_url = os.environ.get('geolocation_url')
#     api_key = os.environ.get('geolocation_key')
#
#     params = {
#         'api_key': api_key,
#         # 'ip_address': validated_ip_address
#     }
#
#     try:
#         response = requests.get(api_url, params=params)
#         print(response.content)
#         data = response.json()
#         ipaddress = data['ip_address']
#         country = data['country']
#         city = data['city']
#         latitude = str(data['latitude'])
#         longitude = str(data['longitude'])
#         location = str(data['latitude']) + ', ' + str(data['longitude'])
#         print(country)
#         print(city)
#         print(ipaddress)
#         print(location)
#
#     except requests.exceptions.RequestException as api_error:
#         print(f"There was an error contacting the Geolocation API: {api_error}")
#         raise SystemExit(api_error)
#
#     for i in AllowedCountries.query.all():
#         if i.country == country:
#             inallowedcountry = True
#
#     if request.method == "POST" and login_form.validate():
#         loginemail = str(login_form.email.data).lower()
#         user = Users.query.filter_by(email=loginemail).first()
#
#         if not user:
#             flash("Invalid email or password", "danger")
#             return redirect(url_for('login_'))
#
#         if user.is_locked:
#             if user.last_failed_attempt is not None:
#                 elapsed_time = datetime.now() - user.last_failed_attempt
#             else:
#                 elapsed_time = timedelta(minutes=1)
#
#             if elapsed_time < timedelta(minutes=10):
#                 app.logger.warning('Attempt to login during account lockout',
#                                    extra={'security_relevant': True, 'http_status_code': 401, 'flagged': True})
#                 flash("Account is locked. Please try again later.", "danger")
#                 return redirect(url_for('login_'))
#             else:
#                 # Reset failed login attempts after 10 minutes
#                 user.failed_login_attempts = 0
#                 user.last_failed_attempt = None
#                 user.is_locked = False
#                 db.session.commit()
#
#         if bcrypt.checkpw(login_form.password.data.encode('utf-8'),
#                           user.password.encode('utf-8')) and inallowedcountry == True:
#             if user.is_active:
#                 flash("Unable to login as another user is logged in on this account")
#                 return redirect(url_for('login_'))
#
#             user.is_active = True
#             session['user_id'] = user.id
#             session['last_activity'] = time.time()  # Reset last activity upon successful login
#             session.permanent = True
#
#             # Reset failed login attempts on successful login
#             user.failed_login_attempts = 0
#             user.last_failed_attempt = None
#             user.is_locked = False
#             db.session.commit()
#
#             if isinstance(user, Members):
#                 return redirect(url_for('fotp', hashedid=object_id_to_hash(object_id=user.id, act='member')))
#             elif isinstance(user, Organisations):
#                 return redirect(url_for('fotp', hashedid=object_id_to_hash(object_id=user.id, act='organisation')))
#             elif isinstance(user, Admins):
#                 return redirect(url_for('fotp', hashedid=object_id_to_hash(object_id=user.id, act='admin')))
#
#             return redirect(url_for('fotp', id=user.id))
#
#         if inallowedcountry == False:
#             print('not in correct country')
#             flash('You are logging in from a country that is not allowed on this account', 'danger')
#             return redirect(url_for('login_'))
#
#         else:
#             # Failed login attempt
#             user.failed_login_attempts += 1
#             user.last_failed_attempt = datetime.now()
#
#             # Check if the account should be locked
#             if user.failed_login_attempts >= 3:
#                 app.logger.warning('Too many failed login attempts',
#                                    extra={'security_relevant': True, 'http_status_code': 401, 'flagged': True})
#                 flash("Too many failed login attempts. Account is locked for 10 minutes.", "danger")
#                 user.is_locked = True
#
#             db.session.commit()
#
#             flash("Invalid email or password", "danger")
#             return redirect(url_for('login_'))
#
#     # Check for elapsed time and reset failed_login_attempts after 10 minutes
#     if 'user_id' in session and 'last_activity' in session:
#         elapsed_time = time.time() - session['last_activity']
#         if elapsed_time > 600:
#             user = Users.query.filter_by(id=session['user_id']).first()
#             if user:
#                 user.failed_login_attempts = 0
#                 user.last_failed_attempt = None
#                 user.is_locked = False
#                 db.session.commit()
#
#     session['last_activity'] = time.time()
#     generate_csrf()  # Add CSRF token to the session
#
#     return render_template('login.html', form=login_form)