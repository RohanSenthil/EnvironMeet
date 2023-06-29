from app import app
from flask import render_template, request, redirect, url_for, flash
from database.models import Attendance

@app.route('/attendance')
def display_attendance():
    attendance_records = Attendance.query.all()

    return render_template('attendance.html', records=attendance_records)