import requests

from BeautifulSoup import BeautifulSoup

USER_AGENT = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:31.0) '
              'Gecko/20100101 Firefox/31.0')
HEADERS = {
    'User-Agent': USER_AGENT,
}

def get_timetable(shortcode, valid_stations):
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
    return [d for d in timetable if d['destination'].lower() in valid_stations]
