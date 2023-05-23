from app import app
from flask import render_template

@app.route('/events')
def events():
    return render_template('events.html')