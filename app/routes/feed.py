from app import app
from flask import render_template

@app.route('/feed')
def feed():
    return render_template('feed/feed.html')