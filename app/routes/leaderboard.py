from app import app
from flask import render_template

@app.route('/leaderboard')
def leaderboard():
    return render_template('leaderboard.html')