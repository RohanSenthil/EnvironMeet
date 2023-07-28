from app import app, log_client
from faker import Faker
import random
from datetime import datetime
import hashlib
import json
import time

fake = Faker()

def generate_status_code_weights(choices):

    weights = []

    for code in choices:
        if code in [400, 401, 403, 404, 405, 429]:
            weights.append(50)
        elif code in [500, 501, 502, 503, 504, 415]:
            weights.append(40)
        elif code in [402, 408]:
            weights.append(30)
        else:
            weights.append(10)

    return weights

def generate_sample_log_data():

    status_code_choices = [x for x in range(400, 452)] + [x for x in range(500, 511)]
    status_code_weights = generate_status_code_weights(status_code_choices)

    log_time = fake.date_time_between(start_date='-30d', end_date='now').isoformat()
    log_ip = fake.ipv4()

    log_message = {
        'when': {
            'timestamp': log_time,
            'event_timestamp': log_time,
        },
        'where': {
            'application_address': '127.0.0.1:5000',
            'page': fake.uri_path(),
            'code_location': fake.file_path(),
            'referer': fake.uri(),
        },
        'who': {
            'ip_address': log_ip,
            'source_address': log_ip,
            'user_identity': random.randint(1, 250),
        },
        'what': {
            'event': random.choice(['WARNING', 'ERROR', 'CRITICAL']),
            'severity': random.choice([30, 40, 50]),
            'security_relevant': fake.boolean(),
            'message': f'Sample Log Data: {fake.text()}',
            'http_status_code': random.choices(status_code_choices, weights=status_code_weights, k=1),
            'user_agent': fake.user_agent(),
        },
    }

    log_message['hash'] = hashlib.sha256(json.dumps(log_message).encode()).hexdigest()

    try:
        log_client.index(index='audit-logs', body=log_message, refresh=True)
        return 'logged'
    except Exception as e:
        return 'error'
    

def generate_sample_logs(num_records):
    for i in range(num_records):
        try:
            generate_sample_log_data()
            time.sleep(10)
        except Exception as e:
            return f'error: {e}'

    return 'success'