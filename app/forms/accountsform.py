from wtforms import Form, StringField, SelectField, TextAreaField, validators, IntegerField , FileField , FloatField, TimeField, PasswordField
from wtforms.validators import ValidationError, InputRequired,DataRequired, EqualTo, Email
from flask_wtf.file import FileRequired , FileAllowed, FileField
from wtforms.fields import DateField

class createm(Form):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    gender = SelectField('Gender', choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], validators=[DataRequired()])
    contact = StringField('Contact', validators=[DataRequired()])