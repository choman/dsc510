# DSC 510
# Week 12 (term project)
# Programming Assignment Week 12 (term project)
# Author: Chad Homan
# 2021/02/03
#
# -*- coding: utf-8 -*-
#
# Abstract: For your class project we will be creating an application to
#           interacts with a webservice in order to obtain data. Your
#           program will use all of the information you have learned in the
#           class in order to create a useful application.
#           Your program must prompt the user for their city or zip code
#           and request weather forecast data from OpenWeatherMap. Your
#           program must display the weather information in a READABLE
#           format to the user.
#
# Requirements:
#
#   - Create a header for your program just as you have in the past.
#   - Create a Python Application which asks the user for their zip code
#     or city.
#   - Use the zip code or city name in order to obtain weather forecast
#     data from OpenWeatherMap.
#   - Display the weather forecast in a readable format to the user.
#   - Use comments within the application where appropriate in order to
#     document what the program is doing.
#   - Use functions including a main function.
#   - Allow the user to run the program multiple times to allow them to
#     look up weather conditions for multiple locations.
#   - Validate whether the user entered valid data. If valid data is not
#     presented notify the user.
#   - Use the Requests library in order to request data from the webservice.
#        * Use Try blocks to ensure that your request was successful. If
#          the connection was not successful display a message to the user.
#   - Use Python 3
#   - Use try blocks when establishing connections to the webservice. You
#     must print a message to the user indicating whether or not the
#     connection was successful
#
# Record Of Modifications
#    Author         Date            Description
#  ----------    ------------       ----------------------------------
#  Chad Homan     2021-02-28        Added cardinal wind direction
#
#  Chad Homan     2021-02-17        added welcome() message
#  Chad Homan     2021-02-12        added dynamic print for weather types
#                                   added print_debug()
#                                   added docstrings
#  Chad Homan     2021-02-11        added hPa to inch convert
#                                   added degree symbol
#                                   working on both zipcode and no zipcode
#                                   Initial output display
#  Chad Homan     2021-02-08        primary header
#

import json
import random
import requests
import sys
import time

try:
    import uszipcode
    USE_USZIPCODE = True

except ModuleNotFoundError:
    print('Proceeding w/o uszipcode module')
    USE_USZIPCODE = False

QUIT         = 'q'
DEGREE_F     = chr(176) + 'F'
DEGREE       = chr(176)
HPA2INCH     = .02953
METER2MILE   = .000621371
MM2INCH      = .0393701
LJUST        = 20
RJUST        = 1
DEBUG        = False
UNITS        = 'imperial'
WEATHER_URL  = 'https://api.openweathermap.org/data/2.5/weather'
WEATHER_KEY  = 'af6ca8a2c9759b2d33ec039bd9c21bbd'
ZIPCODE_CODE = 'https://app.zipcodebase.com/api/v1/search'
ZIPCODE_CITY = 'https://app.zipcodebase.com/api/v1/code/city'
ZIPCODE_KEY  = '823b29f0-6fb2-11eb-af5d-b780351b2eba'

states = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}

wind_dirs = [
    'N', 'NNE', 'NE', 'ENE',
    'E', 'ESE', 'SE', 'SSE',
    'S', 'SSW', 'SW', 'WSW',
    'W', 'WNW', 'NW', 'NNW'
    ]


# function: main()
# abstract: Main program
#
def main():
    welcome()
    getLocation()


def welcome():
    print()
    print("Welcome for Chad's Weather Machine")
    print('Follow the directions, press <enter>')
    print('on a line by itself to leave')


# function: getLocation()
# abstract: Get a location to obtain weather info
#
def getLocation():
    search = None

    if USE_USZIPCODE:
        search = uszipcode.SearchEngine(simple_zipcode=True)

    while True:
        print()
        location = input('Enter location (<zip> or <city, state>): ').strip()

        if location.lower() in QUIT:
            sys.exit()

        zipinfo = verifyLocation(location, search)
        print_debug("zipinfo = {zipinfo}")

        if zipinfo:
            weather_info = getWeather(zipinfo)
            display_Weather(weather_info, zipinfo)

    print_debug(f'location = {location}')
    return zipinfo


