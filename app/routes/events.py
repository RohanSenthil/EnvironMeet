from app import app
from flask import render_template, request, redirect, url_for, flash
from database.models import Events, db
from app.forms.eventsform import FormEvents
from datetime import datetime

@app.route('/events')
def events():
    # dbevents.create_all()
    events = Events.query.all()

    return render_template('events.html', events=events)

#NAVIN CODE
@app.route('/events/add', methods=["GET","POST"])
def add_events():

    form = FormEvents(request.form)
    if request.method == "POST" and form.validate():
        event = Events(organiser=form.organiser.data, name=form.name.data, date=form.date.data, price=form.price.data)
        db.session.add(event)
        db.session.commit()
        db.session.close()
        return redirect(url_for('events'))

    return render_template('addevents.html', form=form)

@app.route('/events/thankyou')
def thankyouforcreatingevents():
    return render_template('eventscreatethankyou.html', thankyouforcreatingevents=thankyouforcreatingevents)