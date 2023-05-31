from flask import Flask
from flask_migrate import Migrate
from database.models import db
from database.tools import generate_uri_from_file
import os
from flask_login import LoginManager, UserMixin, login_user, logout_user
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

#xavier
loginmanager = LoginManager(app)
loginmanager.init_app(app)
loginmanager.login_view = 'login_'
loginmanager.login_message = 'Please log in to access this page.'
app.config['RECAPTCHA_PUBLIC_KEY'] = os.environ.get('RECAPTCHA_PUBLIC_KEY')
app.config['RECAPTCHA_PRIVATE_KEY'] = os.environ.get('RECAPTCHA_PRIVATE_KEY')
mail = Mail(app)

from app import routes
from app.util import filters