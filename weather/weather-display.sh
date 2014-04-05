#!/bin/sh
cd "$(dirname "$0")"
rm weather-script-output.png
wget -O "/mnt/us/weather/weather-script-output.png" "http://microdash.herokuapp.com/FOG/"
eips -c
eips -c
eips -g weather-script-output.png
