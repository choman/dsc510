# DSC 510
# Week 4
# Programming Assignment Week 4
# Author: Chad Homan
# 2021/01/05
#
# Abstract: This program performs basic math and averages based on user
#           input. 
#
# Create a program with the following requirements:
#
#  * Your program must have a header.
#  * This program will perform various calculations (addition, 
#    subtraction, multiplication, division, and average calculation)
#  * This program will contain a variety of loops and functions.
#  * The program will add, subtract, multiply, divide two numbers and
#    provide the average of multiple numbers input by the user.
#  * Define a function named performCalculation which takes one parameter.
#    The parameter will be the operation being performed (+, -, *, /).
#     - This function will perform the given prompt the user for two 
#       numbers then perform the expected operation depending on the
#       parameter that's passed into the function.
#     - This function will print the calculated value for the end user.
#  * Define a function named calculateAverage which takes no parameters.
#      - This function will ask the user how many numbers they wish to 
#        input.
#      - This function will use the number of times to run the program 
#        within a for loop in order to calculate the total and average.
#      - This function will print the calculated average.
#  * This program will have a main section which contains a while loop. 
#    The while loop will be used to allow the user to run the program 
#    until they enter a value which ends the loop.
#  * The main program should prompt the user for the operation they wish
#    to perform.
#  * The main program should evaluate the entered data using if 
#    statements.
#  * The main program should call the necessary function to perform the 
#    calculation.
#
# Record Of Modifications
#    Author         Date            Description
#  ----------    ------------       ----------------------------------
#  Chad Homan     2021-01-05        Initial header and code
#                                   updated comments- line up
#                                   Added initial menu
#

import datetime
import sys

actions = {
    "1": "Perform Calculation",
    "2": "Calculate Average",
}

calc_options = ["+", "-", "*", "/"]


def main():
    while True:
        printMenu()
        action = input("Selection: ")
        processAction(action)

def printMenu():
    print("what would you like to do:\n")
    
    for key, value in actions.items():
        print(f"   ({key}) {value}")
    
    print()
    print("   (q) quit\n")

def processAction(action=None):
    if action is None:
        pass
    
    if action == "1":
        beginCalculation()

    elif action == "2":
        beginAverage()

    elif action == "q".lower():
        sys.exit()

    else:
        print("Invalid Selection, please choose again")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
