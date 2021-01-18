# DSC 510
# Week 5
# Programming Assignment Week 5
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
#  Chad Homan     2021-01-13        Added areEntriesValid()
#  Chad Homan     2021-01-12        Doing research and discovered operator
#                                       module
#                                   Improved input validation
#  Chad Homan     2021-01-12        Consolidated two functions into one
#                                   Corrected divide by zero error
#  Chad Homan     2021-01-10        Added function headers, linted
#                                   resolved issue in printAverages
#  Chad Homan     2021-01-05        Initial header and code
#                                   updated comments- line up
#                                   Added initial menu
#                                   Added initial average code - needs
#                                       breaking up
#                                   Added initial calc code - needs
#                                       test and tweaking
#

import sys
import operator

actions = {
    "1": "Perform Calculation",
    "2": "Calculate Average",
}

calc_options = {
    "+": "Addition",
    "-": "Subtraction",
    "*": "Multiplication",
    "/": "Division",
}

math_options = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
}


# function: main()
# abstract: Main program
#
def main():
    while True:
        printMenu(actions)
        action = input("Selection: ").strip()
        processAction(action)


# function: printMenu()
# abstract: print simple menu
#
def printMenu(menu):
    print("what would you like to do:\n")

    [print(f"   ({key}) {value}") for key, value in menu.items()]

    print()
    print("   (q) quit\n")


# function: processAction()
# abstract: determine choice made by user
#
def processAction(action=None):
    if action is None:
        pass

    if action == "1":
        beginCalculation()

    elif action == "2":
        calculateAverage()

    elif action == "q".lower():
        sys.exit()

    else:
        printWarningMsg("Invalid Selection, please choose again")


# function: beginCalculation()
# abstract: initialize calculation
#
def beginCalculation():
    printMenu(calc_options)
    action = input("Selection: ").strip()
    processCalcOption(action)


# function: printMsg()
# abstract: function to print messages
#
def printWarningMsg(msg):
    print(f"WARNING: {msg}")
    print()
    print()


# function: areEntriesValid()
# abstract: perfom valid tests on entries
#
def areEntriesValid(action=None, entries=None):
    valid = True

    if not len(entries) == 2:
        printWarningMsg("Require two and only two entries")
        valid = False

    for count, value in enumerate(entries, start=1):
        if not testInt(value):
            printWarningMsg(f"Not a valid integer #{count}: {value}")
            valid = False

    return valid


# function: performCalculation()
# abstract: perfom calculation of two numbers
#
def performCalculation(action):
    print()
    numbers = input(f"Please enter two numbers separted by spaces: ")
    numbers = numbers.split()

    if not areEntriesValid(entries=numbers):
        return

    num1, num2 = [int(tmp) for tmp in numbers]

    if "/" in action and num2 == 0:
        printWarningMsg("Cannot divide by zero (0)")
        return

    mesg = f"{num1} {action} {num2}"
    ans = math_options[action](num1, num2)

    print(f"Results: {mesg}: {ans}\n\n")


# function: performCalcOption()
# abstract: based on user input, perform that type of calculation
#
def processCalcOption(action):
    if action in calc_options:
        performCalculation(action)

    else:
        printWarningMsg("Invalid Selection, please choose again")


# function: calculateAverage()
# abstract: based on a user defined quantity of numbers, find the average
#
def calculateAverage():
    numbers = []

    while True:
        try:
            count = int(input("\nHow many numbers to average? "))

            if count <= 0:
                print("Please enter a positive number greater then 0")

            else:
                break

        except ValueError:
            print("Invalid entry, please enter an integer")

    for x in range(count):
        digit = input("Enter numner: ")

        if testInt(digit):
            numbers.append(int(digit))

        else:
            print("Bad number, please enter positive number")

    total, average = getTotalAndAverage(numbers)
    printAverages(numbers, total, average)


# function: getTotalAndAverage()
# abstract: Main program
#
def getTotalAndAverage(numbers):
    total   = sum(numbers)
    average = total / len(numbers)

    return total, average


# function: printAverages()
# abstract: print results of the averages
#
def printAverages(numbers, total, average):
    tmp = [str(x) for x in numbers]

    print()
    print(f"Numbers: {', '.join(tmp)}")
    print(f"Sum:     {total}")
    print(f"Average: {average:.02f}")
    print()


# function: testInt()
# abstract: verify the numbers entered are int's
#           The is example code from the internet, I forgot
#           from where.
#
def testInt(value):
    try:
        float(value)
    except ValueError:
        return False
    else:
        return float(value).is_integer()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
