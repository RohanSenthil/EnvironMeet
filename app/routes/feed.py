from app import app, db
from flask import render_template, request, redirect, url_for, flash
from database.models import Posts
from app.forms.feedForms import PostForm 
from werkzeug.utils import secure_filename
import os

@app.route('/feed', methods=['GET', 'POST'])
def feed():
    newPostForm = PostForm()
    if request.method == 'POST':

        if newPostForm.validate_on_submit():

            newPost = Posts(desc=newPostForm.desc.data)

            # Handling file upload
            uploaded_file = newPostForm.image_1.data

            if uploaded_file is not None:
                filename = secure_filename(uploaded_file.filename)
                image_path = os.path.join(app.config['UPLOAD_PATH'], filename)
                uploaded_file.save(image_path)
                newPost.image = image_path
                path_list = newPost.image.split('/')[1:]
                new_path = '/'.join(path_list)
                
                newPost.image = new_path

            db.session.add(newPost)
            db.session.commit()

            flash('Post created!')

        return redirect(url_for('feed'))
    
    else:
        posts = Posts.query.all()

        return render_template('feed.html', posts=posts, newPostForm=newPostForm)