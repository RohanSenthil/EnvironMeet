from app import app
from flask import render_template
from app.routes import feed

# Routes
@app.route('/')
def home():
    return render_template('index.html')
