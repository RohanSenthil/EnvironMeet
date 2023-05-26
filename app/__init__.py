from flask import Flask
from flask_migrate import Migrate
from database.models import db
from database.tools import generate_uri_from_file

app = Flask(__name__)

db_uri = generate_uri_from_file('database/db_config.yml')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

db.init_app(app)
with app.app_context():
    db.create_all()

migrate = Migrate(app, db)

from app import routes