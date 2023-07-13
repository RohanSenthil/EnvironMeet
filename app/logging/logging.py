from app import app, log_client
import logging
from datetime import datetime
from flask import request
from app.logging.index_mappings import audit_logs_mapping


# Log Config
class OpenSearchLogHandler(logging.Handler):

    def __init__(self):
        super().__init__()


    def emit(self, record):
        log_message = {

            'when': {
                'timestamp': datetime.utcnow().isoformat(),
                'event_timestamp': datetime.fromtimestamp(record.created).isoformat(),
            },
            'where': {
                'application_address': request.host,
                'geolocation': record.__dict__.get('geolocation'),
                'page': request.url,
                'code_location': record.filename,
            },
            'who': {
                'source_address': request.remote_addr,
                'user_identity': '',
            },
            'what': {
                'event': record.levelname,
                'severity': record.levelno,
                'security_relevant': True,
                'message': self.format(record),
                'http_status_code': '',
                'http_headers': dict(request.headers),
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



