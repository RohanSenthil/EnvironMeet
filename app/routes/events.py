from app import app, db
from flask import render_template, request, redirect, url_for, flash
from database.models import Events, SignUps, Members, Organisations, Users
from app.forms.eventsform import FormEvents
from app.forms.eventssignup import SignUp
from app.util import validation, id_mappings
from PIL import Image
import os
from flask.json import jsonify
from werkzeug.utils import secure_filename
import uuid
from datetime import datetime
from sqlalchemy import create_engine, text
from flask_login import login_required, current_user

@app.route('/events')
def events():
    events = Events.query.all()
    user = current_user

    return render_template('events.html', events=events, user=user, orgObj=Organisations, memberObj=Members, object_id_to_hash=id_mappings.object_id_to_hash, get_user_from_id=id_mappings.get_user_from_id)

@app.route('/events/add', methods=["GET","POST"])
@login_required
def add_events():

    if not isinstance(current_user, Organisations):
        return jsonify({'error': 'Unauthorized'}, 401)

    form = FormEvents(request.form)
    form.organiser.data = current_user.name

    if request.method == "POST" and form.validate():

        if form.organiser.data != current_user.name:
            return jsonify({'error', 'Unauthorized attempt to modify read only fields'}, 404)

        event = Events(organiser=current_user.id, name=form.name.data, date=form.date.data, time=form.time.data, price=form.price.data, points=form.points.data)

        uploaded_file = request.files['image']
        #Upload images to uploads folder
        max_content_length = 5 * 1024 * 1024

        if uploaded_file.filename != '':

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

            event.image = image_path

            randomized_image = validation.randomize_image(og_image)

            path_list = event.image.split('/')[1:]
            new_path = '/'.join(path_list)
            event.image = new_path
            randomized_image.save('app/' + new_path)

        db.session.add(event)
        db.session.commit()

        hashed_id = id_mappings.hash_object_id(object_id=event.id, act='event')
        id_mappings.store_id_mapping(object_id=event.id, hashed_value=hashed_id, act='event')

        return redirect(url_for('events'))

    return render_template('addevents.html', form=form)

@app.route('/events/signup/<hashedEventid>', methods=["GET","POST"])
@login_required
def signup_events(hashedEventid):

    if not isinstance(current_user, Members):
        return jsonify({'error': 'Unauthorized, only members can sign up'}, 401)
    
    eventid = id_mappings.hash_to_object_id(hashedEventid)
    if eventid is None:
        return jsonify({'error': 'id does not exist'}, 404)
    
    print(eventid)
    event = Events.query.get(eventid)
    user = current_user

    signup = SignUp(request.form)
    signup.name.data = user.name
    signup.email.data = user.email
    signup.eventid.data = event.name

    # eventss = Events.query.all()
    # events_list=[(i.id, i.name) for i in eventss]
    # signup.eventid.choices = events_list

    if request.method == "POST" and signup.validate():

        if signup.name.data != user.name and signup.email.data != user.email and signup.eventid.data != event.name:
            return jsonify({'error', 'Unauthorized attempt to modify read only fields'}, 404)

        signup = SignUps(user_id=user.id, name=signup.name.data, email=signup.email.data, eventid=eventid, attendance_marked='no')
        db.session.add(signup)
        db.session.commit()
        
        signup_id = signup.id
        
        # attendance = Attendance(event=eventid, member=user.id)
        # db.session.add(attendance)
        # db.session.commit()
        # db.session.close()
        return redirect(url_for('events'))

    return render_template('eventssignup.html', signup=signup, event=event)

# @app.route('/transfer', methods=['GET', 'POST'])
# def transfer_column():
#     # Step 2: Query the source table to retrieve the column data
#     source_data = SignUps.query.all()
#
#     # Step 3-6: Iterate over the source data, create destination instances, and transfer the column
#     for source_entry in source_data:
#         if source_entry == 'eventid':
#             column_value = source_entry.column_to_transfer
#
#             destination_entry = Attendance(transferred_column=column_value)
#
#             # Step 5: Add the new instances to the session
#             db.session.add(destination_entry)
#
#     # Step 6: Commit the session
#     db.session.commit()
#
#     return 'Column transferred successfully!'