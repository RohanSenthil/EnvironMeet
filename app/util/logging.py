from app import app, log_client
import logging
from datetime import datetime


# Log Config
class OpenSearchLogHandler(logging.Handler):

    def __init__(self):
        super().__init__()


    def emit(self, record):
        log_message = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'message': self.format(record)
        }

        log_client.index(index=index_name, body=log_message, refresh=True)


with app.app_context():

    # connected = log_client.ping()
    connected = False

    if connected:

        print('\nSuccessfully connected to OpenSearch')

        index_name = 'audit-logs'
        index_exists = log_client.indices.exists(index=index_name)

        if not index_exists:
            log_client.indices.create(index_name)
            print('\nCreating index...')
        else:
            print('\nIndex exists...skipping creation...')

        app.logger.handlers = []
        log_handler = OpenSearchLogHandler()
        app.logger.addHandler(log_handler)
        app.logger.setLevel(logging.INFO)

    else:
        print('\nFailed to connect to OpenSearch')



