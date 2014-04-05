from PIL import Image, ImageDraw

from django.http import HttpResponse


def get_image():
    size = (600, 800)
    im = Image.new('L', size, 255)
    draw = ImageDraw.Draw(im)
    position = (10, 10)
    text = "Hello World!"
    draw.text(position, text, 33)
    return im


def station(request, shortcode=None):
    img = get_image()
    response = HttpResponse(content_type='image/png')
    img.save(response, 'PNG')
    return response
