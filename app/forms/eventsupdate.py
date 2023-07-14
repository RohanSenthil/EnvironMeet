from wtforms import Form, StringField, SelectField, TextAreaField, validators, IntegerField , FileField , FloatField, TimeField
from wtforms.validators import ValidationError, InputRequired,DataRequired
from flask_wtf.file import FileRequired , FileAllowed, FileField
from wtforms.fields import DateField
import sqlite3
from sqlalchemy import create_engine
from flask import Flask, render_template, request
class eventsupdate(Form):
    name = StringField('Name of event:', validators= [InputRequired()])
    date = DateField('Date: ',  validators= [InputRequired()])
    time = TimeField('Time: ',  validators= [InputRequired()])
    price = StringField('Price (Opt): ', validators=[InputRequired()])
    points = IntegerField('Number of Points (100-500): ', validators=[InputRequired()])
    image = FileField('', validators=[FileAllowed(['jpg', 'png'], 'Images only!')])