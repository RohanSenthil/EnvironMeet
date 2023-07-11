from wtforms import Form, StringField, SelectField, TextAreaField, validators, IntegerField , FileField , FloatField, TimeField
from wtforms.validators import ValidationError, InputRequired,DataRequired, Email
from flask_wtf.file import FileRequired , FileAllowed, FileField
from wtforms.fields import DateField
import sqlite3
from sqlalchemy import create_engine
from flask import Flask


# def fetch_available_items(table_name, column):
#     database_url = 'sqlite:///environmeet.db'
#
#     engine = create_engine(database_url)
#     with engine.connect() as con:
#         result = con.execute(f"SELECT {column} FROM {table_name}")
#         return result.fetchall()

# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'wgaming'

class SignUp(Form):
    name = StringField('Name:', validators= [InputRequired()])
    email = StringField('Email:', validators=[DataRequired(), Email()])
    eventid = StringField('Event Name:', validators=[InputRequired()])





