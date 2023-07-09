from app import app
from datetime import datetime

@app.template_filter('formatTimestamp')
def format_timestamp(theTimestamp):
    return theTimestamp.strftime('%A, %d %B %Y, %I:%M%p')


@app.template_filter('isinstance')
def jinja2_isinstance(obj, classinfo):
    return isinstance(obj, classinfo)