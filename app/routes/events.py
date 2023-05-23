from app import app
from flask import render_template

@app.route('/events')
def eventspage():
    return render_template('events.html')