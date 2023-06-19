from app import app
from flask import render_template, request, redirect, url_for, flash
from database.models import Events, SignUps, db
from app.forms.eventsform import FormEvents
from app.forms.eventssignup import SignUp
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
        event = Events(organiser=form.organiser.data, name=form.name.data, date=form.date.data, time=form.time.data, price=form.price.data, points=form.points.data, image=form.image.data)
        db.session.add(event)
        db.session.commit()
        db.session.close()
        return redirect(url_for('events'))

    return render_template('addevents.html', form=form)

@app.route('/events/signup', methods=["GET","POST"])
def signup_events():
    signup = SignUp(request.form)
    if request.method == "POST" and signup.validate():
        signup = SignUps(name=signup.name.data, email=signup.email.data, eventname=signup.eventname.data)
        db.session.add(signup)
        db.session.commit()
        db.session.close()
        return redirect(url_for('events'))

    return render_template('eventssignup.html', signup=signup)