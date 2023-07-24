from flask import make_response, render_template
from flask_limiter import Limiter, RequestLimit
from app import app
from flask_limiter.util import get_remote_address
from flask.json import jsonify
# from database.models import db, RateLimit
# import datetime


# def save_rate_limit_data(endpoint, limit, period):
#     rateLimit = RateLimit(
#         endpoint=endpoint,
#         ip=get_remote_address(),
#         limit=limit,
#         period=period,
#         last_hit=datetime.datetime.utcnow()
#     )

#     db.session.add(rateLimit)
#     db.session.commit()


def exceed_rate_responder(requestLimit = RequestLimit):
    # save_rate_limit_data(endpoint=endpoint, limit=requestLimit.limit, period=period)
    app.logger.warning(f'Exceeded Rate Limit: {requestLimit.limit}', extra={'security_relevant': True, 'http_status_code': 429})
    return jsonify({'error': 'Rate Limit Exceeded'})
    # return make_response(render_template('rateLimit.html', requestLimit=requestLimit), 429)


# Rate Limiting
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=['1 per second'],
    # storage_uri='memory://', # For testing only change to db 
    on_breach=exceed_rate_responder,
)


# @limiter.request_filter
# def rate_limit_filter():
#     return RateLimit.query.filter_by(ip=get_remote_address()).first()