#!/usr/bin/env python3
"""Prints the weather at the command line."""

import json
import urllib
import sys
import geocoder
import os

# 5006 Valley Drive
DEFAULT_LATLNG = [38.630130, -76.516820]

home = os.path.expanduser("~")
data_dir = os.path.join(home, '.local/share/pyweather-lmr')
config = os.path.join(data_dir, "config.json")

print("Pyweather LMR")

os.makedirs(os.path.dirname(config), exist_ok=True)
try:
    with open(config, 'r') as f:
        api_key = json.load(f)["api_key"]
except FileNotFoundError:
    api_key = input("Enter Open Weather API Key: ")
    data = {
        "api_key": api_key
    }
    with open(config, 'w') as f:
        json.dump(data, f)


def ktof(k):
    """Converts Kelvin to Fahrenheit."""
    f = 9/5 * (k - 273) + 32
    return round(f)


def dtocard(d):
    """Converts degrees to cardinal direction."""
    c = ''
    if d >= 348.75 or d < 11.25:
        c = 'N'
    elif d < 33.75:
        c = 'NNE'
    elif d < 56.25:
        c = 'NE'
    elif d < 78.75:
        c = 'ENE'
    elif d < 101.25:
        c = 'E'
    elif d < 123.75:
        c = 'ESE'
    elif d < 146.25:
        c = 'SE'
    elif d < 168.75:
        c = 'SSE'
    elif d < 191.25:
        c = 'S'
    elif d < 213.75:
        c = 'SSW'
    elif d < 236.25:
        c = 'SW'
    elif d < 258.75:
        c = 'WSW'
    elif d < 281.25:
        c = 'W'
    elif d < 303.75:
        c = 'WNW'
    elif d < 326.25:
        c = 'NW'
    elif d < 348.75:
        c = 'NNW'

    return c


def beaufort(n):
    """Converts windspeed in m/s into Beaufort Scale descriptor."""
    s = ''
    if n < 0.3:
        s = 'calm'
    elif n < 1.6:
        s = 'light air'
    elif n < 3.4:
        s = 'light breeze'
    elif n < 5.5:
        s = 'gentle breeze'
    elif n < 8.0:
        s = 'moderate breeze'
    elif n < 10.8:
        s = 'fresh breeze'
    elif n < 13.9:
        s = 'strong breeze'
    elif n < 17.2:
        s = 'high wind'
    elif n < 20.8:
        s = 'gale'
    elif n < 24.5:
        s = 'strong gale'
    elif n < 28.5:
        s = 'storm'
    elif n < 32.7:
        s = 'violent storm'
    else:
        s = 'hurricane force'
    return s


def main():
    # get location
    try:
        g = geocoder.ip('me')  # returns [##.####, ##.####]
        [lat, lng] = g.latlng
        # location = g.city + ', ' + g.state
    except TypeError:
        [lat, lng] = DEFAULT_LATLNG

    # get weather from OpenWeatherMap API
    try:
        url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lng}&APPID={api_key}'
        urldata = urllib.request.urlopen(url)
        with urllib.request.urlopen(url) as url:
            data = json.loads(url.read().decode('utf-8'))
        urldata.close()
        temp = ktof(data['main']['temp'])
        # low = ktof(data['main']['temp_min'])
        temp = ktof(data['main']['temp_max'])
        windir = ''
        try:
            dtocard(data['wind']['deg'])
        except KeyError:
            pass
        windspeed = data['wind']['speed']
        wind = beaufort(windspeed) + ' ' + windir
        description = data['weather'][0]['main']
        print('{}\u00b0F, {}, {}'.format(temp, description, wind))
    except urllib.error.HTTPError:
        print('Unable to contact OpenWeather')



if __name__ == '__main__':
    main()