def getWeather(zip):
    """Get wether info from openweather map"""

    url_data = {
        'units': UNITS,
        'appid': WEATHER_KEY,
        'zip':   zip['zipcode'],
    }

    print_debug(f'url = {WEATHER_URL}')
    print_debug(f'url_data = {url_data}')

    data = getInfo(WEATHER_URL, params=url_data)
    return data


def print_debug(msg):
    """simple debug messages"""
    if DEBUG:
        print(f'DEBUG: {msg}')


def display_Weather(weather, zipinfo):
    """driver for weather display"""
    temps = weather['main']
    print_calls = {
        'humidity':   print_humidity,
        'pressure':   print_pressure,
        'temp_max':   print_temp_max,
        'temp_min':   print_temp_min,
        'feels_like': print_feels_like,
        'temp':       print_temp,
        'visibility': print_visibility,
        'wind':       print_wind,
        'clouds':     print_clouds,
        'sys':        print_sys,
        'snow':       print_snow_rain,
        'rain':       print_snow_rain,
    }

    print_debug(weather)
    print_debug(weather['weather'])
    print_debug(weather['main'])

    print()
    wheader = (
      f"Current weather in {zipinfo['city']}, "
      f"{zipinfo['state']} {zipinfo['zipcode']}:\n"
    )
    print(wheader)

    print_debug(temps)
    for k, v in temps.items():
        if k in print_calls:
            print_calls[k](k, v)

    print()
    print_desc(weather)

    for k, v in weather.items():
        if k in print_calls:
            print_calls[k](k, v)


def print_desc(weather):
    """Prepare and display weather description info"""
    key = format_title('Description')
    for desc in weather['weather']:
        print(f"{key:<{LJUST}}{desc['description'].capitalize()}")


def format_title(key):
    """Prepare description field for values"""
    key = f' {key.title()}:'
    return key


def print_humidity(key, value):
    """Prepare and display humidity info"""
    key = format_title(key)
    print(f'{key:<{LJUST}}{value:>{RJUST}}%')


def print_pressure(key, value):
    """Prepare and display pressure info"""
    key = format_title(key)
    value = f'{value * HPA2INCH:.2f}in'
    print(f'{key:<{LJUST}}{value:>{RJUST}}')


def print_temp(key, value):
    """Prepare and display various temp info"""
    key = format_title(key)
    value = f'{value}{DEGREE_F}'
    print(f'{key:<{LJUST}}{value:>{RJUST}}')


def print_feels_like(key, value):
    """Prepare feels like temp info"""
    print_temp('Feels Like', value)


def print_temp_max(key, value):
    """Prepare high temp info"""
    print_temp('High', value)


def print_temp_min(key, value):
    """Prepare low temp info"""
    print_temp('Low', value)


def print_visibility(key, value):
    """Prepare and display visibility info"""
    key = format_title(key)
    value = f'{value * METER2MILE:.2f}mi'
    print(f'{key:<{LJUST}}{value:>{RJUST}}')


def print_wind(key, value):
    """Prepare and display wind info"""
    key = format_title(key)
    cardinal_direction = getWindDirection(value['deg'])

    direction = f'Direction: {cardinal_direction}'
    svalue = f"{value['speed']}mph"
    print(f'{key:<{LJUST}}{svalue:>{RJUST}}')

    key = format_title("Wind Direction")
    svalue = f"{cardinal_direction} - {value['deg']}{DEGREE}"
    print(f'{key:<{LJUST}}{svalue:>{RJUST}}')


def print_clouds(key, value):
    """Prepare and display cloud info"""
    key = format_title(key)
    value = f"{value['all']}%"
    print(f'{key:<{LJUST}}{value:>{RJUST}}')


def print_snow_rain(key, value):
    """Prepare and display snow/rain info"""
    key = format_title(key)
    for k, v in value.items():
        value = f'{k}: {v * MM2INCH:.2f}in'
        print(f'{key:<{LJUST}}{value:>{RJUST}}')


