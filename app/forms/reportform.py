from wtforms import Form, StringField, SelectField, TextAreaField, validators, IntegerField , FileField , FloatField, TimeField, PasswordField, BooleanField
from wtforms.validators import ValidationError, InputRequired,DataRequired, EqualTo, Email, Regexp
from flask_wtf.file import FileRequired , FileAllowed, FileField
from wtforms.fields import DateField
from database.models import Members, Organisations, Users
from flask_wtf import RecaptchaField

class Report(Form):
    reason = SelectField('Select Reason for Report', choices=[('Spam', 'Spam'), ('Nudity or Sexual Activity', 'Nudity or Sexual Activity'), ('Hate Speech or Symbol', 'Hate Speech or Symbol'), ('Violence', 'Violence'), ('Sale of illegal goods', 'Sale of illegal goods'), ('Bullying or Harrasment', 'Bullying or Harrasment'), ('Intellectual Property Violation', 'Intellectual Property Violation'), ('Suicide', 'Suicide'), ('Eating Disorders', 'Eating Disorders'), ('Scam or Fraud', 'Scam or Fraud'), ('False Information', 'False Information'), ("I Just Don't Like It", "I Just Don't Like It")], validators=[DataRequired()])
    comment = TextAreaField('Additional Comments (Optional)')