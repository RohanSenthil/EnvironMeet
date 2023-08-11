import re
import requests
from app import app
import bleach

def detect_phish(msg, flags):

    urls = re.findall('(?:[-\w.]|(?:%[\da-fA-F]{2}))+', msg)

    if len(urls) > 5:
        app.logger.warning(f'Potential attemp to overload url moderator', extra={'security_relevant': True, 'http_status_code': 400})
        return 'Too many links'
    
    for url in urls:
        
        if not url.startswith('http'):
            new_url = 'http://' + url
        
        response = requests.get(f'https://api.exerra.xyz/scam?url={new_url}')
        response_json = response.json()
        result = response_json['isScam']

        if result:
            app.logger.warning(f'Potential malicious link sent: {url}', extra={'security_relevant': True, 'http_status_code': 400})
            msg = msg.replace(url, '[POTENTIALLY MALICIOUS LINK]')
            flags += 1
        
    return (msg, flags)


def detect_xss(msg, flags):
    xss_pattern = r'<script\b[^>]*>(.*?)<\/script>|on\w+="[^"]*"'
    result = bool(re.search(xss_pattern, msg, re.IGNORECASE))

    if result:
        app.logger.warning(f'Potential XSS attempt: {msg}', extra={'security_relevant': True, 'http_status_code': 400})
        flags += 1
    
    return flags


def detect_sql_injection(msg, flags):
    # This will likely trigger a lot of false positives, but it can be reviwed when logged
    sql_injection_pattern = r'\b(SELECT|INSERT|UPDATE|DELETE|FROM|WHERE|DROP|UNION|ORDER BY|GROUP BY)\b'
    result = bool(re.search(sql_injection_pattern, msg, re.IGNORECASE))

    if result:
        app.logger.warning(f'Potential SQL Injection attempt: {msg}', extra={'security_relevant': True, 'http_status_code': 400})
        flags += 1
    
    return flags


def detect_command_injection(msg, flags):
    # This will likely trigger a lot of false positives, but it can be reviwed when logged
    command_injection_pattern = r'[&|;`$]'
    result = bool(re.search(command_injection_pattern, msg, re.IGNORECASE))

    if result:
        app.logger.warning(f'Potential Command Injection attempt: {msg}', extra={'security_relevant': True, 'http_status_code': 400})
        flags += 1
    
    return flags


def moderate_msg(msg):

    flags = 0

    msg, flags = detect_phish(msg, flags)
    flags = detect_xss(msg, flags)

    # Comment out since will likley generate too much false positives and would require too much manual review to ascertain
    # flags = detect_sql_injection(msg, flags)
    # flags = detect_command_injection(msg, flags)

    msg = bleach.clean(msg)
        
    return (msg, flags)