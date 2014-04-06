import os
import textwrap
import requests

from BeautifulSoup import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont

from django.http import HttpResponse
from microdash.core import twitter

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
here = lambda *x: os.path.join(PROJECT_ROOT, '..', *x)
HEADER_FONT = here('fonts', 'Playfair_Display', 'PlayfairDisplay-Bold.ttf')
CONTENT_FONT = here('fonts', 'Open_Sans', 'OpenSans-Regular.ttf')

MARGIN_LEFT = 10
VALID_STATIONS = ['london liverpool street']
TWITTER_HANDLE = 'greateranglia'
USER_AGENT = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:31.0) '
              'Gecko/20100101 Firefox/31.0')
HEADERS = {
    'User-Agent': USER_AGENT,
}


def get_timetable(shortcode):
    url = ('http://www.abelliogreateranglia.co.uk/travel-information'
           '/journey-planning/live-departures/station/%s' % shortcode)
    response = requests.get(url, headers=HEADERS)
    if not response.status_code == 200:
        response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.content)
    columns = ['destination', 'time', 'status', 'origin', 'operator']
    timetable = []
    for row in soup.findAll('tr'):
        if row.find('th'):
            continue
        row_data = dict([(k, v.text) for k, v in zip(columns, row.findAll('td'))])
        timetable.append(row_data)
    return [d for d in timetable if d['destination'].lower() in VALID_STATIONS]


def get_dashboard_image(timetable):
    size = (600, 800)
    im = Image.new('L', size, 255)
    draw = ImageDraw.Draw(im)
    position = (MARGIN_LEFT, 10)
    font_header = ImageFont.truetype(HEADER_FONT, 40)
    text = "Forest Gate station"
    draw.text(position, text, 33, font=font_header)
    font_content = ImageFont.truetype(CONTENT_FONT, 18)
    for i, item in enumerate(timetable, start=1):
        position_y = 40 + (35 * i)
        destination_position = (MARGIN_LEFT, position_y)
        draw.text(destination_position, item['destination'], 33, font=font_content)
        time_position = (MARGIN_LEFT + 250, position_y)
        draw.text(time_position, item['time'], 33, font=font_content)
        status_position = (MARGIN_LEFT + 330, position_y)
        draw.text(status_position, item['status'], 33, font=font_content)
    position = (MARGIN_LEFT, 350)
    font_header = ImageFont.truetype(HEADER_FONT, 40)
    text = "@%s" % TWITTER_HANDLE
    draw.text(position, text, 33, font=font_header)
    timeline = twitter.get_user_timeline(
        TWITTER_HANDLE, count=50, exclude_replies='true')
    font_tweet = ImageFont.truetype(CONTENT_FONT, 17)
    font_tweet_date = ImageFont.truetype(CONTENT_FONT, 12)
    for i, item in enumerate(timeline[:4], start=1):
        position_y = 330 + (85 * i)
        date_position = (MARGIN_LEFT, position_y)
        draw.text(date_position, item['created_at'], 33, font=font_tweet_date)
        initial_text = position_y + 15
        for k, mini_text in enumerate(textwrap.wrap(item['text'], 70)):
            position_y = initial_text + (k* 20)
            tweet_position = (MARGIN_LEFT, position_y)
            draw.text(tweet_position, mini_text, 33, font=font_tweet)
    return im


def station_dashboard(request, shortcode='FOG'):
    timetable = get_timetable(shortcode)
    img = get_dashboard_image(timetable)
    response = HttpResponse(content_type='image/png')
    img.save(response, 'PNG')
    return response
