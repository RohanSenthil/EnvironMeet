from app import app, db
from flask import render_template, request, redirect, url_for, flash
from database.models import Posts
from app.forms.feedForms import PostForm 
from werkzeug.utils import secure_filename
import os

@app.route('/feed', methods=['GET'])
def feed():
    newPostForm = PostForm()
    posts = Posts.query.all()

    return render_template('feed.html', posts=posts, newPostForm=newPostForm)
    

@app.route('/post/create', methods=['POST'])
def createPost():
    newPostForm = PostForm()
    if request.method == 'POST' and newPostForm.validate_on_submit():

        newPost = Posts(desc=newPostForm.desc.data)

        # Handling file upload
        uploaded_file = newPostForm.image.data

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

    return redirect(url_for('feed'))


@app.route('/post/edit/<int:postid>', methods=['POST'])
def editPost(postid):

    # Implement Authorisation Check

    post = Posts.query.get(postid)
    form = request.form

    if post is not None:
        post.desc = form[f'desc_{postid}']

        db.session.commit()

    return redirect(url_for('feed'))


@app.route('/post/delete/<int:postid>', methods=['POST'])
def deletePost(postid):

    # Implement Authorisation Check

    post = Posts.query.get(postid)

    if post is not None:

        if post.image is not None:
            imageFileName = post.image

            if os.path.exists('app/' + imageFileName):
                os.remove('app/' + imageFileName)

        db.session.delete(post)
        db.session.commit()



    return redirect(url_for('feed'))