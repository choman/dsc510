# DSC 510
# Week 4
# Programming Assignment Week 4
# Author: Chad Homan
# 2021/01/05
#
# Abstract: This week we will create a program which works with lists.
#           Your goal is to create a program which contains a list of
#           temperatures. Your program will populate the list based upon
#           user input. Your program will determine the number of
#           temperatures in the program, determine the largest temperature,
#           and the smallest temperature.
#
# Create a program with the following requirements:
#
#  - Your program must have a header.
#  - Create an empty list called temperatures.
#  - Allow the user to input a series of temperatures along with a sentinel
#    value which will stop the user input.
#  - Evaluate the temperature list to determine the largest and smallest
#    temperature.
#  - Print the largest temperature.
#  - Print the smallest temperature.
#  - Print a message tells the user how many temperatures are in the list.
#
#
# Record Of Modifications
#    Author         Date            Description
#  ----------    ------------       ----------------------------------
#  Chad Homan     2021-01-18        added docstrings
#                                   experimentnig with min/max
#  Chad Homan     2021-01-17        fixed flake8 linter issues
#                                   added headers on functions
#  Chad Homan     2021-01-15        initial code
#

DONE      = "done"
USE_INDEX = False


# function: main()
# abstract: Main program
#
def main():
    """Primary program driver"""
    temperatures, junk = getTemps()

    if USE_INDEX:
        temperatures = processTemps(temperatures)

    printTemps(temperatures)


# function: getTemps()
# abstract: Gather a list of temperature from user input
#
def getTemps():
    """User input driver

    Gather input from user, done to quit
    alphanumeric entries are placed into 'bad'
    """

    temperatures = []
    bad          = []

    print(f"Enter temperatures, when finished enter: {DONE}\n")

    while True:
        temp = input("Enter temperature: ").strip()

        if DONE in temp.lower():
            break

        if testTemp(temp):
            temperatures.append(float(temp))

        else:
            bad.append(temp)

    return temperatures, bad


# function: testTemp()
# abstract: verify the numbers entered are float's
#
def testTemp(temp):
    """testTemp

    :param temp: item to testG
    :return: Boolean: True if float or int, False if not
    """

    try:
        float(temp)
        return True

    except ValueError:
        return False


# function: processTemps()
# abstract: Currently sorts the list lowest to highest
#
def processTemps(temps):
    """procesTemps

    :param temps: list of temperature values
    :return: sorted list of values
    """

    return sorted(temps)


# function: printTemps()
# abstract: Displays the following infomation
#           - highest temperature entered
#           - lowest temperature entered
#           - number of temperatures entered
#
def printTemps(temps):
    """procesTemps

    :param temps: list of temperature values
    """
    count   = len(temps)

    if USE_INDEX:
        lowest  = temps[0]
        highest = temps[-1]
    else:
        lowest  = min(temps)
        highest = max(temps)

    print()
    print(f"Highest Temperature: {highest}")
    print(f"Lowest Temperature:  {lowest}")
    print()
    print(f"Number of temperatures: {count}")


if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        print()
