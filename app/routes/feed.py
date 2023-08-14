from flask_login import login_required, current_user
from app import app, db, imagekit
from app.util.rate_limiting import limiter
from flask import render_template, request, redirect, url_for
from database.models import Posts, Likes, Comments, SignUps
from app.forms.feedForms import PostForm 
from werkzeug.utils import secure_filename
import os
from flask.json import jsonify
from app.util import share, validation, id_mappings, moderator
from app.util.helpers import get_following
import uuid
from PIL import Image
from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions


@app.route('/feed', methods=['GET'])
def feed():
    newPostForm = PostForm()
    posts = Posts.query.all()
    user = current_user
    if user.is_authenticated:
        following = get_following(user)

        event_choices = newPostForm.event.choices
        attendedEvents = SignUps.query.filter_by(user_id=current_user.id)
        events_list = [(id_mappings.object_id_to_hash(i.eventid, act='event'), id_mappings.get_event_from_id(i.eventid).name) for i in attendedEvents]
        newPostForm.event.choices = event_choices + events_list

    else:
        following = []

    return render_template('feed.html', posts=posts, newPostForm=newPostForm, user=user, object_id_to_hash=id_mappings.object_id_to_hash, get_user_from_id=id_mappings.get_user_from_id, following=following, get_event_from_id=id_mappings.get_event_from_id)


@app.route('/post/view/<encoded_hashedid>', methods=['GET'])
def viewPost(encoded_hashedid):

    try:
        hashedid = share.decode_url(encoded_hashedid)
    except Exception as e:
        app.logger.error(f'Possible attempt to manipulate URL, Error: {e}', extra={'security_relevant': True, 'http_status_code': 400})
        return jsonify({'error': 'Post doesn\'t exist'}, 400)
    
    postid = id_mappings.hash_to_object_id(hashedid)
    if postid is not None:
        post = Posts.query.get(postid)
    else:
        post = None

    user = current_user

    if post is not None:
        return render_template('post.html', post=post, user=user, object_id_to_hash=id_mappings.object_id_to_hash, get_user_from_id=id_mappings.get_user_from_id, get_event_from_id=id_mappings.get_event_from_id)
    else:
        return jsonify({'error': 'Post doesn\'t exist'}, 404)
    


@app.route('/post/create', methods=['POST'])
@limiter.limit('2/minute')
@limiter.limit('3/day')
@login_required
def createPost():
    newPostForm = PostForm()

    event_choices = newPostForm.event.choices
    attendedEvents = SignUps.query.filter_by(user_id=current_user.id)
    events_list = [(id_mappings.object_id_to_hash(i.eventid, act='event'), id_mappings.get_event_from_id(i.eventid).name) for i in attendedEvents]
    newPostForm.event.choices = event_choices + events_list
    
    if request.method == 'POST' and newPostForm.validate_on_submit():

        if current_user is None:
            return redirect(url_for('login_'))

        if len(newPostForm.desc.data) > 500:

            app.logger.warning('Attempt to bypass client side validation', extra={'security_relevant': True, 'http_status_code': 400, 'flagged': True})
            return jsonify({'error': 'Exceeded word limit'}, 400)

        desc, flags = moderator.moderate_msg(newPostForm.desc.data)

        newPost = Posts(author=current_user.id ,desc=desc)

        valid_events = [id_mappings.object_id_to_hash(i.eventid, act='event') for i in attendedEvents]

        if newPostForm.event.data != 'None' and newPostForm.event.data in valid_events:
            newPost.event = id_mappings.hash_to_object_id(newPostForm.event.data)

        # Handling file upload
        uploaded_file = newPostForm.image.data 
        max_content_length = 5 * 1024 * 1024

        if uploaded_file is not None:

            if not validation.file_is_image(uploaded_file.stream):
                return jsonify({'error': 'File type not allowed'}, 415)
            
            # For Purpose of Eicar demo we will comment this out
            # try:
            #     og_image = Image.open(uploaded_file)
            # except OSError as e:
            #     app.logger.error(f'Possible attempt to upload manipulated image, Error: {e}', extra={'security_relevant': True, 'http_status_code': 415})
            #     return jsonify({'error': 'Invalid image file'}, 415)

            filename = uploaded_file.filename
            secureFilename = secure_filename(str(uuid.uuid4().hex) + '.' + filename.rsplit('.', 1)[1].lower())
            image_path = os.path.join(app.config['UPLOAD_PATH'], secureFilename)

            if uploaded_file.content_length > max_content_length:
                if uploaded_file.content_length > max_content_length * 2:
                    return jsonify({'error': 'File size too big'}, 413)

                image = Image.open(uploaded_file)
                image.thumbnail(max_content_length)
                og_image = Image.open(image)
            else:
                # For Purpose of Eicar demo we will add this
                if filename != 'eicar.png':
                    og_image = Image.open(uploaded_file)

    
            scan_result = validation.scan_file(uploaded_file.read())

            if scan_result == False:

                randomized_image = validation.randomize_image(og_image)

                path_list = image_path.split('/')[1:]
                new_path = '/'.join(path_list)
                newPost.image = new_path
                randomized_image.save('app/' + new_path)

                upload = imagekit.upload_file(
                    file=open('app/' + new_path, 'rb'),
                    file_name=secureFilename,
                    options=UploadFileRequestOptions(
                        folder='/Posts_Images',
                    ),
                )

                response = upload.response_metadata.raw
                newPost.image = response['url']
                newPost.image_id = upload.file_id

                if os.path.exists('app/' + new_path):
                    os.remove('app/' + new_path)

            else:
                flags += 1
                newPost.image = None

        db.session.add(newPost)
        db.session.commit()

        hashed_id = id_mappings.hash_object_id(object_id=newPost.id, act='post')
        id_mappings.store_id_mapping(object_id=newPost.id, hashed_value=hashed_id, act='post')

        if flags > 0:
            redirect_url = url_for("viewPost", encoded_hashedid=share.encode_url(hashed_id))
            return render_template('flagged.html'), {'Refresh': f'10; url={redirect_url}'}

        return redirect(url_for('viewPost', encoded_hashedid=share.encode_url(hashed_id)))
    
    return redirect(url_for('feed'))


