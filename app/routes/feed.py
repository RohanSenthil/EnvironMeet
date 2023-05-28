from app import app, db
from flask import render_template, request, redirect, url_for, flash
from database.models import Posts

@app.route('/feed', methods=['GET', 'POST'])
def feed():

    if request.method == 'POST':
        desc = request.form.get('desc')

        if len(desc) <= 200:
            newPost = Posts(desc=desc)
            db.session.add(newPost)
            db.session.commit()
        else:
            flash('Post description should contain no more than 200 characters.')

        return redirect(url_for('feed'))
    
    else:
        posts = Posts.query.all()

        return render_template('feed.html', posts=posts)