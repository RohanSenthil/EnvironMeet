from app import app
from database.models import Members, db,Leaderboard, Users, LeaderboardContent
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from sqlalchemy import desc
from app.forms.leaderboardform import InviteForm, LeaderboardJoin
from app.util import id_mappings
from app.util.id_mappings import get_user_from_id
import time

@app.route('/leaderboard/global')
def leaderboardglobal():
    db.session()
    print('aaa')
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
@login_required
def leaderboardshit(leaderboardname):
    user = current_user
    leaderboardin = LeaderboardContent.query.filter_by(leaderboardname=leaderboardname)
    leaderboardaa = LeaderboardContent.query.filter_by(leaderboardname=leaderboardname).first()
    form = LeaderboardJoin(request.form)
    print(leaderboardin)
    for i in get_user_from_id(leaderboardin):
        if current_user == i:
            print('aaa')
        elif request.method == 'POST' and form.validate():
            leaderboardjoin = LeaderboardContent(leaderboardid=leaderboardaa.leaderboardid, leaderboardname=leaderboardname, owner=leaderboardaa.owner, memberid=user.id, memberpoints=user.points)
            db.session.add(leaderboardjoin)
            db.session.commit()

    return render_template('leaderboarduser.html', leaderboardin=leaderboardin, get_user_from_id=id_mappings.get_user_from_id, form=form)