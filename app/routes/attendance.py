from app import app
from flask import render_template, request, redirect, url_for, flash
from database.models import Attendance, SignUps
from app.util import id_mappings

@app.route('/attendance')
def display_attendance():
    attendance_records = Attendance.query.all()
    eventsignups = SignUps.query.all()

    return render_template('attendance.html', get_event_from_id=id_mappings.get_event_from_id, records=attendance_records)

@app.route('/attendance/checkorgs')
def display_attendance_org():
    eventsignups = SignUps.query.all()

    return render_template('checkattendance.html', get_event_from_id=id_mappings.get_event_from_id, records=eventsignups)