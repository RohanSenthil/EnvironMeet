from wtforms import Form, StringField, SelectField, TextAreaField, validators, IntegerField , FileField , FloatField, TimeField, PasswordField, BooleanField
from wtforms.validators import ValidationError, InputRequired,DataRequired, EqualTo, Email, Regexp
from flask_wtf.file import FileRequired , FileAllowed, FileField
from wtforms.fields import DateField
from database.models import Members, Organisations, Users
from flask_wtf import RecaptchaField
import re
from app.routes.accounts import decrypt, encrypt

class PasswordValidator:
    def __call__(self, form, field):
        password = field.data
        if len(password) < 10:
            raise validators.ValidationError('Password must be at least 10 characters long.')

        # Check for at least one uppercase letter
        if not any(char.isupper() for char in password):
            raise validators.ValidationError('Password must contain at least one uppercase letter.')

        # Check for at least one lowercase letter
        if not any(char.islower() for char in password):
            raise validators.ValidationError('Password must contain at least one lowercase letter.')

        # Check for at least one number
        if not any(char.isdigit() for char in password):
            raise validators.ValidationError('Password must contain at least one number.')

        # Check for at least one special character (non-alphanumeric)
        if not re.search(r'[!@#$%^&*(),.?":{}|]', password):
            raise validators.ValidationError('Password must contain at least one special character.')
        
class SafeStringField(StringField):
    def process_formdata(self, valuelist):
        if valuelist:
            user_input = valuelist[0]
            encoded_input = self.html_encode(user_input)
            self.data = encoded_input

    @staticmethod
    def html_encode(input_string):
        html_entities = {
            '<': '&lt;',
            '>': '&gt;',
            '&': '&amp;',
            '"': '&quot;',
            "'": '&#39;',
            '/': '&#47;',
            '¡': '&iexcl;',
            '¢': '&cent;',
            '£': '&pound;',
            '¤': '&curren;',
            '¥': '&yen;',
            '¦': '&brvbar;',
            '§': '&sect;',
            '©': '&copy;',
            '®': '&reg;',
            '°': '&deg;',
            '±': '&plusmn;',
            'µ': '&micro;',
            '¶': '&para;',
            '·': '&middot;',
            '¿': '&iquest;',
            'À': '&Agrave;',
            'Á': '&Aacute;',
            'Â': '&Acirc;',
            'Ã': '&Atilde;',
            'Ä': '&Auml;',
            'Å': '&Aring;',
            'Æ': '&AElig;',
            'Ç': '&Ccedil;',
            'È': '&Egrave;',
            'É': '&Eacute;',
            'Ê': '&Ecirc;',
            'Ë': '&Euml;',
            'Ì': '&Igrave;',
            'Í': '&Iacute;',
            'Î': '&Icirc;',
            'Ï': '&Iuml;',
            'Ð': '&ETH;',
            'Ñ': '&Ntilde;',
            'Ò': '&Ograve;',
            'Ó': '&Oacute;',
            'Ô': '&Ocirc;',
            'Õ': '&Otilde;',
            'Ö': '&Ouml;',
            '×': '&times;',
            'Ø': '&Oslash;',
            'Ù': '&Ugrave;',
            'Ú': '&Uacute;',
            'Û': '&Ucirc;',
            'Ü': '&Uuml;',
            'Ý': '&Yacute;',
            'Þ': '&THORN;',
            'ß': '&szlig;',
            'à': '&agrave;',
            'á': '&aacute;',
            'â': '&acirc;',
            'ã': '&atilde;',
            'ä': '&auml;',
            'å': '&aring;',
            'æ': '&aelig;',
            'ç': '&ccedil;',
            'è': '&egrave;',
            'é': '&eacute;',
            'ê': '&ecirc;',
            'ë': '&euml;',
            'ì': '&igrave;',
            'í': '&iacute;',
            'î': '&icirc;',
            'ï': '&iuml;',
            'ð': '&eth;',
            'ñ': '&ntilde;',
            'ò': '&ograve;',
            'ó': '&oacute;',
            'ô': '&ocirc;',
            'õ': '&otilde;',
            'ö': '&ouml;',
            '÷': '&divide;',
            'ø': '&oslash;',
            'ù': '&ugrave;',
            'ú': '&uacute;',
            'û': '&ucirc;',
            'ü': '&uuml;',
            'ý': '&yacute;',
            'þ': '&thorn;',
            'ÿ': '&yuml;',
        }

        encoded_string = ""
        for char in input_string:
            if char in html_entities:
                encoded_string += html_entities[char]
            else:
                encoded_string += char
        return encoded_string


