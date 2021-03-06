import os
import textwrap

from PIL import Image, ImageDraw, ImageFont

from django.http import HttpResponse
from microdash.core import twitter, timetable

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
here = lambda *x: os.path.join(PROJECT_ROOT, '..', *x)
HEADER_FONT = here('fonts', 'Playfair_Display', 'PlayfairDisplay-Bold.ttf')
CONTENT_FONT = here('fonts', 'Dosis', 'Dosis-Regular.ttf')
CONTENT_BOLD_FONT = here('fonts', 'Dosis', 'Dosis-ExtraBold.ttf')


MARGIN_LEFT = 20
VALID_STATIONS = ['london liverpool street']
TWITTER_HANDLE = 'greateranglia'


def get_dashboard_image(size):
    """Prepare canvas to render image."""
    im = Image.new('L', size, 255)
    return im


def draw_station(draw, station):
    """Draw the station name."""
    position = (MARGIN_LEFT, 10)
    font = ImageFont.truetype(HEADER_FONT, 40)
    draw.text(position, station, 33, font=font)
    return draw


def draw_timetable(draw, timetable_list, limit=4):
    """Draw the timetable."""
    font_s = ImageFont.truetype(CONTENT_FONT, 15)
    font_m = ImageFont.truetype(CONTENT_FONT, 25)
    font_xl = ImageFont.truetype(CONTENT_BOLD_FONT, 40)
    module_position = 75
    row_height = 75
    # Fields and position:
    attrs = [
        ('destination', (0, 0), font_s),
        ('time', (0, 12), font_xl),
        ('depart_in', (95, 26), font_m),
        ('status', (400, 0), font_m),
    ]
    for i, item in enumerate(timetable_list[:limit]):
        for name, row_position, font in attrs:
            row_x, row_y = row_position
            position_y = module_position + row_y + (row_height * i)
            position_x = MARGIN_LEFT + row_x
            draw.text((position_x, position_y), item[name], 33, font)
    return draw


def draw_timeline(draw, timeline, limit=4):
    """Draw the twitter timeline."""
    module_position = 380
    font_header = ImageFont.truetype(HEADER_FONT, 35)
    draw.text((MARGIN_LEFT, module_position),
              "@%s" % TWITTER_HANDLE, 33, font=font_header)
    font = ImageFont.truetype(CONTENT_FONT, 20)
    font_date = ImageFont.truetype(CONTENT_FONT, 14)
    tweets_position = module_position + 50
    tweet_height = 60
    for i, item in enumerate(timeline[:limit]):
        position_y = tweets_position + (tweet_height * i)
        date_position = (MARGIN_LEFT, position_y)
        offset_text = position_y + 15
        for k, mini_text in enumerate(textwrap.wrap(item['text'], 70)):
            position_y = offset_text + (k * 22)
            tweet_position = (MARGIN_LEFT, position_y)
            mini_text = mini_text.replace('&amp;', '&')
            draw.text(tweet_position, mini_text, 33, font=font)
    return draw


def station_dashboard(request, shortcode='FOG'):
    size = (600, 800)
    img = get_dashboard_image(size)
    draw = ImageDraw.Draw(img)
    station = "Forest Gate station"
    draw = draw_station(draw, station)
    timetable_list = timetable.get_timetable(shortcode, VALID_STATIONS)
    draw = draw_timetable(draw, timetable_list)
    timeline = twitter.get_user_timeline(
        TWITTER_HANDLE, count=50, exclude_replies='true')
    draw = draw_timeline(draw, timeline)
    response = HttpResponse(content_type='image/png')
    img.save(response, 'PNG')
    return response
