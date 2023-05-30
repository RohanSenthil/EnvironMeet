from flask_wtf import FlaskForm
from wtforms import TextAreaField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileField, FileAllowed, FileRequired

class PostForm(FlaskForm):
    desc = TextAreaField('', validators=[DataRequired(message='Please describe what you did!'), Length(min=1, max=500, message='Description must be between 1-500 words')])
    image_1 = FileField('', validators=[FileAllowed(['jpg', 'png'], 'Images only!')])