@app.route('/post/edit/<hashedid>', methods=['POST'])
@limiter.limit('3/minute')
@limiter.limit('10/day')
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
            desc, flags = moderator.moderate_msg(form[f'desc_{hashedid}'])
            post.desc = desc

            db.session.commit()

            if flags > 0:
                redirect_url = url_for("viewPost", encoded_hashedid=share.encode_url(hashedid))
                return render_template('flagged.html'), {'Refresh': f'10; url={redirect_url}'}

        else:
            app.logger.warning('Unauthorized attempt to edit post', extra={'security_relevant': True, 'http_status_code': 401, 'flagged': True})
            return jsonify({'error': 'Unauthorized'}, 401)
    else:
        return jsonify({'error': 'Post doesn\'t exist'}, 400)
    
    return redirect(url_for('viewPost', encoded_hashedid=share.encode_url(hashedid)))


@app.route('/post/delete/<hashedid>', methods=['POST'])
@limiter.limit('3/minute')
@limiter.limit('10/day')
@login_required
def deletePost(hashedid):

    postid = id_mappings.hash_to_object_id(hashedid)

    if postid is None:
        return jsonify({'error': 'id does not exist'}, 404)

    post = Posts.query.get(postid)

    if post is not None:

        # Authorisation Check
        if post.author == current_user.id:
            if post.image is not None:
                imageFileName = post.image_id

                if os.path.exists(imageFileName):
                    os.remove(imageFileName)

                imagekit.delete_file(file_id=imageFileName)

            for comment in post.comments:
                commentHashedid = id_mappings.object_id_to_hash(comment.id)
                id_mappings.delete_id_mapping(commentHashedid)

            db.session.delete(post)
            db.session.commit()

            id_mappings.delete_id_mapping(hashedid)

        else:
            app.logger.warning('Unauthorized attempt to delete post', extra={'security_relevant': True, 'http_status_code': 401, 'flagged': True})
            return jsonify({'error': 'Unauthorized'}, 401)

    return redirect(url_for('feed'))


@app.route('/post/like/<hashedid>', methods=['POST'])
@limiter.exempt()
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
@limiter.limit('50/day')
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
            comment, flags = moderator.moderate_msg(comment)
            newComment = Comments(author=current_user.id, text=comment, post_id=postid)
            db.session.add(newComment)
            db.session.commit()

            hashed_id = id_mappings.hash_object_id(object_id=newComment.id, act='comment')
            id_mappings.store_id_mapping(object_id=newComment.id, hashed_value=hashed_id, act='comment')

            if flags > 0:
                redirect_url = url_for("viewPost", encoded_hashedid=share.encode_url(hashed_id))
                return render_template('flagged.html'), {'Refresh': f'10; url={redirect_url}'}

    post = Posts.query.get(postid)
    hashed_id = id_mappings.object_id_to_hash(object_id=post.id, act='post')

    return jsonify({'success': 'facts', 'postid': hashed_id})


@app.route('/post/comment/edit/<hashedid>', methods=['POST'])
@limiter.limit('10/minute')
@limiter.limit('50/day')
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
        app.logger.warning('Unauthorized attempt to edit comment', extra={'security_relevant': True, 'http_status_code': 401, 'flagged': True})
        return jsonify({'error': 'Unauthorized'}, 401)
    else:
        
        newComment, flags = moderator.moderate_msg(newComment)

        comment.text = newComment
        db.session.commit()

        if flags > 0:
            redirect_url = url_for("viewPost", encoded_hashedid=share.encode_url(hashed_id))
            return render_template('flagged.html'), {'Refresh': f'10; url={redirect_url}'}

    post_id = comment.post_id
    hashed_id = id_mappings.object_id_to_hash(object_id=post_id, act='post')

    return jsonify({'success': 'facts', 'postid': hashed_id})


@app.route('/post/comment/delete/<hashedid>', methods=['POST'])
@limiter.limit('10/minute')
@limiter.limit('25/day')
@login_required
def deleteComment(hashedid):

    commentid = id_mappings.hash_to_object_id(hashedid)

    if commentid is None:
        return jsonify({'error': 'id does not exist'}, 404)

    comment = Comments.query.get(commentid)

    if not comment:
        return jsonify({'error': 'Comment does not exists'}, 400)
    elif current_user.id != comment.author:
        app.logger.warning('Unauthorized attempt to delete comment', extra={'security_relevant': True, 'http_status_code': 401, 'flagged': True})
        return jsonify({'error': 'Unauthorized'}, 401)
    else:
        db.session.delete(comment)
        db.session.commit()

        id_mappings.delete_id_mapping(hashedid)

    post_id = comment.post_id

    return jsonify({'success': 'facts', 'postid': post_id})


@app.route('/post/share/<hashedid>', methods=['POST'])
@limiter.exempt()
def sharePost(hashedid):

    native = share.generateNativeLink(hashedid, request.url_root)
    
    return jsonify({'success': 'facts', 'native': native})