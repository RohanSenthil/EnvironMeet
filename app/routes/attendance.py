from app import app
from flask import render_template, request, redirect, url_for, flash
from database.models import Attendance, SignUps, db
from app.util import id_mappings
from flask_login import current_user, login_required

@app.route('/attendance')
def display_attendance():
    eventsignups = SignUps.query.all()

    return render_template('attendance.html', get_event_from_id=id_mappings.get_event_from_id, records=eventsignups)

@app.route('/attendance/delete/<id>')
# @privileged_route("admin")
def deleteattendance(id):
    signups = SignUps.query.filter_by(id=id).first()
    if signups:
        db.session.delete(signups)
        db.session.commit()
    return redirect(url_for('display_attendance'))

@app.route('/attendance/checkorgs')
def display_attendance_org():
    eventsignups = SignUps.query.all()

    return render_template('checkattendance.html', get_event_from_id=id_mappings.get_event_from_id, records=eventsignups)