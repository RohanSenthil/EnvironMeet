from app import app, db
from flask import render_template, request, redirect, url_for
from database.models import Posts

@app.route('/feed', methods=['GET', 'POST'])
def feed():

    if request.method == 'POST':
        desc = request.form.get('desc')
        
        newPost = Posts(desc=desc)
        db.session.add(newPost)
        db.session.commit()

        return redirect(url_for('feed'))
    
    else:
        posts = Posts.query.all()

        return render_template('feed.html', posts=posts)