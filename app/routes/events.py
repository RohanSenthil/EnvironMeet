from app import app
from flask import render_template, request, redirect, url_for, flash
from database.models import Events, db
from app.forms.eventsform import FormEvents

@app.route('/events')
def events():
    # dbevents.create_all()
    # events = Events.query.all()
    return render_template('events.html', events=events)

#NAVIN CODE
@app.route('/events/add', methods=["GET","POST"])
def add_events():

    form = FormEvents(request.form)
    # if form.validate() and request.method == "POST":
    #     # picture_1 = save_image(request.files.get('picture_1'), request.files.get('picture_1').filename)
    #     event = Events(name=FormEvents.name.data.title(), date=FormEvents.date.data, time=FormEvents.time.data,
    #                        price=FormEvents.price.data, organiser=FormEvents.organiser.data)
    #                         # picture_1=picture_1.filename)
    #     db.session.add(event)
    #     db.session.commit()
    #     db.session.close()
    #
    #
    #     return redirect(url_for('events'))
    # else:
    #     flash('You Are Not Authorised to View the Employee Portal', 'danger')
    #     return abort(403)
    # else:
    #     loginmanager.login_message_category = 'warning'
    #     return app.login_manager.unauthorized()
    # else:
    return render_template('addevents.html', form=form)

@app.route('/events/thankyou')
def thankyouforcreatingevents():
    return render_template('eventscreatethankyou.html', thankyouforcreatingevents=thankyouforcreatingevents)