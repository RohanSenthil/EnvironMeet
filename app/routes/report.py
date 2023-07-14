from app import app
from database.models import Members, db,Leaderboard, Users, LeaderboardContent, Posts, PostReport, Events, EventReport, UserReport
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from sqlalchemy import desc
from app.forms.reportform import Report
from app.util import id_mappings, helpers, validation, share
import time

@app.route('/report/post/<hashedid>', methods=["GET","POST"])
@login_required
def reportpost(hashedid):
    postid = id_mappings.hash_to_object_id(hashedid)
    post = Posts.query.get(postid)
    user = current_user
    reportpost = Report(request.form)
    print(post.id)
    if reportpost.comment.data is None:
        if request.method == 'POST' and reportpost.validate():
            print('cuh')
            postreport = PostReport(postid=post.id, author=post.author, reason=reportpost.reason.data, reporter=user.id)
            db.session.add(postreport)
            db.session.commit()
            db.session.close()
    else:
        if request.method == 'POST' and reportpost.validate():
            print('cuh')
            postreport = PostReport(postid=post.id, author=post.author, reason=reportpost.reason.data, comment=reportpost.comment.data, reporter=user.id)
            db.session.add(postreport)
            db.session.commit()
            db.session.close()


    return render_template('reportpost.html', form=reportpost, user=user, post=post, get_user_from_id=id_mappings.get_user_from_id)

@app.route('/report/event/<hashedid>', methods=["GET","POST"])
@login_required
def reportevent(hashedid):
    eventid = id_mappings.hash_to_object_id(hashedid)
    event = Events.query.get(eventid)
    user = current_user
    reportevent = Report(request.form)
    if reportevent.comment.data is None:
        if request.method == 'POST' and reportevent.validate():
            print('cuh')
            eventreport = EventReport(eventreported=event.id, organiser=event.organiser, reason=reportevent.reason.data, reporter=user.id)
            db.session.add(eventreport)
            db.session.commit()
            db.session.close()
    else:
        if request.method == 'POST' and reportevent.validate():
            print('cuh')
            eventreport = EventReport(eventreported=event.id, organiser=event.organiser, reason=reportevent.reason.data, comment=reportevent.comment.data, reporter=user.id)
            db.session.add(eventreport)
            db.session.commit()
            db.session.close()

    return render_template('reportevent.html', form=reportevent, user=user, get_user_from_id=id_mappings.get_user_from_id)
