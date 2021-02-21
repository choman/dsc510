# DSC 510
# Week 11
# Programming Assignment Week 11
# Author: Chad Homan
# 2021/02/17
#
# Abstract: This week we’re going to demonstrate our knowledge of Python
#           object oriented programming concepts by creating a simple cash
#           register program.
#
# Create a program with the following requirements:
#  - Your program must have a header.
#  - Your program must have a welcome message for the user.
#  - Your program must have one class called CashRegister.
#      - Your program will have an instance method called addItem which
#        takes one parameter for price. The method should also keep track
#        of the number of items in your cart.
#      - Your program should have two getter methods.
#          - getTotal – returns totalPrice
#          - getCount – returns the itemCount of the cart
#  - Your program must create an instance of the CashRegister class.
#  - Your program should have a loop which allows the user to continue to
#    add items to the cart until they request to quit.
#  - Your program should print the total number of items in the cart.
#  - Your program should print the total $ amount of the cart.
#      - The output should be formatted as currency. Be sure to investigate
#        the locale class. You will need to call locale.setlocale and
#        locale.currency.
#
# Record Of Modifications
#    Author         Date            Description
#  ----------    ------------       ----------------------------------
#  Chad Homan     2021-02-21        privatized count and total
#                                   added 'getter' via a property
#                                   added locale
#  Chad Homan     2021-02-17        initial code
#

import locale


class CashRegister():

    def __init__(self):
        locale.setlocale(locale.LC_ALL, '')
        self.__count = 0
        self.__total = 0

    def addItem(self, price):
        self.__count += 1
        self.__total += price

    @property
    def getCount(self):
        return self.__count

    @property
    def getTotal(self):
        return locale.currency(self.__total, symbol=True)


# function: main()
# abstract: Main program
#
def main():
    welcome()

    cart = CashRegister()

    while True:
        price = input("Enter price to add another item: ")
        price = price.strip()

        if not len(price):
            break

        cart.addItem(float(price))

    print()
    print(f"Items in your cart: {cart.getCount}")
    print(f"Total price:        {cart.getTotal}")


# function: welcome()()
# abstract: welcome message
#
def welcome():
    print()
    print("Welcome to Chad's Mini-Mart")


if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        print()
