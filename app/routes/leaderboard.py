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
    inlist = True
    form = AllowedCountriesForm(request.form)
    googlekey = os.environ.get('googlemaps_key')
    deleteform = LeaderboardJoin(request.form)


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

    listofallowedcountries = AllowedCountries.query.all()
    for i in listofallowedcountries:
        if i.country == form.country.data and i.user == user.id:
            inlist = False

    if request.method == 'POST' and form.validate() and inlist == True:
        allowedcountry = AllowedCountries(user=user.id, country=form.country.data)
        db.session.add(allowedcountry)
        db.session.commit()

    if inlist == False:
        flash('The Country is already in the list!', 'danger')





    return render_template('maps.html', location=location, user=user, latitude=latitude, longitude=longitude, googlekey=googlekey, form=form, listofallowedcountries=listofallowedcountries, deleteform=deleteform)


@app.route('/allowcountry/delete/<country>',  methods=["GET","POST"])
@limiter.limit('3/second')
@login_required

def deletecountry(country):
    user = current_user
    country = AllowedCountries.query.filter_by(country=country).first()
    if country and user.id == country.user:
        db.session.delete(country)
        db.session.commit()
        flash(f'You have deleted {country.country} from the list', 'success')

    return redirect(url_for('maps'))