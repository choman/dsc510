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
#
#  Record of Modifications:
#
#    Author         Date         Description
#   ---------     ----------     -
#   Chad Homan    2020-12-14
#
import datetime
import sys

CABLE_PRICE     = 0.87
CABLE_PRICE_100 = 0.70
CABLE_PRICE_250 = 0.50
DEBUG           = False


# function: main()
# abstract: Main program
#
def main():
    receipt_info = {}

    receipt_info['company_name'] = getCompanyName()
    receipt_info['feet'] = getRequiredFeet(receipt_info['company_name'])
    receipt_info['price'] = getPricePerFoot(receipt_info)
    receipt_info['cost'] = calculateCost(receipt_info)

    printReceipt(receipt_info)

# Function: getCompanyName
# Abstract: Get company name
#
def getCompanyName():
    greet_msg    = "Greetings, what is your company name? "
    company_name = input(greet_msg)

    return company_name

# Function: getRequiredFeet
# Abstract: Get length of fiber optic cable in feet
#
def getRequiredFeet(company_name=None):
    while True:
        ans = input(f"Welcome from {company_name}, how many feet of fiber optic cable do you need? ")

        try:
            feet = float(ans)

        except:
            print("Invalid response, please enter required feet")
            continue

        ans = input(f"You are asking for {feet} of fiber optic cable [Y/n]: ")

        if 'y' in ans.lower():
            return feet

# Function: getPricePerFoot
# Abstract: Get length of fiber optic cable in feet
#
def getPricePerFoot(receiptInfo):
    if receiptInfo['feet'] > 250:
        price = CABLE_PRICE_250

    elif receiptInfo['feet'] > 100:
        price = CABLE_PRICE_100

    else:
        price = CABLE_PRICE

    return price


# Function: calculateCost
# Abstract: Calculate the cost of the request length of
#           fiber optic cable
#
def calculateCost(receiptInfo):
    cost = receiptInfo['feet'] * receiptInfo['price']
    cost = f"${cost:.2f}"
    print(f"\nThe price for {receiptInfo['feet']} of fiber optic cable is: {cost}")

    return cost

def printDebug(msg=None):
    if DEBUG:
        print(f"{msg}")

# Function: printReceipt
# Abstract: display receipt
#
def printReceipt(receipt_info):
    now  = datetime.datetime.now()
    date = f'{now:%Y-%m-%d %H:%M}'
    item = f"Fiber Optic Cable: {receipt_info['feet']}"

    printDebug(receipt_info)

    #{\'Fiber Optic Cable: {receipt_info['feet']}\':20}{receipt_info['cost']:>20}
    # Heredoc as my receipt
    receipt = f"""
               Bozo's Fiber World
               ==================

Company: {receipt_info['company_name']}
Date:    {date}
Price:   ${receipt_info['price']:.2f}/ft

{"Item":30}{"Price":>10}
{"----------------------":30}{"-----":>10}
{item:30}{receipt_info['cost']:>10}

{"----------------------":30}{"-----":>10}
{"Total":30}{receipt_info['cost']:>10}

Thank you! Please come again.
"""
    print(f"{receipt}")


if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        print()
        pass
