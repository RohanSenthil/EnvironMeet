from app import app
from flask import render_template, request, redirect, url_for, flash
from database.models import  SignUps, Events, Users, Members, db
from app.forms.eventsupdate import eventsupdate
from app.util import id_mappings
from flask_login import current_user, login_required
import os
from datetime import datetime
from flask.json import jsonify
from werkzeug.utils import secure_filename
import uuid
from app.util.verification import check_is_confirmed, admin_required, org_required

@app.route('/attendance')
@login_required
def display_attendance():
    eventsignups = SignUps.query.all()

    user = current_user

    return render_template('attendance.html', get_event_from_id=id_mappings.get_event_from_id, records=eventsignups, user=user)

@app.route('/attendance/delete/<id>')
# @privileged_route("admin")
def deleteattendance(id):
    signups = SignUps.query.filter_by(id=id).first()
    if signups:
        db.session.delete(signups)
        db.session.commit()
    return redirect(url_for('display_attendance'))

@app.route('/attendance/checkorgs/delete/<id>')
@org_required
# @privileged_route("admin")
def deleteevent(id):
    event = Events.query.filter_by(id=id).first()
    if event:
        db.session.delete(event)
        db.session.commit()
    return redirect(url_for('manage_events'))

@app.route('/events/manage')
@org_required
def manage_events():
    eventssignups = Events.query.all()

    user = current_user

    names = SignUps.query.all()

    return render_template('checkattendance.html', get_event_from_id=id_mappings.get_event_from_id, get_signups_from_id=id_mappings.get_signups_from_id, records=eventssignups, names=names, user=user)


@app.route('/attendance/checkorgs/update/<id>', methods=['GET', 'POST'])
@org_required
def updateevents(id):
    updateform = eventsupdate(request.form)
    oldevents = Events.query.get(id)
    if request.method == "POST" and updateform.validate():
        name = request.form['name']
        date = request.form['date']
        time = request.form['time']
        price = request.form['price']
        points = request.form['points']
        image = request.files['image']

        if image.filename == None or image.filename == '':
            updateform.image.data = oldevents.image
        else:
            pic_filename = secure_filename(image.filename)
            pic_name1 = str(uuid.uuid1()) + "_" + pic_filename
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], pic_name1))
            pic_name = "static/uploads/" + pic_name1
            oldevents.image = pic_name

        oldevents.name = name
        oldevents.date = date
        oldevents.time = time
        oldevents.price = price
        oldevents.points = points

        db.session.commit()
        db.session.close()

        return redirect(url_for('manage_events'))
    else:
        updateform.name.data = oldevents.name
        updateform.date.data = oldevents.date
        updateform.time.data = oldevents.time
        updateform.price.data = oldevents.price
        updateform.points.data = oldevents.points

    return render_template('updateevent.html', form=updateform, oldevents=oldevents)

@app.route('/attendance/checkorgs/attendees/<id>')
@org_required
def check_attendees(id):
    event = Events.query.get(id)
    if event is None:
        return jsonify({'error': 'Event not found'}, 404)

    attendees = event.attendees

    user = current_user

    return render_template('checkattendees.html', event=event, attendees=attendees, user=user)

@app.route('/attendance/checkorgs/attendees/delete/<id>')
@org_required
def deleteattendee(id):
    attendees = SignUps.query.filter_by(id=id).first()
    if attendees:
        db.session.delete(attendees)
        db.session.commit()
    return redirect(url_for('check_attendees', id=attendees.eventid))

@app.route('/attendance/checkorgs/attendees/markattendance/<int:id>')
@org_required
def markattendance(id):
    attendee = SignUps.query.get(id)
    points = Members.query.get(attendee.user_id)
    eventpoints = Events.query.get(attendee.eventid)
    if attendee:
        if attendee.attendance_marked == "Yes":
            flash("Attendance has already been marked!")
        else:
            attendee.attendance_marked = "Yes"
            points.points += eventpoints.points
            points.yearlypoints += eventpoints.points
            db.session.commit()
    return redirect(url_for('check_attendees', id=attendee.eventid))