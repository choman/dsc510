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
#  Chad Homan     2021-03-02        Implemented a template for docstrings
#                                   Corrected hPa math to X in water
#                                   added logic for metric and standard
#                                   added wind arrow - unicode
#                                   sanity check on loc
#  Chad Homan     2021-02-28        Added cardinal wind direction
#                                   assistance from: https://bit.ly/2PskWDi
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

import datetime
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

USE_ARROWS   = True
QUIT         = 'q'
DEGREE       = chr(176)
HPA2INCH     = .401463
HPA2CM       = 1.01972
METER2MILE   = .000621371
MM2INCH      = .0393701
LJUST        = 20
RJUST        = 1
DEBUG        = False
WEATHER_URL  = 'https://api.openweathermap.org/data/2.5/weather'
WEATHER_KEY  = 'af6ca8a2c9759b2d33ec039bd9c21bbd'
ZIPCODE_CODE = 'https://app.zipcodebase.com/api/v1/search'
ZIPCODE_CITY = 'https://app.zipcodebase.com/api/v1/code/city'
ZIPCODE_KEY  = '823b29f0-6fb2-11eb-af5d-b780351b2eba'

IMPERIAL     = 'imperial'  # fahrenhite
METRIC       = 'metric'    # celcius
STANDARD     = 'standard'  # kelvin

DEGREES = {
   IMPERIAL: f'{DEGREE}F',
   METRIC:   f'{DEGREE}C',
   STANDARD: f'{DEGREE}K',
}

