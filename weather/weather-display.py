#!/usr/bin/env python
from subprocess import call
from datetime import datetime

URL = 'http://microdash.herokuapp.com/FOG/'
OUTPUT_FILE = '/mnt/us/weather/weather-script-output.png'


def clear_screen():
    call('/usr/sbin/eips -c', shell=True)


def get_dashboard(url, output_file):
    call('rm %s' % output_file, shell=True)
    call('wget -O "%s" "%s"' % (output_file, url), shell=True)


def set_dashboard_background(image_path):
    call('eips -g %s' % image_path, shell=True)


def main():
    now = datetime.now()
    # Only execute after 6 and before 10:
    if (now.hour >= 5) and (now.hour <= 11):
        clear_screen()
        get_dashboard(URL, OUTPUT_FILE)
        set_dashboard_background(OUTPUT_FILE)


if __name__ == "__main__":
    main()
