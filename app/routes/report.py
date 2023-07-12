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
    user = current_user
    reportpost = Report(request.form)
    post = Posts.query.get(postid)
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


    return render_template('reportpost.html', form=reportpost, user=user)
