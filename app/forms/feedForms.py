from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, SelectField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileField, FileAllowed

class PostForm(FlaskForm):
    desc = TextAreaField('', validators=[DataRequired(message='Please describe what you did!'), Length(min=1, max=500, message='Description must be between 1-500 words')])
    image = FileField('', validators=[FileAllowed(['jpg', 'png'], 'Images only!')])
    event = SelectField('', validators=[DataRequired()], choices=[('None', 'None')])