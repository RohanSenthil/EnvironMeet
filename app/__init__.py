from flask import Flask, session
from flask_migrate import Migrate
from database.tools import generate_uri_from_file
import os
from flask_login import LoginManager
from flask_mail import Mail
import bcrypt
from flask_security import Security, SQLAlchemyUserDatastore
from opensearchpy import OpenSearch, RequestsHttpConnection, AWSV4SignerAuth
from imagekitio import ImageKit
from flask_login import current_user
from flask_wtf.csrf import CSRFProtect
from datetime import timedelta
import boto3
from flask_socketio import SocketIO


app = Flask(__name__)

# DB Config
db_uri = generate_uri_from_file('database/db_config.yml')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

# AWS Config
session = boto3.Session(
    aws_access_key_id=os.environ.get('aws_access_key_id'),
    aws_secret_access_key=os.environ.get('aws_secret_access_key'),
)

region = 'ap-southeast-2'
service = 'es'
credentials = session.get_credentials()
auth = AWSV4SignerAuth(credentials, region, service)

# Log Config
log_client = OpenSearch(
    hosts=[{'host': 'search-environmeet-logs-gu63r25dgclotf2rt4leyepnpi.ap-southeast-2.es.amazonaws.com', 'port':  443}],
    http_auth = auth, 
    use_ssl = True,
    verify_certs = True,
    connection_class = RequestsHttpConnection,
    pool_maxsize = 20,
)
# log_client = OpenSearch(
#     hosts=[{'host': 'localhost', 'port': 9200}],
#     http_compress=True,
#     http_auth = (os.environ.get('OPENSEARCH_USERNAME'), os.environ.get('OPENSEARCH_PASSWORD')), # For testing change creds for prod
#     use_ssl = True,
#     verify_certs = False,
#     ssl_assert_hostname = False,
#     ssl_show_warn = False
# )

from app.logging import logging

# Other Config
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['UPLOAD_PATH'] = os.environ.get('UPLOAD_PATH')

# For Testing
app.config['TEMPLATES_AUTO_RELOAD'] = True

from database.models import db, Organisations

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


app.config['MAIL_SERVER'] = 'smtp-mail.outlook.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME') 
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = "environmeet@outlook.com"
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)


# Temp Media Storage
UPLOAD_FOLDER = 'app/static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Actual Media Storage
imagekit = ImageKit(
    private_key=os.environ.get('imgkit_private_key'),
    public_key=os.environ.get('imgkit_public_key'),
    url_endpoint=os.environ.get('imgkit_url_endpoint'),
)


# Verification
app.config['SECURITY_PASSWORD_SALT'] = os.environ.get('SECURITY_PASSWORD_SALT') 

csrf = CSRFProtect(app)

# Socket
socketio = SocketIO(app, cors_allowed_origins='*')

#Session
app.config['APP_SECRET_KEY']=os.environ.get('app_secret_key')
app.permanent_session_lifetime = timedelta(minutes=60)  # Set session timeout to 30 minutes

# Pass variables to base template
@app.context_processor
def utility_processor():
    return dict(user=current_user, orgObj=Organisations)

from app import routes
from app.util import filters