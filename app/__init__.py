from flask import Flask
from flask_migrate import Migrate
from database.models import db
from database.tools import generate_uri_from_file
import os

app = Flask(__name__)

# DB Config
db_uri = generate_uri_from_file('database/db_config.yml')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

# Other Config
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['UPLOAD_PATH'] = os.environ.get('UPLOAD_PATH')

# For Testing
app.config['TEMPLATES_AUTO_RELOAD'] = True

db.init_app(app)
with app.app_context():
    db.create_all()

migrate = Migrate(app, db)

from app import routes
from app.util import filters