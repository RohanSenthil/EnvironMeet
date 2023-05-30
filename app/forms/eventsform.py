from wtforms import Form, StringField, SelectField, TextAreaField, validators, IntegerField , FileField , FloatField, TimeField
from wtforms.validators import ValidationError, InputRequired,DataRequired
from flask_wtf.file import FileRequired , FileAllowed, FileField
from wtforms.fields import DateField
# from database.models import Products


# def unique(form, field):
#     if field.data is not None:
#         data = field.data.title()
#         not_unique = Products.query.filter_by(name=data).first()
#         if not_unique :
#             raise ValidationError("Name must be unique.")
# def exists(form,field):
#     if field.data is None or field.data == "":
#         raise ValidationError("Input is required.")
# def positive(form,field):
#     if field.data is None:
#         raise ValidationError("Input is required")
#     else:
#         if field.data < 0:
#             raise ValidationError("Input must not be negative")
#         if field.data == 0:
#             raise ValidationError("Input must not be 0.")
#
# def discount(form,field):
#     if field.data is None:
#         raise ValidationError("Input is required")
#     elif field.data < 0 or field.data > 100:
#         raise ValidationError("Discount must be between 0 and 100")
class FormEvents(Form):
    name = StringField('Name:', validators= [InputRequired()])
    date = DateField('Date: ',  validators= [InputRequired()])
    time = TimeField('Time: ',  validators= [InputRequired()])
    price = StringField('Price: ', validators=[InputRequired()])
    organiser = StringField('Organiser: ', validators=[InputRequired()])
    # type = SelectField('Type:',validators=[exists],choices=[('', 'Select'), ('H', 'Home Office'), ('D', 'Dining'), ('B', 'Bedding'),('L', 'Living')], default='')
    # price = FloatField('Price:',[positive])
    # quantity= IntegerField('Quantity:',[positive])
    # color = StringField('Color:',[exists])
    # product_nature = SelectField('Product Nature:',validators=[exists],choices=[('', 'Select'), ('P','Promotional'),('N','New Arrivals') , ('R','Regular Products')], default='')
    # description = TextAreaField('Description:',validators=[exists])
    # picture_1 = FileField(label='Picture:', validators=[FileAllowed(['jpg', 'png'])])
    # discount = FloatField('Discount in % :',validators=[discount])

# class Restock(Form):
#     name = StringField('Name:', render_kw={"disabled":"disabled"})
#     quantity = IntegerField('Quantity:',validators=[positive])
#
#
# def pos_update(form,field):
#     if field.data is not None:
#         if float(field.data) < 0:
#             raise ValidationError("Input must not be negative")
#         if float(field.data) == 0:
#             raise ValidationError("Input must not be 0.")
# def dis_update(form,field):
#     if field.data is not None:
#         if float(field.data) < 0 or float(field.data) > 100:
#             raise ValidationError("Discount must be between 0 and 100")
#
# class UpdateProducts(Form):
#     name = StringField('Name:')
#
#     type = SelectField('Type:',choices=[('', 'Select'), ('H', 'Home Office'), ('D', 'Dining'), ('B', 'Bedding'),('L', 'Living')], default='')
#     price = FloatField('Price:',validators=[pos_update])
#     quantity= IntegerField('Quantity:',validators=[pos_update],render_kw={"disabled":"disabled"})
#     color = StringField('Color:')
#     product_nature = SelectField('Product Nature:',choices=[('', 'Select'), ('P','Promotional'),('N','New Arrivals') , ('R','Regular Products')], default='')
#     description = TextAreaField('Description:')
#     picture_1 = FileField(label='Picture:', validators=[FileAllowed(['jpg', 'png'])])
#     discount = FloatField('Discount in % :',validators=[dis_update])
