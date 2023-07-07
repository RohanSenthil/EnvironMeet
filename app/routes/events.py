from app import app
from flask import render_template, request, redirect, url_for, flash
from database.models import Events, SignUps, db, Attendance
from app.forms.eventsform import FormEvents
from app.forms.eventssignup import SignUp
from app.util import validation
from PIL import Image
import os
from flask.json import jsonify
from werkzeug.utils import secure_filename
import uuid
from datetime import datetime
from sqlalchemy import create_engine, text

@app.route('/events')
def events():
    events = Events.query.all()

    return render_template('events.html', events=events)

@app.route('/events/add', methods=["GET","POST"])
def add_events():

    form = FormEvents(request.form)
    if request.method == "POST" and form.validate():
        event = Events(organiser=form.organiser.data, name=form.name.data, date=form.date.data, time=form.time.data, price=form.price.data, points=form.points.data)

        uploaded_file = request.files['image']
        #Upload images to uploads folder
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

            event.image = image_path

            randomized_image = validation.randomize_image(og_image)

            path_list = event.image.split('/')[1:]
            new_path = '/'.join(path_list)
            event.image = new_path
            randomized_image.save('app/' + new_path)

        db.session.add(event)
        db.session.commit()
        db.session.close()
        return redirect(url_for('events'))

    return render_template('addevents.html', form=form)

@app.route('/events/signup', methods=["GET","POST"])
def signup_events():
    signup = SignUp(request.form)

    eventss = Events.query.all()
    events_list=[(i.id, i.name) for i in eventss]
    signup.eventid.choices = events_list

    if request.method == "POST" and signup.validate():
        signup = SignUps(name=signup.name.data, email=signup.email.data, eventid=signup.eventid.data)
        db.session.add(signup)
        db.session.commit()
        db.session.close()
        #
        # signup_id = signup.id
        #
        # attendance = Attendance(signup_id=signup_id, event=signup.eventid.data)
        # db.session.add(attendance)
        # db.session.commit()
        # db.session.close()
        return redirect(url_for('events'))

    return render_template('eventssignup.html', signup=signup, eventss=eventss)

@app.route('/transfer', methods=['GET', 'POST'])
def transfer_column():
    # Step 2: Query the source table to retrieve the column data
    source_data = SignUps.query.all()

    # Step 3-6: Iterate over the source data, create destination instances, and transfer the column
    for source_entry in source_data:
        if source_entry == 'eventid':
            column_value = source_entry.column_to_transfer

            destination_entry = Attendance(transferred_column=column_value)

            # Step 5: Add the new instances to the session
            db.session.add(destination_entry)

    # Step 6: Commit the session
    db.session.commit()

    return 'Column transferred successfully!'

@app.template_filter('isinstance')
def jinja2_isinstance(obj, classinfo):
    return isinstance(obj, classinfo)

app.jinja_env.filters['isinstance'] = jinja2_isinstance