# DSC 510
# Week 12 (term project)
# Programming Assignment Week 12 (term project)
# Author: Chad Homan
# 2021/01/05
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

DONE = "done"


# function: main()
# abstract: Main program
#
def main():
    location = getLocation()


# function: getLocation()
# abstract: Get a location to obtain weather info
#
def getLocation():

    while True:
       location = input(f"Enter location (zip or city, state): ").strip()

       if verifyLocation(location):
           break

    print(f"location = {location}")
    return location

def verifyLocation(loc):

    if loc.isdigit() and len(loc) == 5:
        return True

    elif "," in loc:
        pass

    return False

if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        print()
