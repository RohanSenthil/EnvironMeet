from PIL import Image
import random
from sklearn.metrics import mean_squared_error
import numpy as np
import imghdr
import requests
import os
from app import app
from flask import request, abort
import time
import json


def scan_file(file_data):

    url = 'https://www.virustotal.com/vtapi/v2/file/scan'
    params = {'apikey': os.environ.get('virustotal_api_key')}
    files = {'file': file_data}

    response = requests.post(url, files=files, params=params)
    response_json = response.json()
    
    if 'resource' in response_json:
        resource = response_json['resource']
        result = isFileMalicious(resource)
        return result
    else:
        return 'Scan request failed'
    

def isFileMalicious(resource):

    # Prevent exceeding rate limit
    max_attempts = 3
    poll_interval = 20
    
    for attempt in range(max_attempts):

        try:
            url = 'https://www.virustotal.com/vtapi/v2/file/report'
            params = {'apikey': os.environ.get('virustotal_api_key'), 'resource': resource}

            response = requests.get(url, params=params)
            response_json = json.loads(response.text)

            if 'positives' in response_json:
                positives = response_json['positives']
                if positives > 0:
                    app.logger.warning('Possible attempt to upload a malicious file', extra={'security_relevant': True, 'http_status_code': 415})
                    return True
                else:
                    return False
            elif 'response_code' in response_json and response_json['response_code'] <= 1:
                time.sleep(poll_interval)
            else:
                return 'Unable to retrieve scan results'
        except Exception as e:
            return f'Reached API Rate Limit, {e}'
        
    return 'Timeout: Analysis did not complete within the given number of attempts.'


def file_is_image(stream):
    header = stream.read(512)
    stream.seek(0)
    format = imghdr.what(None, header)

    if not format:
        app.logger.warning('Possible client side validation bypass', extra={'security_relevant': True, 'http_status_code': 415})
        return False
    
    if format not in ['jpeg', 'jpg', 'png']:
        app.logger.warning('Possible client side validation bypass', extra={'security_relevant': True, 'http_status_code': 415})
        return False
    
    return ('.' + (format if format != 'jpeg' else 'jpg')) in ['.jpg', '.png']


def randomize_image(og_image):

    random.seed(42)

    randomized_image = Image.new('RGB', og_image.size)
    og_image_rgb = og_image.convert('RGB')

    max_variation = 20
    similarity_threshold = 0.975

    for x in range(og_image_rgb.width):
        for y in range(og_image_rgb.height):
            pixel = og_image_rgb.getpixel((x, y))

            randomized_pixel = (
                pixel[0] + random.randint(-max_variation, max_variation),
                pixel[1] + random.randint(-max_variation, max_variation),
                pixel[2] + random.randint(-max_variation, max_variation),
            )

            randomized_pixel = tuple(max(0, min(255, val)) for val in randomized_pixel)

            randomized_image.putpixel((x, y), randomized_pixel)


    randomized_image = randomized_image.resize(og_image_rgb.size)

    og_array = np.array(og_image_rgb)
    randomized_array = np.array(randomized_image)

    mse = mean_squared_error(og_array.flatten(), randomized_array.flatten())
    similarity = 1 - (mse / (255 ** 2))

    if similarity < similarity_threshold:
        return randomize_image(og_image)

    return randomized_image


@app.before_request
def check_file_served():

    requested_path = request.path

    safe_locations = [rule.rule for rule in app.url_map.iter_rules()]

    if not any(requested_path.startswith(location) for location in safe_locations):
        app.logger.warning(f'Unauthorized file serving attempt: {requested_path}', extra={'security_relevant': True, 'http_status_code': 403})
        abort(403)  
