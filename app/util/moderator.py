import re
import requests

def moderate_msg(msg):

    urls = re.findall('(?:[-\w.]|(?:%[\da-fA-F]{2}))+', msg)

    if len(urls) > 5:
        return 'Too many links'
    
    for url in urls:
        
        if not url.startswith('http'):
            new_url = 'http://' + url
        
        response = requests.get(f'https://api.exerra.xyz/scam?url={new_url}')
        response_json = response.json()
        result = response_json['isScam']

        if result:
            msg = msg.replace(url, '[POTENTIALLY MALICIOUS LINK]')
            print(msg)

    return msg