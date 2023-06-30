from flask_login import login_required, current_user
from app import app, db
from app.util.rate_limiting import limiter
from flask import render_template, request, redirect, url_for, flash
from database.models import Posts, Likes, Comments
from app.forms.feedForms import PostForm 
from werkzeug.utils import secure_filename
import os
from flask.json import jsonify
from app.util import share
from app.util import validation
from app.util import id_mappings
import uuid
from PIL import Image


@app.route('/feed', methods=['GET'])
def feed():
    newPostForm = PostForm()
    posts = Posts.query.all()
    user = current_user

    return render_template('feed.html', posts=posts, newPostForm=newPostForm, user=user, object_id_to_hash=id_mappings.object_id_to_hash, get_user_from_id=id_mappings.get_user_from_id)


@app.route('/post/view/<encoded_hashedid>', methods=['GET'])
def viewPost(encoded_hashedid):

    hashedid = share.decode_url(encoded_hashedid)
    postid = id_mappings.hash_to_object_id(hashedid)
    if postid is not None:
        post = Posts.query.get(postid)

    user = current_user

    if post is not None:
        return render_template('post.html', post=post, user=user, object_id_to_hash=id_mappings.object_id_to_hash, get_user_from_id=id_mappings.get_user_from_id)
    else:
        return jsonify({'error': 'Post doesn\'t exist'}, 400)
    


@app.route('/post/create', methods=['POST'])
@limiter.limit('5/hour')
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
                if uploaded_file.content_length > max_content_length * 2:
                    return jsonify({'error': 'File size too big'}, 400)

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

        hashed_id = id_mappings.hash_object_id(object_id=newPost.id, act='post')
        id_mappings.store_id_mapping(object_id=newPost.id, hashed_value=hashed_id, act='post')

    return redirect(url_for('viewPost', encoded_hashedid=share.encode_url(hashed_id)))


@app.route('/post/edit/<hashedid>', methods=['POST'])
@limiter.limit('10/hour')
@login_required
def editPost(hashedid):

    postid = id_mappings.hash_to_object_id(hashedid)
    if postid is None:
        return jsonify({'error': 'id does not exist'}, 404)
    
    post = Posts.query.get(postid)

    if post is not None:

        # Authorisation Check
        if post.author == current_user.id:
            form = request.form
            print('test')
            post.desc = form[f'desc_{hashedid}']

            db.session.commit()

        else:
            return jsonify({'error': 'Unauthorized'}, 401)
    else:
        return jsonify({'error': 'Post doesn\'t exist'}, 400)
    
    return redirect(url_for('viewPost', encoded_hashedid=share.encode_url(hashedid)))


@app.route('/post/delete/<hashedid>', methods=['POST'])
@limiter.limit('10/hour')
@login_required
def deletePost(hashedid):

    postid = id_mappings.hash_to_object_id(hashedid)

    if postid is None:
        return jsonify({'error': 'id does not exist'}, 404)

    # Implement Authorisation Check

    post = Posts.query.get(postid)

    if post is not None:

        # Authorisation Check
        if post.author == current_user.id:
            if post.image is not None:
                imageFileName = post.image

                if os.path.exists(imageFileName):
                    os.remove(imageFileName)

            db.session.delete(post)
            db.session.commit()

            id_mappings.delete_id_mapping(hashedid)

        else:
            return jsonify({'error': 'Unauthorized'}, 401)

    return redirect(url_for('feed'))


@app.route('/post/like/<hashedid>', methods=['POST'])
@login_required
def likePost(hashedid):

    postid = id_mappings.hash_to_object_id(hashedid)

    if postid is None:
        return jsonify({'error': 'id does not exist'}, 404)
    
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


@app.route('/post/comment/add/<hashedid>', methods=['POST'])
@limiter.limit('10/minute')
@login_required
def addComment(hashedid):

    postid = id_mappings.hash_to_object_id(hashedid)

    if postid is None:
        return jsonify({'error': 'id does not exist'}, 404)

    comment = request.form.get('desc')

    if not comment or len(comment) <= 0:
        return jsonify({'error': 'No comment to add'}, 400)
    else:
        post = Posts.query.get(postid)
        if post:
            newComment = Comments(author=current_user.id, text=comment, post_id=postid)
            db.session.add(newComment)
            db.session.commit()

            hashed_id = id_mappings.hash_object_id(object_id=newComment.id, act='comment')
            id_mappings.store_id_mapping(object_id=newComment.id, hashed_value=hashed_id, act='comment')

    post = Posts.query.get(postid)
    hashed_id = id_mappings.object_id_to_hash(object_id=post.id, act='post')

    return jsonify({'success': 'facts', 'postid': hashed_id})


@app.route('/post/comment/edit/<hashedid>', methods=['POST'])
@limiter.limit('10/minute')
@login_required
def editComment(hashedid):

    commentid = id_mappings.hash_to_object_id(hashedid)

    if commentid is None:
        return jsonify({'error': 'id does not exist'}, 404)

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
    hashed_id = id_mappings.object_id_to_hash(object_id=post_id, act='post')

    return jsonify({'success': 'facts', 'postid': hashed_id})


@app.route('/post/comment/delete/<hashedid>', methods=['POST'])
@limiter.limit('30/minute')
@login_required
def deleteComment(hashedid):

    commentid = id_mappings.hash_to_object_id(hashedid)

    if commentid is None:
        return jsonify({'error': 'id does not exist'}, 404)

    comment = Comments.query.get(commentid)

    if not comment:
        return jsonify({'error': 'Comment does not exists'}, 400)
    elif current_user.id != comment.author:
        return jsonify({'error': 'Unauthorized'}, 401)
    else:
        db.session.delete(comment)
        db.session.commit()

        id_mappings.delete_id_mapping(hashedid)

    post_id = comment.post_id

    return jsonify({'success': 'facts', 'postid': post_id})


@app.route('/post/share/<hashedid>', methods=['POST'])
def sharePost(hashedid):

    native = share.generateNativeLink(hashedid, request.url_root)
    
    return jsonify({'success': 'facts', 'native': native})