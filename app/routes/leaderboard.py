from app import app
from database.models import Members, db
from flask import render_template, request

@app.route('/leaderboard')
def leaderboard():

    alltimes = Members.query.all()
    print(alltimes)

    return render_template('leaderboard.html', alltimes=alltimes)

