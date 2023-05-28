from app import app
from datetime import datetime

@app.template_filter('formatTimestamp')
def format_timestamp(theTimestamp):
    return theTimestamp.strftime('%A, %d %B %Y, %I:%M%p')