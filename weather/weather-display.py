#!/usr/bin/env python
from subprocess import call

URL = 'http://microdash.herokuapp.com/FOG/'
OUTPUT_FILE = '/mnt/us/weather/weather-script-output.png'


def clear_screen():
    call('/usr/sbin/eips -c', shell=True)


def get_image():
    call('wget -O "%s" "%s"' % (OUTPUT_FILE, URL), shell=True)


def main():
    clear_screen()
    get_image()


if __name__ == "__main__":
    main()
