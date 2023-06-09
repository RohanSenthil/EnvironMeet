from app import app
from database.models import Members, db
from flask import render_template, request
from sqlalchemy import desc
import time

@app.route('/leaderboard')
def leaderboard():
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
            print('dada')
            db.session.commit()
            print('commit')
            # db.session.expire_on_commit = False
            print('close')
        db.session.close()

    return render_template('leaderboard.html', members=members, yearlymembers=yearlymembers)

