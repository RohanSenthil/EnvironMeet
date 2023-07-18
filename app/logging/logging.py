from app import app, log_client
import logging
from datetime import datetime
from flask import request
from app.logging.index_mappings import audit_logs_mapping
from flask_login import current_user

# Example Usage
# app.logger.warning('Unauthorized attempt to delete', extra={'security_relevant': True, 'http_status_code': 401})
# Edit values to relevant values
# Typically .warning used, can also use .error or .critical etc. depending on context, refer to python logger levels

def get_current_user_id():
    print(current_user.is_authenticated)
    if current_user.is_authenticated:
        return current_user.id 
    else:
        return None


# Log Config
class OpenSearchLogHandler(logging.Handler):

    def __init__(self):
        super().__init__()


    def emit(self, record):
        print(record.__dict__)
        log_message = {
            'when': {
                'timestamp': datetime.utcnow().isoformat(),
                'event_timestamp': datetime.fromtimestamp(record.created).isoformat(),
            },
            'where': {
                'application_address': request.host,
                'ip_address': request.remote_addr,
                'page': request.url,
                'code_location': record.filename,
            },
            'who': {
                'source_address': request.environ.get('HTTP_X_FORWARDED_FOR') or request.remote_addr,
                'user_identity': get_current_user_id(),
            },
            'what': {
                'event': record.levelname,
                'severity': record.levelno,
                'security_relevant': record.security_relevant,
                'message': self.format(record),
                'http_status_code': record.http_status_code,
                'user_agent': request.headers.get('User-Agent'),
            },
        }

        log_client.index(index=index_name, body=log_message, refresh=True)


with app.app_context():

    # connected = log_client.ping()
    connected = False

    if connected:

        print('\nSuccessfully connected to OpenSearch')

        index_name = 'audit-logs'
        index_exists = log_client.indices.exists(index=index_name)

        # For Dev purposes only
        # log_client.indices.delete(index='audit-logs')

        if not index_exists:

            body = audit_logs_mapping

            log_client.indices.create(index_name, body=body)
            print('\nCreating index...')
        else:
            print('\nIndex exists...skipping creation...')

        app.logger.handlers = []
        log_handler = OpenSearchLogHandler()
        app.logger.addHandler(log_handler)
        app.logger.setLevel(logging.INFO)

    else:
        print('\nFailed to connect to OpenSearch')


# Handle global exceptions
# @app.errorhandler(Exception)
# def handle_global_exceptions(error):
#     app.logger.exception(f'Error: {error}', extra={'security_relevant': False, 'http_status_code': 500})

