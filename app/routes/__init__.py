from app import app
from flask import render_template
from app.routes import feed, events, accounts, leaderboard, profile, helpers, attendance, report, chat
from flask.json import jsonify

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return ''

# Test Route
@app.route('/critical')
def raise_critical():
    app.logger.critical(f'Error: This is a test', extra={'security_relevant': False, 'http_status_code': 500})
    return jsonify({'logged': 'critical error test'}, 500)