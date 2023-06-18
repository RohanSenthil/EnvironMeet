import base64


def encode_url(data):
    data_bytes = data.encode('utf-8')
    encoded_bytes = base64.urlsafe_b64encode(data_bytes)
    encoded_data = encoded_bytes.decode('utf-8')

    return encoded_data


def decode_url(encoded_data):
    encoded_bytes = encoded_data.encode('utf-8')
    data_bytes = base64.urlsafe_b64decode(encoded_bytes)
    data = data_bytes.decode('utf-8')

    return data


def generateNativeLink(identifier, root):
    return f'{root}post/view/{encode_url(identifier)}'
