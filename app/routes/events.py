from app import app
from flask import render_template, request, redirect, url_for, flash
from database.models import Events, dbevents

@app.route('/events')
def events():
    # dbevents.create_all()
    # events = Events.query.all()
    return render_template('events.html', events=events)

#NAVIN CODE
@app.route('/events/add', methods=["GET","POST"])
def add_events():
    if addevents_form.validate() and request.method == "POST":
        picture_1 = save_image(request.files.get('picture_1'), request.files.get('picture_1').filename)
        product = Products(name=addevents_form.name.data.title(), date=addevents_form.date.data, time=addevents_form.time.data,
                           price=addevents_form.price.data, organiser=addevents_form.organiser.data,
                            picture_1=picture_1.filename)
        db.session.add(product)
        db.session.commit()
        db.session.close()


        return render_template('addevents.html', form=addevents_form)
    # else:
    #     flash('You Are Not Authorised to View the Employee Portal', 'danger')
    #     return abort(403)
    # else:
    #     loginmanager.login_message_category = 'warning'
    #     return app.login_manager.unauthorized()