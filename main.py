# DSC 510
# Week 1
# Programming Assignment Week 1
# Author: Chad Homan
# 2020/12/05
#
#
# Create a program with the following requirements:
#    Using comments, create a header at the top of the program indicating the purpose of the program, assignment number, and your name. Refer to the submission instructions for an example of a header.
#    Display a welcome message for your user.
#    Retrieve the company name from the user.
#    Retrieve the number of feet of fiber optic cable to be installed from the user.
#    Calculate the installation cost of fiber optic cable by multiplying the total cost as the number of feet times $0.87.
#    Print a receipt for the user including the company name, number of feet of fiber to be installed, the calculated cost, and total cost in a legible format.
#    Include appropriate comments throughout  program.

import datetime
import sys

CABLE_PRICE = 0.87

# function: main()
# abstract: Main program
def main():
    data = {}

    data['company_name'] = getCompanyName()
    data['feet'] = getRequiredFeet(data['company_name'])
    data['cost'] = calculateCost(data['feet'])

    printReceipt(data)

# function: getCompanyName()
# abstract: Get company name
def getCompanyName():
    greet_msg = "Greetings, what is your company names? "
    company_name = input(greet_msg)

    return company_name

# function: getRequiredFeet()
# abstract: Get length of fiber optic cable in feet
def getRequiredFeet(company_name=None):
    while True:
        ans = input(f"Welcome from {company_name}, how many feet of fiber optic cable do you need? ")

        try:
            feet = float(ans)

        except:
            print ("Invalid response, please enter required feet")
            continue

        ans = input(f"You are asking for {feet} of fiber optic cable [Y/n]: ")

        if 'y' in ans.lower():
            return feet

# function: calculateCost()
# abstract: Calculate the cost of the request length of
#           fiber optic cable
def calculateCost(feet=0):
    cost = feet * CABLE_PRICE
    cost = f"${cost:.2f}"
    print (f"\nThe price for {feet} of fiber optic cable is: {cost}")

    return cost

def printReceipt(data):
    now = datetime.datetime.now()
    date = f'{now:%Y-%m-%d %H:%M}'
    print(data)
    pad = ''

    receipt = f"""
               Bozo's Fiber World
                {date}

Item                                       Price
----------------------                     -------
Fiber Optic Cable: {data['feet']}ft{data['cost']:>23}

----------------------                     -------
Total                                      {data['cost']}

Thank you! Please come again.
"""

    print(f"{receipt}")




if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
