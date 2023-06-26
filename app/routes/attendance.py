from app import app
from flask import render_template, request, redirect, url_for, flash
from database.models import Attendance, Members, Users

@app.route('/attendance')
def attendance():
    user = Members.query.get(id=Users.id).first()
    attendance = Attendance.query.all()

    return render_template('attendance.html', attendance=attendance, user=user)