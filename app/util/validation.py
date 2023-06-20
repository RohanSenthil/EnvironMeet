import magic
from PIL import Image
import random
from sklearn.metrics import mean_squared_error
import numpy as np
import imghdr

def file_is_image(stream):
    # mime_type = magic.from_file(filepath, mime=True)
    # return mime_type in ['image/jpeg', 'image/png']

    header = stream.read(512)
    stream.seek(0)
    format = imghdr.what(None, header)
    if not format:
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