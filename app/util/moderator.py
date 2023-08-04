import re
import requests
from app import app

def moderate_msg(msg):

    urls = re.findall('(?:[-\w.]|(?:%[\da-fA-F]{2}))+', msg)

    if len(urls) > 5:
        return 'Too many links'
    
    for url in urls:
        
        if not url.startswith('http'):
            app.logger.warning(f'Potential attemp to overload url moderator', extra={'security_relevant': True, 'http_status_code': 400})
            new_url = 'http://' + url
        
        response = requests.get(f'https://api.exerra.xyz/scam?url={new_url}')
        response_json = response.json()
        result = response_json['isScam']

        if result:
            app.logger.warning(f'Potential malicious link sent', extra={'security_relevant': True, 'http_status_code': 400})
            msg = msg.replace(url, '[POTENTIALLY MALICIOUS LINK]')
        
    return msg