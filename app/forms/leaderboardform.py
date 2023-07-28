from flask_wtf import FlaskForm
from wtforms import Form, StringField, SelectField, TextAreaField, validators, IntegerField , FileField , FloatField, TimeField
from wtforms.validators import ValidationError, InputRequired,DataRequired, Email, Length

class InviteForm(Form):
    name = StringField('Leaderboard Name: ', validators=[InputRequired()])
    desc = StringField('Description: ', validators=[InputRequired()])
    # username = StringField('Username: ', validators=[InputRequired()])

class LeaderboardJoin(Form):
    reason = StringField('aa')