from flask_login import login_required, current_user
from app import app, db
from flask import render_template, request, redirect, url_for, flash
from database.models import Posts, Likes, Comments
from app.forms.feedForms import PostForm 
from werkzeug.utils import secure_filename
import os
from flask.json import jsonify
from app.util import share
from app.util import validation
import uuid
from PIL import Image


@app.route('/feed', methods=['GET'])
@login_required
def feed():
    newPostForm = PostForm()
    posts = Posts.query.all()
    user = current_user

    return render_template('feed.html', posts=posts, newPostForm=newPostForm, user=user)


@app.route('/post/view/<encoded_postid>', methods=['GET'])
def viewPost(encoded_postid):

    postid = share.decode_url(encoded_postid)
    post = Posts.query.get(postid)

    user = current_user

    if post is not None:
        return render_template('post.html', post=post, user=user)
    else:
        return jsonify({'error': 'Post doesn\'t exist'}, 400)
    


@app.route('/post/create', methods=['POST'])
@login_required
def createPost():
    newPostForm = PostForm()
    if request.method == 'POST' and newPostForm.validate_on_submit():

        newPost = Posts(author=current_user.id ,desc=newPostForm.desc.data)

        # Handling file upload
        uploaded_file = newPostForm.image.data 
        max_content_length = 5 * 1024 * 1024

        if uploaded_file is not None:

            if not validation.file_is_image(uploaded_file.stream):
                return jsonify({'error': 'File type not allowed'}, 400)

            filename = uploaded_file.filename
            secureFilename = secure_filename(str(uuid.uuid4().hex) + '.' + filename.rsplit('.', 1)[1].lower())
            image_path = os.path.join(app.config['UPLOAD_PATH'], secureFilename)

            if uploaded_file.content_length > max_content_length:
                image = Image.open(uploaded_file)
                image.thumbnail(max_content_length)
                og_image = Image.open(image)
            else:
                og_image = Image.open(uploaded_file)

            newPost.image = image_path

            randomized_image = validation.randomize_image(og_image)

            path_list = newPost.image.split('/')[1:]
            new_path = '/'.join(path_list)
            newPost.image = new_path
            randomized_image.save('app/' + new_path)

        db.session.add(newPost)
        db.session.commit()

    return redirect(url_for('viewPost', encoded_postid=share.encode_url(str(newPost.id))))


@app.route('/post/edit/<int:postid>', methods=['POST'])
@login_required
def editPost(postid):
    
    post = Posts.query.get(postid)

    if post is not None:

        # Authorisation Check
        if post.author == current_user.id:
            form = request.form
            post.desc = form[f'desc_{postid}']

            db.session.commit()

        else:
            return jsonify({'error': 'Unauthorized'}, 401)
    else:
        return jsonify({'error': 'Post doesn\'t exist'}, 400)
    
    return redirect(url_for('viewPost', encoded_postid=share.encode_url(str(post.id))))


@app.route('/post/delete/<int:postid>', methods=['POST'])
@login_required
def deletePost(postid):

    # Implement Authorisation Check

    post = Posts.query.get(postid)

    if post is not None:

        if post.image is not None:
            imageFileName = post.image

            if os.path.exists(imageFileName):
                os.remove(imageFileName)

        db.session.delete(post)
        db.session.commit()



    return redirect(url_for('feed'))


@app.route('/post/like/<postid>', methods=['POST'])
@login_required
def likePost(postid):
    
    post = Posts.query.get(postid)
    like = Likes.query.filter_by(author=current_user.id, post_id=postid).first()
    
    if not post:
        return jsonify({'error': 'Post doesn\'t exist'}, 400)

    elif like:
        db.session.delete(like)
        db.session.commit()

    else:
        like = Likes(author=current_user.id, post_id=postid)
        db.session.add(like)
        db.session.commit()

    return jsonify({'likes': len(post.likes), 'liked': current_user.id in map(lambda n: n.author, post.likes)})


@app.route('/post/comment/add/<postid>', methods=['POST'])
@login_required
def addComment(postid):

    comment = request.form.get('desc')

    if not comment or len(comment) <= 0:
        return jsonify({'error': 'No comment to add'}, 400)
    else:
        post = Posts.query.get(postid)
        if post:
            newComment = Comments(author=current_user.id, text=comment, post_id=postid)
            db.session.add(newComment)
            db.session.commit()

    post = Posts.query.get(postid)
    post_id = post.id

    return jsonify({'success': 'facts', 'postid': post_id})


@app.route('/post/comment/edit/<commentid>', methods=['POST'])
@login_required
def editComment(commentid):

    newComment = request.form.get('desc')
    comment = Comments.query.get(commentid)

    if not newComment or len(newComment) <= 0:
        return jsonify({'error': 'Comment cannot be blank'}, 400)
    elif current_user.id != comment.author:
        return jsonify({'error': 'Unauthorized'}, 401)
    else:
        comment.text = newComment
        db.session.commit()

    post_id = comment.post_id

    return jsonify({'success': 'facts', 'postid': post_id})


@app.route('/post/comment/delete/<commentid>', methods=['POST'])
@login_required
def deleteComment(commentid):

    comment = Comments.query.get(commentid)

    if not comment:
        return jsonify({'error': 'Comment does not exists'}, 400)
    elif current_user.id != comment.author:
        return jsonify({'error': 'Unauthorized'}, 401)
    else:
        db.session.delete(comment)
        db.session.commit()

    post_id = comment.post_id

    return jsonify({'success': 'facts', 'postid': post_id})


@app.route('/post/share/<postid>', methods=['POST'])
@login_required
def sharePost(postid):

    native = share.generateNativeLink(postid, request.url_root)
    
    return jsonify({'success': 'facts', 'native': native})