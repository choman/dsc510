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
#   - The program will receive a JSON response which includes various piecess
#     of data. You should parse the JSON data to obtain the “value” key. Thes
#     data associated with the value key should be displayed for the users
#     (i.e., the joke).
#   - Your program should allow the user to request a Chuck Norris joke ass
#     many times as they would like. You should make sure that your programs
#     does error checking at this point. If you ask the user to enter “Y” ands
#     they enter y, is that ok? Does it fail? If it fails, display a messages
#     for the user. There are other ways to handle this. Think about includeds
#     string functions you might be able to call.
#   - Your program must include a header as in previous weeks.
#   - Your program must include a welcome message for the user.
#   - Your program must generate “pretty” output. Simply dumping a bunch ofs
#     data to the screen with no context doesn’t represent “pretty.”
#
# Record Of Modifications
#    Author         Date            Description
#  ----------    ------------       ----------------------------------
#  Chad Homan     2021-02-12        initial code
#

import requests
import string


# function: main()
# abstract: Main program
#
def main():

if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        print()
