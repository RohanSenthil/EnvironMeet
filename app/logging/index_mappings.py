audit_logs_mapping = {
    'mappings': {
        'properties': {
            'when': {
                'properties' : {
                    'timestamp': { 'type' : 'date' },
                    'event-timestamp': { 'type' : 'date' },
                }
            },
            'where': {
                'properties': {
                    'application_address': { 'type' : 'keyword' },
                    'ip_address': { 'type' : 'keyword' },
                    'page': { 'type': 'keyword' },
                    'code_location': { 'type' : 'keyword' },
                }
            },
            'who': {
                'properties': {
                    'source_address': { 'type' : 'keyword' },
                    'user_identity': { 'type' : 'keyword' },
                }
            },
            'what': { 
                'properties': {
                    'event': { 'type' : 'keyword' },
                    'severity': { 'type' : 'integer' },
                    'security_relevant': { 'type' : 'boolean' },
                    'message': { 'type' : 'text' },
                    'http_status_code': { 'type' : 'keyword' },
                    'user_agent': { 'type' : 'keyword' },
                }
            },
        }
    }
}