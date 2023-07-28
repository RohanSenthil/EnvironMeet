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
    if request.method == 'POST' and reportpost.validate():
        print('cuh')
        postreport = PostReport(postid=post.id, author=post.author, reason=reportpost.reason.data, comment=reportpost.comment.data, reporter=user.id, discriminator=user.discriminator)
        db.session.add(postreport)
        db.session.commit()
        hashed_id = id_mappings.hash_object_id(object_id=postreport.id, act='reportpost')
        id_mappings.store_id_mapping(object_id=postreport.id, hashed_value=hashed_id, act='reportpost')
        # flash('You have ')
        return redirect(url_for('feed'))

    return render_template('reportpost.html', form=reportpost, user=user, post=post, get_user_from_id=id_mappings.get_user_from_id)

@app.route('/report/event/<hashedid>', methods=["GET","POST"])
@login_required
def reportevent(hashedid):
    eventid = id_mappings.hash_to_object_id(hashedid)
    event = Events.query.get(eventid)
    user = current_user
    reportevent = Report(request.form)
    if request.method == 'POST' and reportevent.validate():
        print('war')
        eventreport = EventReport(eventreported=event.id, organiser=event.organiser, reason=reportevent.reason.data, comment=reportevent.comment.data, reporter=user.id)
        db.session.add(eventreport)
        db.session.commit()
        hashed_id = id_mappings.hash_object_id(object_id=eventreport.id, act='reportevent')
        id_mappings.store_id_mapping(object_id=eventreport.id, hashed_value=hashed_id, act='reportevent')
        return redirect(url_for('events'))

    return render_template('reportevent.html', form=reportevent, user=user, get_user_from_id=id_mappings.get_user_from_id, event=event)

@app.route('/report/user/<hashedid>', methods=["GET","POST"])
@login_required
def reportuser(hashedid):
    userid = id_mappings.hash_to_object_id(hashedid)
    user = Users.query.get(userid)

    currentuser = current_user

    posts = 0
    for i in Posts.query.filter_by(author=user.id):
        posts += 1
    followers = 0
    for i in Users.query.all():
        if i.is_following(user):
            followers += 1
    following = 0
    for i in Users.query.all():
        if user.is_following(i):
            following += 1
    reportuser = Report(request.form)
    if request.method == 'POST' and reportuser.validate():
        print('userreported')
        userreport = UserReport(userreported=user.id, reason=reportuser.reason.data, comment=reportuser.comment.data, reporter=currentuser.id, discriminator=currentuser.discriminator)
        db.session.add(userreport)
        db.session.commit()
        hashed_id = id_mappings.hash_object_id(object_id=userreport.id, act='reportevent')
        id_mappings.store_id_mapping(object_id=userreport.id, hashed_value=hashed_id, act='reportevent')
        return redirect(url_for('feed'))

    return render_template('reportuser.html', form=reportuser, currentuser=currentuser, get_user_from_id=id_mappings.get_user_from_id, user=user, posts=posts, followers=followers, following=following)
