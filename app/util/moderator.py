import re
import requests
from app import app
import bleach

def detect_phish(msg, flags):

    url_regex = r"""(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:\'\".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))"""
    urls = re.findall(url_regex, msg)

    if len(urls) > 5:
        app.logger.warning(f'Potential attemp to overload url moderator', extra={'security_relevant': True, 'http_status_code': 400, 'flagged': True})
        return 'Too many links'
    
    for url in urls:
        
        if not url.startswith('http'):
            new_url = 'http://' + url
        
        response = requests.get(f'https://api.exerra.xyz/scam?url={new_url}')
        response_json = response.json()
        result = response_json['isScam']

        if result:
            app.logger.warning(f'Potential malicious link sent: {url}', extra={'security_relevant': True, 'http_status_code': 400, 'flagged': True})
            msg = msg.replace(url, '[POTENTIALLY MALICIOUS LINK]')
            flags += 1
        
    return (msg, flags)


def detect_xss(msg, flags):
    xss_pattern = r'<script\b[^>]*>(.*?)<\/script>|on\w+="[^"]*"'
    result = bool(re.search(xss_pattern, msg, re.IGNORECASE))

    if result:
        app.logger.warning(f'Potential XSS attempt: {msg}', extra={'security_relevant': True, 'http_status_code': 400, 'flagged': True})
        flags += 1
    
    return flags


def detect_sql_injection(msg, flags):
    # This will likely trigger a lot of false positives, but it can be reviwed when logged
    sql_injection_pattern = r'\b(SELECT|INSERT|UPDATE|DELETE|FROM|WHERE|DROP|UNION|ORDER BY|GROUP BY)\b'
    result = bool(re.search(sql_injection_pattern, msg, re.IGNORECASE))

    if result:
        app.logger.warning(f'Potential SQL Injection attempt: {msg}', extra={'security_relevant': True, 'http_status_code': 400, 'flagged': True})
        flags += 1
    
    return flags


def detect_command_injection(msg, flags):
    # This will likely trigger a lot of false positives, but it can be reviwed when logged
    command_injection_pattern = r'[&|;`$]'
    result = bool(re.search(command_injection_pattern, msg, re.IGNORECASE))

    if result:
        app.logger.warning(f'Potential Command Injection attempt: {msg}', extra={'security_relevant': True, 'http_status_code': 400, 'flagged': True})
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