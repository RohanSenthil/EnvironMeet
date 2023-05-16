from flask import Flask    
from flask_sqlalchemy import SQLAlchemy
from models import db
from tools import generate_uri_from_file

app = Flask(__name__)

db_uri = generate_uri_from_file('db_config.yml')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

db.init_app(app)
with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(port=8000, debug=True)
