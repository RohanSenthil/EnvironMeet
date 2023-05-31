from flask import Flask
from flask_migrate import Migrate
from database.models import db
from database.tools import generate_uri_from_file
import os
from flask_login import LoginManager
from flask_mail import Mail
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

# Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login_'
login_manager.login_message = 'Please log in to access this page.'

from app import routes
from app.util import filters