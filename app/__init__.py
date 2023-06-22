from flask import Flask
from flask_migrate import Migrate
from database.tools import generate_uri_from_file
import os
from flask_login import LoginManager
from flask_mail import Mail
import bcrypt
from flask_security import Security, SQLAlchemyUserDatastore

app = Flask(__name__)

# DB Config
db_uri = generate_uri_from_file('database/db_config.yml')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
# app.config['SQLALCHEMY_BINDS'] = {
#     'environmeet_db': app.config['SQLALCHEMY_DATABASE_URI'],
#     'environmeet_logs': '',
# }

# Other Config
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['UPLOAD_PATH'] = os.environ.get('UPLOAD_PATH')

# For Testing
app.config['TEMPLATES_AUTO_RELOAD'] = True

from database.models import db
from database.models import db

db.init_app(app)
with app.app_context():
    db.create_all()

migrate = Migrate(app, db)

# Auth
loginmanager = LoginManager()
loginmanager.init_app(app)
loginmanager.login_view = 'login_' 
loginmanager.login_message = 'Please log in to access this page.'
app.config['RECAPTCHA_PUBLIC_KEY'] = os.environ.get('RECAPTCHA_PUBLIC_KEY')
app.config['RECAPTCHA_PRIVATE_KEY'] = os.environ.get('RECAPTCHA_PRIVATE_KEY')

mail = Mail(app)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = "environmeet@gmail.com"
app.config['MAIL_PASSWORD'] = f"rohanaldomcDONALDO4927"
app.config['MAIL_DEFAULT_SENDER'] = "environmeet@gmail.com"
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

from app import routes
from app.util import filters