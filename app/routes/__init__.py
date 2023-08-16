from app import app
from flask import render_template, request, url_for
from app.routes import feed, events, accounts, leaderboard, profile, helpers, attendance, report, chat
from flask.json import jsonify
from flask_login import current_user

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return ''

@app.route('/flagged')
def flagged():
    redirect_url = request.referrer

    if not current_user.is_authenticated:
        redirect_url = url_for('login_')

    return render_template('flagged.html'), {'Refresh': f'10; url={redirect_url}'}

# Test Route
@app.route('/critical')
def raise_critical():
    app.logger.critical(f'Error: This is a test', extra={'security_relevant': False, 'http_status_code': 500})
    return jsonify({'logged': 'critical error test'}, 500)