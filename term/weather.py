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
import uszipcode

DONE   = "done"
APIKEY = "af6ca8a2c9759b2d33ec039bd9c21bbd"


# function: main()
# abstract: Main program
#
def main():
    location = getLocation()
    weather_info = getWeather(location)
    display_Weather(weather_info)


# function: getLocation()
# abstract: Get a location to obtain weather info
#
def getLocation():

    search = uszipcode.SearchEngine(simple_zipcode=True) #

    while True:
        location = input(f"Enter location (zip or city, state): ").strip()

        zipinfo = verifyLocation(location, search)
        if zipinfo:
            break

    ##print(f"location = {location}")
    print(f"zipinfo = {zipinfo}")
    return zipinfo


def getWeather(zip):

    part     = "minutely"
    units    = "imperial"
    baseurl  = "https://api.openweathermap.org/data/2.5/onecall?"
    url_data =  [
       f"lat={zip.lat}",
       f"lon={zip.lng}",
       f"exclude={part}",
       f"units={units}",
       f"appid={APIKEY}",
    ]
    adjurl   = "&".join(url_data)
    url      = f"{baseurl}{adjurl}"

    r = requests.get(url)
    return json.loads(r.content)


def display_Weather(weather):
    print(weather)
    print(weather["current"])



def verifyLocation(loc, search):

    if loc.isdigit() and len(loc) == 5:
        zipinfo = search.by_zipcode(loc)

    elif "," in loc:
        city, state = loc.split(",")
        city  = city.strip()
        state = state.strip()
        zipinfo = search.by_city_and_state(city, state)[0]

    else:
        zipinfo = None

    return zipinfo


if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        print()
