# DSC 510
# Week 8
# Programming Assignment Week 8
# Author: Chad Homan
# 2021/01/05
#
# Abstract: We will create a program which performs three essential
#           operations. It will process this .txt file: Gettysburg.txt.
#           Calculate the total words, and output the number of
#           occurrences of each word in the file.
#
#           - Open the file and process each line.
#           - Either add each word to the dictionary with a frequency
#             of 1 or update the word’s count by 1.
#           - Nicely print the output, in this case from high to low
#             frequency. You should use string formatting for this.
#
#           We want to achieve each major goal with a function
#           (one function, one action). We can find four functions
#           that need to be created.
#
#           add_word: Add each word to the dictionary. Parameters are
#           the word and a dictionary. No return value.
#
#           Process_line: There is some work to be done to process
#           the line: strip off various characters, split out the words,
#           and so on. Parameters are a line and the dictionary. It calls
#           the function add word with each processed word. No return value.
#
#           Pretty_print: Because formatted printing can be messy and
#           often particular to each situation (meaning that we might
#           need to modify it later), we separated out the printing
#           function. The parameter is a dictionary. No return value.
#
#           main: We will use a main function as the main program. As
#           usual, it will open the file and call process_line on each
#           line. When finished, it will call pretty_print to print
#           the dictionary.
#
#           In the main function, you will need to open the file. We
#           will cover more regarding opening of files next week but
#           I wanted to provide you with the block of code you will
#           utilize to open the file, see below.
#
# Create a program with the following requirements:
#
#  - Your program must have a header.
#
# Record Of Modifications
#    Author         Date            Description
#  ----------    ------------       ----------------------------------
#  Chad Homan     2021-02-05        Still playing with the sorting, did not
#                                   like the multiple loops from the 
#                                   pretty_print_sorted1(). After some 
#                                   experimenting, added another function:
#                                      - pretty_print_sorted2()
#  Chad Homan     2021-02-02        Added a second sort to make the pretty
#                                   print sort alphabetically:
#                                      - pretty_print_sorted1()
#  Chad Homan     2021-01-27        resolved issue reading file into list
#                                   fixed pretty_print padding
#  Chad Homan     2021-01-25        initial code
#                                   linted
#                                   added function docstrings
#

import string

PRETTY_PRINT         = 0
PRETTY_PRINT_SORTED1 = 1
PRETTY_PRINT_SORTED2 = 2
FILENAME             = "gettysburg.txt"
USE_BUFFER           = False


# function: main()
# abstract: Main program
#
def main():
    info = {}
    data = []

    if USE_BUFFER:
        openFile(data)
        for line in data:
            process_line(line, info)

    else:
        with open(FILENAME) as gba_file:
            for line in gba_file:
                process_line(line, info)

    if PRETTY_PRINT == PRETTY_PRINT_SORTED1:
        pretty_print_sorted1(info)

    elif PRETTY_PRINT == PRETTY_PRINT_SORTED2:
        pretty_print_sorted2(info)

    else:
        pretty_print(info)


# function: openFile()
# abstract: read in the file for processing
#
def openFile(data):
    """gets the contents of FILENAME"""
    with open(FILENAME) as fp:
        data.extend(fp.readlines())


# function: process_line()
# abstract: process the passed in line
#
def process_line(line, info):
    """Process_line: There is some work to be done to process
    the line: strip off various characters, split out the words,
    and so on. Parameters are a line and the dictionary. It calls
    the function add word with each processed word.

    No return value.
    """

    for item in line.split():
        if "--" in item:
            continue

        item = item.strip().lower()
        item = item.strip(string.punctuation)

        add_word(item, info)


# function: add_word()
# abstract: Add word to dict and increment count
#
def add_word(word, info):
    """add_word: Add each word to the dictionary. Parameters are
    the word and a dictionary.

    No return value.
    """

    info.setdefault(word, 0)
    info[word] += 1


# function: pretty_print()
# abstract: print list nice and clean
#
def pretty_print(info):
    """Pretty_print: Because formatted printing can be messy and
    often particular to each situation (meaning that we might
    need to modify it later), we separated out the printing
    function. The parameter is a dictionary.

    No return value.
    """

    print(f"Length of dictionary: {len(info)}")
    print("Word          Count")
    print("-------------------")

    for word in sorted(info, key=info.get, reverse=True):
        print(f"{word:<12}{info[word]:>5}")


# function: pretty_print_sorted1()
# abstract: print list nice and clean
#
def pretty_print_sorted1(info):
    """Pretty_print: Because formatted printing can be messy and
    often particular to each situation (meaning that we might
    need to modify it later), we separated out the printing
    function. The parameter is a dictionary.


    No return value.
    """

    print(f"Length of dictionary: {len(info)}")
    print("Word          Count")
    print("-------------------")

    mydict = {}
    for word in sorted(info, key=info.get, reverse=True):
        mydict.setdefault(info[word], [])
        mydict[info[word]].append((word, info[word]))

    for k, v in reversed(sorted(mydict.items())):
        for i in sorted(v):
            print(f"{i[0]:<12}{i[1]:>5}")


# function: pretty_print()
# abstract: print list nice and clean
#
def pretty_print_sorted2(info):
    """Pretty_print: Because formatted printing can be messy and
    often particular to each situation (meaning that we might
    need to modify it later), we separated out the printing
    function. The parameter is a dictionary.

    No return value.
    """

    print(f"Length of dictionary: {len(info)}")
    print("Word          Count")
    print("-------------------")

    for word in sorted(sorted(info), key=info.get, reverse=True):
        print(f"{word:<12}{info[word]:>5}")


if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        print()
