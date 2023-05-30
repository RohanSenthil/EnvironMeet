from app import app
from flask import render_template, request, redirect, url_for, flash
from database.models import Events, dbevents

@app.route('/events')
def events():
    # dbevents.create_all()
    # events = Events.query.all()
    return render_template('events.html', events=events)

#NAVIN CODE
@app.route('/inventory/add', methods=["GET","POST"])
def add_products():
    if user_is_authenticated():
        privileged_level = get_user_permission_level_from_token()
        if privileged_level in ['admin', 'emp']:
            addproducts_form = FormProducts(request.form)
            if addproducts_form.validate() and request.method == "POST":
                picture_1 = save_image(request.files.get('picture_1'), request.files.get('picture_1').filename)
                product = Products(name=addproducts_form.name.data.title(), type=addproducts_form.type.data,
                                   quantity=addproducts_form.quantity.data, price=addproducts_form.price.data,
                                   restock_status="-", description=addproducts_form.description.data, sold=0,
                                   color=addproducts_form.color.data,
                                   product_nature=addproducts_form.product_nature.data,
                                   picture_1=picture_1.filename, discount=addproducts_form.discount.data)
                db.session.add(product)
                db.session.commit()
                db.session.close()
                flash(f"{addproducts_form.name.data.title()} has been successfully added to Inventory","danger")
                return redirect(url_for('view_products'))

            return render_template('inventory/add.html', form=addproducts_form)
        else:
            flash('You Are Not Authorised to View the Employee Portal', 'danger')
            return abort(403)
    else:
        loginmanager.login_message_category = 'warning'
        return app.login_manager.unauthorized()