from flask import make_response, render_template
from flask_limiter import Limiter, RequestLimit
from app import app
from flask_limiter.util import get_remote_address
from flask.json import jsonify
import os


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
    # storage_uri=f'redis://{os.environ.get("redis_user")}:{os.environ.get("redis_password")}@redis-15175.c252.ap-southeast-1-1.ec2.cloud.redislabs.com:15175',
    # storage_uri='memory://', # For testing only change to db 
    on_breach=exceed_rate_responder,
)


# @limiter.request_filter
# def rate_limit_filter():
#     return RateLimit.query.filter_by(ip=get_remote_address()).first()