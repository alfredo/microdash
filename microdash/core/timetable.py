import requests

from datetime import datetime
from BeautifulSoup import BeautifulSoup

USER_AGENT = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:31.0) '
              'Gecko/20100101 Firefox/31.0')
HEADERS = {
    'User-Agent': USER_AGENT,
}
URL_PREFIX = ('http://www.abelliogreateranglia.co.uk/travel-information'
              '/journey-planning/live-departures/station/')

# 7-8 minutes to commute to station
STATION_COMMUTE = 60 * 8


def get_datetime(now, time_str):
    hour_str, minutes_str = time_str.split(':')
    return datetime(
        now.year, now.month, now.day, int(hour_str), int(minutes_str))


def parse_response(content, valid_stations):
    columns = ['destination', 'time', 'status', 'origin', 'operator']
    soup = BeautifulSoup(content)
    timetable = []
    for row in soup.findAll('tr'):
        # Ignore header row:
        if row.find('th'):
            continue
        data = dict([(k, v.text) for k, v in zip(columns, row.findAll('td'))])
        # Ignore non related stations:
        if data['destination'].lower() in valid_stations:
            timetable.append(data)
    return timetable


def get_schedule(raw_timetable):
    now = datetime.now()
    for item in raw_timetable:
        item['destination'] = item['destination'].upper()
        train_datetime = get_datetime(now, item['time'])
        diff = train_datetime - now
        item['datetime'] = train_datetime
        home_departure = diff.total_seconds() - STATION_COMMUTE
        item['home_departure'] = home_departure
        if home_departure > 0:
            depart_in = 'Depart in %s mins.' % int((home_departure / 60))
        else:
            depart_in = ('Unlikely. Train in %s mins.'
                         % int(diff.total_seconds() / 60))
        item['depart_in'] = depart_in
    return raw_timetable


def get_timetable(shortcode, valid_stations):
    """Prepares the timetable."""
    url = '%s%s' % (URL_PREFIX, shortcode)
    response = requests.get(url, headers=HEADERS)
    if not response.status_code == 200:
        response = requests.get(url, headers=HEADERS)
    raw_timetable = parse_response(response.content, valid_stations)
    return get_schedule(raw_timetable)
