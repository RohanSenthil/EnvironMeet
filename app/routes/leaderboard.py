from app import app
from flask import render_template

@app.route('/leaderboard')
def events():
    return render_template('leaderboard.html')