from wtforms import Form, StringField, SelectField, TextAreaField, validators, IntegerField , FileField , FloatField, TimeField, PasswordField, BooleanField
from wtforms.validators import ValidationError, InputRequired,DataRequired, EqualTo, Email, Regexp
from flask_wtf.file import FileRequired , FileAllowed, FileField
from wtforms.fields import DateField
from database.models import Members, Organisations, Users
from flask_wtf import RecaptchaField

class createm(Form):
    name = StringField('Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password:', [
        validators.Length(min=10),
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Confirm Password', validators=[DataRequired()])
    gender = SelectField('Gender', choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], validators=[DataRequired()])
    contact = StringField('Contact Number', validators=[DataRequired(), Regexp('^\d{8}$', message="Contact must be 8 integer digits.")])
    profile_pic = FileField('Profile Picture:', validators=[FileAllowed(['jpeg','jpg','png'], "File uploaded is not in accepted format.")])

    def validate_email(self, email):
        unique = Users.query.filter_by(email=(email.data).lower()).first()
        if unique:
            raise ValidationError("Email already in database! Please enter a new email.")
        
    def validate_username(self, username):
        unique = Users.query.filter_by(username=(username.data).lower()).first()
        if unique:
            raise ValidationError("Username already in database! Please enter a unique username.")
        
class updatem(Form):
    name = StringField('Name', validators=[DataRequired()])
    gender = SelectField('Gender', choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], validators=[DataRequired()])
    contact = StringField('Contact Number', validators=[DataRequired(), Regexp('^\d{8}$', message="Contact must be 8 integer digits.")])
    username = StringField('Username', validators=[DataRequired()])
    profile_pic = FileField('Profile Picture:', validators=[FileAllowed(['jpeg','jpg','png'], "File uploaded is not in accepted format.")])
    # def validate_username(self, username):
    #     unique = Users.query.filter_by(username=(username.data).lower()).first()
    #     if unique:
    #         raise ValidationError("Username already in database! Please enter a unique username.")

class login(Form):
    recaptcha = RecaptchaField()
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password:', [
        validators.Length(min=10),
        validators.DataRequired(),
    ])

class forget(Form):
    email = StringField('Email', validators=[DataRequired(), Email()])
        
class reset(Form):
    password = PasswordField('New Password:', [
        validators.Length(min=10),
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Confirm Password:')






class createo(Form):
    name = StringField('Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password:', [
        validators.Length(min=10),
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Confirm Password', validators=[DataRequired()])
    address = StringField('Address')
    description = TextAreaField('Description:')
    contact = StringField('Contact Number', validators=[DataRequired(), Regexp('^\d{8}$', message="Contact must be 8 integer digits.")])
    profile_pic = FileField('Display Picture:', validators=[FileAllowed(['jpeg','jpg','png'], "File uploaded is not in accepted format.")])

    def validate_email(self, email):
        unique = Users.query.filter_by(email=(email.data).lower()).first()
        if unique:
            raise ValidationError("Email already in database! Please enter a new email.")
        
    def validate_username(self, username):
        unique = Users.query.filter_by(username=(username.data).lower()).first()
        if unique:
            raise ValidationError("Username already in database! Please enter a unique username.")

class updateo(Form):
    name = StringField('Name', validators=[DataRequired()])
    contact = StringField('Contact Number', validators=[DataRequired(), Regexp('^\d{8}$', message="Contact must be 8 integer digits.")])
    username = StringField('Username', validators=[DataRequired()])
    address = StringField('Address')
    description = TextAreaField('Description:')
    profile_pic = FileField('Profile Picture:', validators=[FileAllowed(['jpeg','jpg','png'], "File uploaded is not in accepted format.")])
    # def validate_username(self, username):
    #     unique = Users.query.filter_by(username=(username.data).lower()).first()
    #     if unique:
    #         raise ValidationError("Username already in database! Please enter a unique username.")