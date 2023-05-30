from app import app
from flask import render_template, request, redirect, url_for, flash
from database.models import Events, dbevents

@app.route('/events')
def events():
    # dbevents.create_all()
    # events = Events.query.all()
    return render_template('events.html', events=events)
