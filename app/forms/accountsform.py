from wtforms import Form, StringField, SelectField, TextAreaField, validators, IntegerField , FileField , FloatField, TimeField, PasswordField
from wtforms.validators import ValidationError, InputRequired,DataRequired, EqualTo, Email
from flask_wtf.file import FileRequired , FileAllowed, FileField
from wtforms.fields import DateField
from database.models import Members, Organisations

class createm(Form):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    gender = SelectField('Gender', choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], validators=[DataRequired()])
    contact = StringField('Contact', validators=[DataRequired()])

    def validate_email(self, email):
        unique = Members.query.filter_by(email=email.data).first()
        unique2 = Organisations.query.filter_by(email=email.data).first()
        if unique or unique2:
            raise ValidationError("Email already in database! Please enter a new email.")

class updatem(Form):
    name = StringField('Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    gender = SelectField('Gender', choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], validators=[DataRequired()])
    contact = StringField('Contact', validators=[DataRequired()])