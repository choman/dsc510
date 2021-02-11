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
#  Chad Homan     2021-02-08        primary header
#

import json
import requests

try:
    import uszipcode
    USE_USZIPCODE = True

except ModuleNotFoundError:
    print(f"Proceeding w/o uszipcode module")
    USE_USZIPCODE = False

QUIT   = "q"
APIKEY = "af6ca8a2c9759b2d33ec039bd9c21bbd"
APIKEY = "b5fc619b5bbbf6aacbcdd198e5e5fab1"


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
        print(f"{zip}")
        if "," in zip:
            url_data.append(f"q={zip},us")

        else:
            url_data.append(f"zip={zip},us")

    adjurl   = "&".join(url_data)
    url      = f"{baseurl}{adjurl}"

    print(url)
    r = requests.get(url)
    return json.loads(r.content)


def display_Weather(weather):
    d = chr(176) + "F"
    trans = {
        "temp_max": "High",
        "temp_min": "Low",
        "feels_like": "Feels Like",
    }

    print(weather)
    print(weather["weather"])
    print(weather["main"])
    temps = weather['main']
    print()
    print(f"Current weather in {weather['name']}:")
    print()
    for k, v in temps.items():
        tag = d
        if k == "humidity":
            tag = "%"
        if k == "pressure":
            tag = "in"
        if k in trans:
            print(f" {trans[k]}:        {v}{tag}")

        else:
            print(f" {k.capitalize()}:        {v}{tag}")

    print()
    print(f" Feels Like:  {temps['feels_like']}{d}")
    print(f" High / Low:  {temps['temp_max']}{d} / {temps['temp_min']}{d}")
    print(f" Description: {weather['weather'][0]['description']}")


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

    else:
        print(f"WARNING: Please enter valid <city, state> or <zipcode>")
        zipinfo = None

    return zipinfo


if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        print()
