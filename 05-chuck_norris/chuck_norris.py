# DSC 510
# Week 10
# Programming Assignment Week 10
# Author: Chad Homan
# 2021/02/12
#
# Abstract: We’ve already looked at several examples of API integration from
#           a Python perspective and this week we’re going to write a program
#           that uses an open API to obtain data for the end user.
#
# Create a program with the following requirements:
#   - Create a program which uses the Request library to make a GET request
#     of the following API: Chuck Norris Jokes.
#   - The program will receive a JSON response which includes various pieces
#     of data. You should parse the JSON data to obtain the “value” key. The
#     data associated with the value key should be displayed for the user
#     (i.e., the joke).
#   - Your program should allow the user to request a Chuck Norris joke as
#     many times as they would like. You should make sure that your programs
#     does error checking at this point. If you ask the user to enter “Y” and
#     they enter y, is that ok? Does it fail? If it fails, display a message
#     for the user. There are other ways to handle this. Think about included
#     string functions you might be able to call.
#   - Your program must include a header as in previous weeks.
#   - Your program must include a welcome message for the user.
#   - Your program must generate “pretty” output. Simply dumping a bunch of
#     data to the screen with no context doesn’t represent “pretty.”
#
# Record Of Modifications
#    Author         Date            Description
#  ----------    ------------       ----------------------------------
#  Chad Homan     2021-02-14        added textwrap and macro WIDTH
#  Chad Homan     2021-02-13        added requests.exceptions
#  Chad Homan     2021-02-12        initial code
#                                   added requests and joke parser
#                                   started pretty print
#

import json
import requests
import textwrap
import sys

QUIT  = "n"
URL   = "https://api.chucknorris.io/jokes/random"
WIDTH = 70


# function: main()
# abstract: Main program
#
def main():
    welcome()

    while True:
        result = wantJoke()
        exit_program(result)
        joke = get_joke()
        pretty_print(joke)


# function: wantJoke()
# abstract: asks user if they want to hear a joke
#
def wantJoke():
    """ask user for joke"""
    print()
    result = input("Would you like to hear a Chuck Norris joke [Y/n]? ")
    return result


# function: get_joke()
# abstract: get a chuck norris joke
#
def get_joke():
    """query URL for random CN joke"""
    try:
        result = requests.get(URL)
        result.raise_for_status()
        data = json.loads(result.content)

    except requests.exceptions.ConnectionError as err:
        raise SystemExit(err)

    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)

    except requests.exceptions.RequestException as err:
        raise SystemExit(err)

    return data


# function: pretty_print()
# abstract: print joke
#
def pretty_print(data):
    jokeList = textwrap.wrap(data['value'], width=WIDTH)
    print()
    print("-" * WIDTH)
    [print(f"{line}") for line in jokeList]
    print("-" * WIDTH)


# function: welcome()
# abstract: welcome message
#
def welcome():
    print()
    print("Welcome to Chad's Chuck Norris joke machine!")
    print("Follow the directions to see a joke, enter 'n' to quit")
    print("anything else will show a joke. Blah-ha-ha")


# function: exit_program()
# abstract: exit program
#
def exit_program(result):
    if len(result) and result.lower() in QUIT:
        sys.exit()


if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        print()