class register(Form):
    name = SafeStringField('Name', validators=[DataRequired()])
    username = SafeStringField('Username', validators=[DataRequired()])
    email = SafeStringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password:', [
        PasswordValidator(),
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

class createm(Form):
    name = SafeStringField('Name', validators=[DataRequired()])
    username = SafeStringField('Username', validators=[DataRequired()])
    email = SafeStringField('Email', validators=[DataRequired(), Email()])
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
    name = SafeStringField('Name', validators=[DataRequired()])
    gender = SelectField('Gender', choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], validators=[DataRequired()])
    contact = StringField('Contact Number', validators=[DataRequired(), Regexp('^\d{8}$', message="Contact must be 8 integer digits.")])
    username = SafeStringField('Username', validators=[DataRequired()])
    profile_pic = FileField('Profile Picture:', validators=[FileAllowed(['jpeg','jpg','png'], "File uploaded is not in accepted format.")])
    # def validate_username(self, username):
    #     unique = Users.query.filter_by(username=(username.data).lower()).first()
    #     if unique:
    #         raise ValidationError("Username already in database! Please enter a unique username.")

class login(Form):
    recaptcha = RecaptchaField()
    email = SafeStringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password:', [
        validators.Length(min=10),
        validators.DataRequired(),
    ])

class forget(Form):
    email = SafeStringField('Email', validators=[DataRequired(), Email()])
        
class reset(Form):
    password = PasswordField('New Password:', [
        PasswordValidator(),
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Confirm Password:')



class createo(Form):
    name = SafeStringField('Name', validators=[DataRequired()])
    username = SafeStringField('Username', validators=[DataRequired()])
    email = SafeStringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password:', [
        PasswordValidator(),
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Confirm Password', validators=[DataRequired()])
    address = SafeStringField('Address')
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
    name = SafeStringField('Name', validators=[DataRequired()])
    contact = StringField('Contact Number', validators=[DataRequired(), Regexp('^\d{8}$', message="Contact must be 8 integer digits.")])
    username = SafeStringField('Username', validators=[DataRequired()])
    address = SafeStringField('Address')
    description = TextAreaField('Description:')
    profile_pic = FileField('Profile Picture:', validators=[FileAllowed(['jpeg','jpg','png'], "File uploaded is not in accepted format.")])
    # def validate_username(self, username):
    #     unique = Users.query.filter_by(username=(username.data).lower()).first()
    #     if unique:
    #         raise ValidationError("Username already in database! Please enter a unique username.")

class getotp(Form):
    num = StringField('Enter OTP:', validators=[DataRequired(), Regexp(r'^\d{6}$', message='Invalid OTP. Must be a 6-digit number.')])



class createa(Form):
    name = SafeStringField('Name', validators=[DataRequired()])
    email = SafeStringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password:', [
        PasswordValidator(),
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Confirm Password', validators=[DataRequired()])
    gender = SelectField('Gender', choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], validators=[DataRequired()])
    contact = StringField('Contact Number', validators=[DataRequired(), Regexp('^\d{8}$', message="Contact must be 8 integer digits.")])

    def validate_email(self, email):
        unique = Users.query.filter_by(email=(email.data).lower()).first()
        if unique:
            raise ValidationError("Email already in database! Please enter a new email.")
            
class updatea(Form):
    name = SafeStringField('Name', validators=[DataRequired()])
    gender = SelectField('Gender', choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], validators=[DataRequired()])
    contact = StringField('Contact Number', validators=[DataRequired(), Regexp('^\d{8}$', message="Contact must be 8 integer digits.")])
    # def validate_username(self, username):
    #     unique = Users.query.filter_by(username=(username.data).lower()).first()
    #     if unique:
    #         raise ValidationError("Username already in database! Please enter a unique username.")
