from app import app
from database.models import Members, db
from flask import render_template, request
from sqlalchemy import desc

@app.route('/leaderboard')
def leaderboard():

    members = Members.query.order_by(desc(Members.points)).all()

    return render_template('leaderboard.html', members=members)

