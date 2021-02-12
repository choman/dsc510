# DSC 510
# Week 12 (term project)
# Programming Assignment Week 12 (term project)
# Author: Chad Homan
# 2021/02/03
#
# Abstract: For your class project we will be creating an application to
#           interacts with a webservice in order to obtain data. Your
#           program will use all of the information you’ve learned in the
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
#   - Validate whether the user entered valid data. If valid data isn’t
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
#  Chad Homan     2021-02-12        added dynamic print for weather types
#                                   added print_debug()
#  Chad Homan     2021-02-11        added hPa to inch convert
#                                   added degree symbol
#                                   working on both zipcode and no zipcode
#                                   Initial output display
#  Chad Homan     2021-02-08        primary header
#

import datetime
import json
import requests
import sys
import time

try:
    import uszipcode
    USE_USZIPCODE = True

except ModuleNotFoundError:
    print(f"Proceeding w/o uszipcode module")
    USE_USZIPCODE = False

QUIT       = "q"
APIKEY     = "af6ca8a2c9759b2d33ec039bd9c21bbd"
APIKEY     = "b5fc619b5bbbf6aacbcdd198e5e5fab1"
DEGREE     = chr(176) + "F"
HPA2INCH   = .02953
METER2MILE = .000621371
MM2INCH    = .0393701
LJUST      = 15
RJUST      = 1
DEBUG      = False


# function: main()
# abstract: Main program
#
def main():
    getLocation()


# function: getLocation()
# abstract: Get a location to obtain weather info
#
def getLocation():
    search = None

    if USE_USZIPCODE:
        search = uszipcode.SearchEngine(simple_zipcode=True)

    while True:
        print()
        location = input(f"Enter location (<zip> or <city, state>): ").strip()

        if location.lower() in QUIT:
            sys.exit()

        zipinfo = verifyLocation(location, search)
        print(f"zipinfo = {zipinfo}")

        if zipinfo:
            weather_info = getWeather(zipinfo)
            display_Weather(weather_info)

    ##print(f"location = {location}")
    return zipinfo


def getWeather(zip):
    part     = "minutely"
    units    = "imperial"
    baseurl  = "https://api.openweathermap.org/data/2.5/onecall?"
    baseurl  = "https://api.openweathermap.org/data/2.5/weather?"
    url_data = [
       f"units={units}",
       f"appid={APIKEY}",
    ]

    if USE_USZIPCODE:
        url_data.append(f"lat={zip.lat}")
        url_data.append(f"lon={zip.lng}")

    else:
        print_debug(zip)

        if "," in zip:
            url_data.append(f"q={zip},us")

        else:
            url_data.append(f"zip={zip},us")

    adjurl   = "&".join(url_data)
    url      = f"{baseurl}{adjurl}"

    print(url)
    r = requests.get(url)
    return json.loads(r.content)

def print_debug(msg):
    if DEBUG:
        print(f"DEBUG: {msg}")

def display_Weather(weather):
    temps = weather['main']

    print_calls = {
        "humidity": print_humidity,
        "pressure": print_pressure,
        "temp_max": print_temp_max,
        "temp_min": print_temp_min,
        "feels_like": print_feels_like,
        "temp": print_temp,
        "visibility": print_visibility,
        "wind": print_wind,
        "clouds": print_clouds,
        "sys": print_sys,
        "snow": print_snow_rain,
        "rain": print_snow_rain,
    }

    print_debug(weather)
    print_debug(weather["weather"])
    print_debug(weather["main"])

    print()
    print(f"Current weather in {weather['name']}:\n")

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
    key = format_title("Description")
    for desc in weather['weather']:
        print(f"{key:<{LJUST}}{desc['description'].capitalize()}")

def format_title(key):
    key = f" {key.capitalize()}:"
    return key

def print_humidity(key, value):
    key = format_title(key)
    print(f"{key:<{LJUST}}{value:>{RJUST}}%")

def print_pressure(key, value):
    key = format_title(key)
    value = f"{value * HPA2INCH:.2f}in"
    print(f"{key:<{LJUST}}{value:>{RJUST}}")

def print_temp(key, value):
    key = format_title(key)
    value = f"{value}{DEGREE}"
    print(f"{key:<{LJUST}}{value:>{RJUST}}")

def print_feels_like(key, value):
    print_temp("Feels Like", value)

def print_temp_max(key, value):
    print_temp("High", value)

def print_temp_min(key, value):
    print_temp("Low", value)

def print_visibility(key, value):
    key = format_title(key)
    value = f"{value * METER2MILE:.2f}mi"
    print(f"{key:<{LJUST}}{value:>{RJUST}}")

def print_wind(key, value):
    key = format_title(key)
    value = f"{value['speed']}mph {value['deg']}"
    print(f"{key:<{LJUST}}{value:>{RJUST}}")

def print_clouds(key, value):
    key = format_title(key)
    value =f"{value['all']}%"
    print(f"{key:<{LJUST}}{value:>{RJUST}}")

def print_snow_rain(key, value):
    key = format_title(key)
    for k, v in value.items():
        print(f"{key:<{LJUST}}     {k}: {v * MM2INCH:.2f}in")
        
def print_sys(key, value):
    value['sunrise'] = time.strftime("%H:%M", time.localtime(value['sunrise']))
    value['sunset'] = time.strftime("%H:%M", time.localtime(value['sunset']))
    key = format_title('Sunrise')
    print(f"{key:<{LJUST}}{value['sunrise']:>{RJUST}}")
    key = format_title('Sunset')
    print(f"{key:<{LJUST}}{value['sunset']:>{RJUST}}")

def verifyLocation(loc, search=None):

    if loc.isdigit() and len(loc) == 5:
        if search is None:
            zipinfo = loc

        else:
            zipinfo = search.by_zipcode(loc)

    elif "," in loc:
        city, state = loc.split(",")
        city  = city.strip()
        state = state.strip()

        if search is None:
            zipinfo = f"{city},{state}"

        else:
            zipinfo = search.by_city_and_state(city, state)[0]
            print(zipinfo)

    else:
        print(f"WARNING: Please enter valid <city, state> or <zipcode>")
        zipinfo = None

    return zipinfo


if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        print()
