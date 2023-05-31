from app import app
from flask import render_template
from app.routes import feed, events, accounts, leaderboard, profile, helpers

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

