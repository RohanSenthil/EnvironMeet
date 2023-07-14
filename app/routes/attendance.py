from app import app
from flask import render_template, request, redirect, url_for, flash
from database.models import  SignUps, Events, Users, db
from app.forms.eventsupdate import eventsupdate
from app.util import id_mappings
from flask_login import current_user, login_required
import os
from datetime import datetime
from flask.json import jsonify
from werkzeug.utils import secure_filename
import uuid

@app.route('/attendance')
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
# @privileged_route("admin")
def deleteevent(id):
    event = Events.query.filter_by(id=id).first()
    if event:
        db.session.delete(event)
        db.session.commit()
    return redirect(url_for('display_attendance_org'))

@app.route('/attendance/checkorgs')
def display_attendance_org():
    eventssignups = Events.query.all()

    user = current_user

    names = SignUps.query.all()

    return render_template('checkattendance.html', get_event_from_id=id_mappings.get_event_from_id, get_signups_from_id=id_mappings.get_signups_from_id, records=eventssignups, names=names, user=user)


@app.route('/attendance/checkorgs/update/<id>', methods=['GET', 'POST'])
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

        return redirect(url_for('display_attendance_org'))
    else:
        updateform.name.data = oldevents.name
        updateform.date.data = oldevents.date
        updateform.time.data = oldevents.time
        updateform.price.data = oldevents.price
        updateform.points.data = oldevents.points

    return render_template('updateevent.html', form=updateform, oldevents=oldevents)