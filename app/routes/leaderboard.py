from app import app
from database.models import Members, db,Leaderboard
from flask import render_template, request
from flask_login import login_required, current_user
from sqlalchemy import desc
import time

@app.route('/leaderboard/global')
def leaderboardglobal():
    db.session()
    print('aaa')
    pp = time.localtime()
    print(pp)
    print(time.asctime(pp))
    members = Members.query.order_by(desc(Members.points)).all()
    print('aaa')
    yearlymembers = Members.query.order_by(desc(Members.yearlypoints)).all()
    if pp.tm_year == 2023 and pp.tm_hour == 9 and pp.tm_yday == 160 and pp.tm_min == 48 and pp.tm_sec < 10:
        for member in members:
            print('poopoo')
            print(member.name)
            member.yearlypoints = 0
            db.session.commit()
        db.session.close()

    return render_template('leaderboardglobal.html', members=members, yearlymembers=yearlymembers)

@app.route('/leaderboard/invite')
@login_required
def leaderboardinvite():



    return render_template('leaderboardinvite.html')