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


def parse_time(time_str):
    """Generates today datetime from a HH:MM formatted time."""
    now = datetime.now()
    hour_str, minutes_str = time_str.split(':')
    return datetime(
        now.year, now.month, now.day, int(hour_str), int(minutes_str))


def parse_response(content, valid_stations):
    """Parse the content response."""
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


def get_train_datetime(item):
    """Parse the train time of arrival."""
    time_str = item['status'] if ':' in item['status'] else item['time']
    return parse_time(time_str)


def update_schedule(item):
    """Add more detail to the schedule.."""
    item['destination'] = item['destination'].upper()
    train_datetime = get_train_datetime(item)
    time_diff = train_datetime - datetime.now()
    home_departure = time_diff.total_seconds() - STATION_COMMUTE
    if home_departure > 0:
        depart_in = 'Depart in %s mins.' % int((home_departure / 60))
    else:
        minutes = int(time_diff.total_seconds() / 60)
        depart_in = ('Unlikely. Train in %s mins.' % minutes)
    item['depart_in'] = depart_in
    return item


def get_timetable(shortcode, valid_stations):
    """Prepares the timetable to be rendered."""
    url = '%s%s' % (URL_PREFIX, shortcode)
    response = requests.get(url, headers=HEADERS)
    if not response.status_code == 200:
        response = requests.get(url, headers=HEADERS)
    raw_timetable = parse_response(response.content, valid_stations)
    return map(update_schedule, raw_timetable)