def print_sys(key, value):
    """Prepare display of the sunrise/sunset"""
    print_riseset('Sunrise', value['sunrise'])
    print_riseset('Sunset', value['sunset'])


def print_riseset(title, value):
    """Actual display of the sunrise/sunset"""
    key = format_title(title)
    value = time.strftime('%H:%M', time.localtime(value))
    print(f'{key:<{LJUST}}{value:>{RJUST}}')


def verifyLocation(loc, search=None):
    """Verify the location entered by the user"""
    warn_msg = 'WARNING: Please enter valid <city, state> or <zipcode>'

    if search is None:
        zipinfo = verifyLocationByURL(loc)
    else:
        zipinfo = verifyLocationByAPI(loc, search)

    if zipinfo is None:
        print(warn_msg)

    return zipinfo


def verifyLocationByAPI(loc, search):
    if loc.isdigit() and len(loc) == 5:
        zipinfo = search.by_zipcode(loc)

        if zipinfo.zipcode is None:
            return None

        zipinfo = normalize_zipinfo(zipinfo=zipinfo)

    elif ',' in loc:
        city, state = loc.split(',')
        city  = city.strip()
        state = state.strip()

        try:
            zipinfo = random.choice(search.by_city_and_state(city, state))

        except IndexError:
            return None

        if zipinfo.zipcode is None:
            return None

        zipinfo = normalize_zipinfo(zipinfo=zipinfo)

    else:
        zipinfo = None

    return zipinfo


def getWindDirection(degree):
    ix = round(degree / (360 / len(wind_dirs)))
    return wind_dirs[ix % len(wind_dirs)]


def verifyLocationByURL(loc):
    headers = {
        'apikey': ZIPCODE_KEY,
    }

    if loc.isdigit() and len(loc) == 5:
        zipinfo = loc
        params = (
            ('codes', f'{loc}'),
            ('country', 'us'),
        )

        zipinfo = getInfo(ZIPCODE_CODE, headers=headers, params=params)

        if not len(zipinfo['results']):
            zipinfo = None

        else:
            zipinfo = normalize_zipinfo(zipinfo=zipinfo)

    elif ',' in loc:
        city, state = loc.split(',')
        city  = city.strip()
        state = state.strip()

        zipinfo = f'{city},{state}'
        params = (
            ('city', f'{city.capitalize()}'),
            ('state_name', f'{states.get(state.upper(), None)}'),
            ('country', 'us'.upper()),
        )

        zipinfo = getInfo(ZIPCODE_CITY, headers=headers, params=params)
        if not len(zipinfo['results']):
            zipinfo = None
        else:
            zipinfo = normalize_zipinfo(zipinfo=zipinfo)

    return zipinfo


def normalize_zipinfo(zipinfo=None):
    data = {}

    if zipinfo is None:
        return zipinfo

    if USE_USZIPCODE:
        data['city'] = zipinfo.major_city
        data['state'] = zipinfo.state
        data['zipcode'] = zipinfo.zipcode

    elif 'query' in zipinfo:
        if 'city' in zipinfo['query']:
            data['city'] = zipinfo['query']['city']
            data['state'] = searchByState(zipinfo['query']['state'])
            data['zipcode'] = random.choice(zipinfo['results'])

        elif 'codes' in zipinfo['query']:
            code = zipinfo['query']['codes'][0]
            data['city'] = zipinfo['results'][code][0]['city']
            data['state'] = searchByState(zipinfo['results'][code][0]['state'])
            data['zipcode'] = zipinfo['results'][code][0]['postal_code']

        else:
            data = None

    else:
        data = None

    return data


def searchByState(state):
    for key, value in states.items():
        if state in value:
            return key.capitalize()


def getInfo(url, headers=None, params=None):
    try:
        result = requests.get(url, headers=headers, params=params)
        result.raise_for_status()

    except requests.exceptions.ConnectionError as err:
        raise SystemExit(err)

    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)

    except requests.exceptions.RequestException as err:
        raise SystemExit(err)

    else:
        data =  json.loads(result.content)
        return data


if __name__ == '__main__':
    try:
        main()

    except KeyboardInterrupt:
        print()
