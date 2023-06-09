from wtforms import Form, StringField, SelectField, TextAreaField, validators, IntegerField , FileField , FloatField, TimeField
from wtforms.validators import ValidationError, InputRequired,DataRequired, Email
from flask_wtf.file import FileRequired , FileAllowed, FileField
from wtforms.fields import DateField

class SignUp(Form):
    name = StringField('Name of event:', validators= [InputRequired()])
    email = StringField('Email:', validators=[DataRequired(), Email()])