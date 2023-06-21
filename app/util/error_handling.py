from flask import make_response, render_template
from flask_limiter import RequestLimit


def exceed_rate_responder(requestLimit = RequestLimit):
    return make_response(render_template('rateLimit.html', requestLimit=requestLimit), 429)