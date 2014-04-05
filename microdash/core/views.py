from PIL import Image, ImageDraw

from django.http import HttpResponse


def get_image():
    size = (600, 800)
    im = Image.new('RGBA', size, (255, 255, 255, 255))
    draw = ImageDraw.Draw(im)
    color = (0, 0, 0)
    position = (10, 10)
    text = "Hello World!"
    draw.text(position, text, fill=color)
    del draw
    return im


def station(request, shortcode=None):
    img = get_image()
    response = HttpResponse(mimetype='image/png')
    img.save(response, 'PNG')
    return response