STATES = {
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

WIND_DIRS = [
    'N', 'NNE', 'NE', 'ENE',
    'E', 'ESE', 'SE', 'SSE',
    'S', 'SSW', 'SW', 'WSW',
    'W', 'WNW', 'NW', 'NNW'
]

# cardinal direction arrows in unicode
if USE_ARROWS:
    WIND_ARROWS = [
        '\u2193', '\u2199', '\u2199', '\u2199',
        '\u2190', '\u2196', '\u2196', '\u2196',
        '\u2191', '\u2197', '\u2197', '\u2197',
        '\u2192', '\u2198', '\u2198', '\u2198'
    ]


# function: main()
# abstract: Main program
#
def main():
    welcome()
    getLocation()


def welcome():
    print()
    print("Welcome for Chad's Weather Machine!")
    print()
    print('Follow the directions')
    print('   - All output is in imperial format')
    print('   - if Celsius is chosen, output is in metric')
    print('   - if Kelvin is chosen, temps only are in Kelvin')
    print()
    print('To exit, press <enter> on a line by itself to leave')


# function: getLocation()
# abstract: Get a location to obtain weather info
#
def getLocation():
    """Loop that queries user for location of weather info

    Returns:
        Nothing
    """
    search = None

    if USE_USZIPCODE:
        search = uszipcode.SearchEngine(simple_zipcode=True)

    while True:
        location = requestWeatherLocation()
        units = requestWeatherType()

        zipinfo = verifyLocation(location, search)
        print_debug(f'zipinfo = {zipinfo}')

        if zipinfo:
            weather_info = getWeather(zipinfo, units)
            display_Weather(weather_info, zipinfo, units)

    print_debug(f'location = {location}')


def requestWeatherLocation():
    """Get weather location

    Returns:
        location (string): location city/state || zip
    """
    print()
    print()
    location = input('Enter location (<zip> or <city, state>): ').strip()

    if location.lower() in QUIT:
        sys.exit()

    return location


def requestWeatherType():
    """get weather type (imperial, metric, kelvin/standard)

    Returns:
        units (string): weather type
    """
    print()
    print('How would you like to view the weather?')
    view = input('(F)ahrenheit, (C)elsius, (K)elvin [F]: ').strip()

    if 'k' in view.lower():
        units = STANDARD

    elif 'c' in view.lower():
        units = METRIC

    else:
        units = IMPERIAL

    return units


def getWeather(zip, units=IMPERIAL):
    """Get wether info from openweather map

    Args:
        zip (int): zipdata

    Returns:
        data (dict): weather data
    """
    url_data = {
        'units': units,
        'appid': WEATHER_KEY,
        'zip':   zip['zipcode'],
    }

    print_debug(f'url = {WEATHER_URL}')
    print_debug(f'url_data = {url_data}')

    data = getInfo(WEATHER_URL, params=url_data)
    return data


def print_debug(msg):
    """simple debug messages

    Args:
        msg (data): info to print debug

    Returns:
        Nothing
    """
    if DEBUG:
        print(f'DEBUG: {msg}')


def display_Weather(weather, zipinfo, units=IMPERIAL):
    """driver for weather display

    Args:
        weather (dict): weather data
        zipinfo (dict): location data

    Returns:
        Nothing
    """
    temps = weather['main']
    print_calls = {
        'humidity':   print_humidity,
        'pressure':   print_pressure,
        'grnd_level': print_grnd_level,
        'sea_level':  print_sea_level,
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
      f"{zipinfo['state']} {zipinfo['zipcode']} "
      f"({weather['coord']['lon']}/{weather['coord']['lat']}):\n"
    )
    print(wheader)

    print_debug(temps)
    for k, v in temps.items():
        if k in print_calls:
            print_calls[k](k, v, units)

    print()
    print_desc(weather)

    tz = weather['timezone']

    for k, v in weather.items():
        if k in print_calls:
            if 'sys' in k:
                print_calls[k](k, v, units, tz)
            else:
                print_calls[k](k, v, units)


def print_desc(weather):
    """Prepare and display weather description info

    Args:
        weather (list): weather descriptions

    Returns:
         nothing
    """
    key = format_title('Description')
    for desc in weather['weather']:
        extra = f"{desc['description'].capitalize()}"
        print(f"{key:<{LJUST}}{desc['main']}, {extra}")


def format_title(key):
    """Prepare description field for values

    Args:
        key (string): description of data

    Returns:
        (string): formatted
    """
    return f' {key.title()}:'


def print_humidity(key, value, units=IMPERIAL):
    """Prepare and display humidity info

    Args:
        key (string): description of data
        value (float): percentage of humidity

    Returns:
        Nothing
    """
    key = format_title(key)
    print(f'{key:<{LJUST}}{value:>{RJUST}}%')


def print_sea_level(key, value, units=IMPERIAL):
    """Prepare and display pressure info

    Args:
        key (string): description of data
        value (float): pressure data in HPA

    Returns:
        Nothing
    """
    print_pressure('Sea Level', value, units=IMPERIAL)


def print_grnd_level(key, value, units=IMPERIAL):
    """Prepare and display pressure info

    Args:
        key (string): description of data
        value (float): pressure data in HPA

    Returns:
        Nothing
    """
    print_pressure('Ground Level', value, units=IMPERIAL)


def print_pressure(key, value, units=IMPERIAL):
    """Prepare and display pressure info

    Args:
        key (string): description of data
        value (float): pressure data in HPA

    Returns:
        Nothing
    """
    key = format_title(key)

    if METRIC in units:
        value = f'{value}hPa ({value * HPA2CM:.2f}cm)'

    else:
        value = f'{value}hPa ({value * HPA2INCH:.2f}in)'

    print(f'{key:<{LJUST}}{value:>{RJUST}}')


def print_temp(key, value, units=IMPERIAL):
    """Prepare and display various temp info

    Args:
        key (string): description of data
        value (float): temp

    Returns:
        Nothing
    """
    key = format_title(key)
    value = f'{value}{DEGREES[units]}'
    print(f'{key:<{LJUST}}{value:>{RJUST}}')


def print_feels_like(key, value, units=IMPERIAL):
    """Prepare feels like temp info

    Args:
        key (string): description of data
        value (float): feels like temp

    Returns:
        Nothing
    """
    print_temp('Feels Like', value, units)


def print_temp_max(key, value, units=IMPERIAL):
    """Prepare high temp info

    Args:
        key (string): description of data
        value (float): high temp

    Returns:
        Nothing
    """
    print_temp('High', value, units)


def print_temp_min(key, value, units=IMPERIAL):
    """Prepare low temp info

    Args:
        key (string): description of data
        value (float): low temp

    Returns:
        Nothing
    """
    print_temp('Low', value, units)


def print_visibility(key, value, units=IMPERIAL):
    """Prepare and display visibility info

    Args:
        key (string): description of data
        value (float): visibility in meters

    Returns:
        Nothing
    """
    key = format_title(key)

    if METRIC in units:
        value = f'{value:.2f}m'

    else:
        value = f'{value * METER2MILE:.2f}mi'

    print(f'{key:<{LJUST}}{value:>{RJUST}}')


def print_wind(key, value, units=IMPERIAL):
    """Prepare and display wind info

    Args:
        key (string): description of data
        value (dict): wind speed and direction

    Returns:
        Nothing
    """
    for k, v in value.items():
        if 'deg' in k:
            key = format_title('Wind direction')
            cardinal_direction = getWindDirection(value['deg'])
            svalue = f"{cardinal_direction} - {value['deg']}{DEGREE}"

        else:
            key = format_title(f'Wind {k}')
            if METRIC in units:
                tag = 'm/s'
            else:
                tag = 'mph'

            svalue = f'{value[k]}{tag}'

        print(f'{key:<{LJUST}}{svalue:>{RJUST}}')


def print_clouds(key, value, units=IMPERIAL):
    """Prepare and display cloud info

    Args:
        key (string): description of data
        value (int): percentage of cloud coverage

    Returns:
        Nothing
    """
    key = format_title(key)
    value = f"{value['all']}%"
    print(f'{key:<{LJUST}}{value:>{RJUST}}')


def print_snow_rain(key, value, units=IMPERIAL):
    """Prepare and display snow/rain info

    Args:
        key (string): description of data
        value (list): how much snow/rain 1h and 3h

    Returns:
        Nothing
    """
    key = format_title(key)
    for k, v in value.items():
        if METRIC in units:
            value = f'{k}: {v:.2f}mm'

        else:
            value = f'{k}: {v * MM2INCH:.2f}in'

        print(f'{key:<{LJUST}}{value:>{RJUST}}')


def print_sys(key, value, units=IMPERIAL, tz=None):
    """Driver/Prepare display of the sunrise/sunset

    Args:
        key (string): description of data
        value (datetime): date/time

    Returns:j
        Nothing
    """
    print_riseset('Sunrise', value['sunrise'], tz)
    print_riseset('Sunset', value['sunset'], tz)


def print_riseset(title, value, tz):
    """Actual display of the sunrise/sunset

    Args:
        title (string): description of data
        value (datetime): date/time

    Returns:
        Nothing
    """
    key = format_title(title)

#    date = datetime.datetime.fromtimestamp(value)

    gvalue = time.strftime('%H:%M %Z', time.gmtime(value))
    lvalue = time.strftime('%H:%M %Z', time.localtime(value))

    print(f'{key:<{LJUST}}{lvalue} ({gvalue:>{RJUST}})')


def verifyLocation(loc, search=None):
    """Initial driver to verify the location entered by the user

    Args:
        loc (string|int): city/sate || zip
        search (object): option seach data base on uszipcode

    Returns:
        zipinfo (dict): zip data
    """
    warn_msg = 'WARNING: Please enter valid <city, state> or <zipcode>'

    if search is None:
        zipinfo = verifyLocationByURL(loc)
    else:
        zipinfo = verifyLocationByAPI(loc, search)

    if zipinfo is None:
        print(warn_msg)

    return zipinfo


def verifyLocationByAPI(loc, search):
    """ Verify location based on API (uszipcode)

    Args:
       loc (string|int): City/State|zip
       search (dict): zipcode hash/object

    Returns:
        zipinfo (dict): location data
    """
    if loc.isdigit() and len(loc) == 5:
        zipinfo = search.by_zipcode(loc)

        if zipinfo.zipcode is None:
            return None

        zipinfo = normalize_zipinfo(zipinfo=zipinfo)

    elif ',' in loc:
        if loc.count(',') > 1:
            city, state, junk = loc.split(',')

        else:
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
    """determine wind direction based on degree/radian

    Args:
        degree (int): randian of window direction

    Returns:
        string: cardinal direction
    """
    ix = round(degree / (360 / len(WIND_DIRS)))
    idx = ix % len(WIND_DIRS)

    if USE_ARROWS:
        result = f'{WIND_DIRS[idx]} {WIND_ARROWS[idx]}'
    else:
        result = f'{WIND_DIRS[idx]}'

    return result


def verifyLocationByURL(loc):
    """ Verify location based on URL call

    Args:
        loc (string|int): City/State || zipcode

    Returns:
        zipinfo (dict): location data
    """
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
            ('city', f'{city.title()}'),
            ('state_name', f'{STATES.get(state.upper(), None)}'),
            ('country', 'us'.upper()),
        )

        zipinfo = getInfo(ZIPCODE_CITY, headers=headers, params=params)
        if not len(zipinfo['results']):
            zipinfo = None
        else:
            zipinfo = normalize_zipinfo(zipinfo=zipinfo)

    return zipinfo


def normalize_zipinfo(zipinfo=None):
    """ Normalize the zip info since pulling from differwent sources
    could easily be modified to return long/lat too

    Args:
        zipinfo (dict): zipinfo
        zipinfo (object): zipinfo

    Returns:
        data (dict): zipinfo
    """
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
    """search by state
    Pass in long name state and return abbreviated state name

    Args:
        state (string): full state name

    Returns:
        string: abbreviated state name
    """
    for key, value in STATES.items():
        if state in value:
            return key.capitalize()


def getInfo(url, headers=None, params=None):
    """ Primary Url connector - uses the requests
    library to pull content from the web.

    Args:
        string: url
        dict: optional header info
        params: optional params info

    Returns:
        dict: url data
    """
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
